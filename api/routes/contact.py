from fastapi import APIRouter, Depends, status, BackgroundTasks, HTTPException
from sqlalchemy.orm import Session
from api.database.connection import get_db
from api.database.schemas.contact import ContactCreate, ContactResponse
from api.crud import contact as crud_contact
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
import logging
from dotenv import load_dotenv
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables - absolute path
env_path = Path(__file__).resolve().parent.parent.parent / '.env'
load_dotenv(env_path)

router = APIRouter()

def send_email_notification(contact_data: ContactCreate):
    """Send email notification for new contact form submission"""
    try:
        email = os.getenv("EMAIL_ADDRESS")
        password = os.getenv("EMAIL_PASSWORD")
        
        logger.info(f"Attempting to send email from: {email}")
        
        if not email or not password:
            raise ValueError("Email credentials not found in environment variables")
        
        # Create email message
        msg = MIMEMultipart()
        msg['From'] = email
        msg['To'] = "deepakkumawat1751@gmail.com"
        msg['Subject'] = f"New Contact: {contact_data.subject}"
        
        body = f"""
        New Contact Form Submission:
        
        Name: {contact_data.name}
        Email: {contact_data.email}
        Subject: {contact_data.subject}
        Message:
        {contact_data.message}
        """
        
        msg.attach(MIMEText(body, 'plain'))
        
        # Connect to SMTP server
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.ehlo()
            server.starttls()
            logger.info("Attempting SMTP login...")
            server.login(email, password)
            logger.info("SMTP login successful, sending email...")
            server.send_message(msg)
            logger.info("✅ Email sent successfully")
            
    except smtplib.SMTPAuthenticationError as e:
        logger.error(f"❌ SMTP Authentication Failed: {e}")
        logger.error("Please verify:")
        logger.error("1. You're using an App Password (not regular password)")
        logger.error("2. 2FA is enabled in your Google account")
        logger.error("3. App password was generated for 'Mail'")
    except Exception as e:
        logger.error(f"❌ Unexpected error: {str(e)}")

@router.post("/", response_model=ContactResponse, status_code=status.HTTP_201_CREATED)
async def submit_contact(
    contact: ContactCreate, 
    db: Session = Depends(get_db),
    background_tasks: BackgroundTasks = None
):
    """Handle contact form submission"""
    try:
        # Store in database
        db_contact = crud_contact.create_contact(db, contact)
        
        # Send email in background
        if background_tasks:
            background_tasks.add_task(send_email_notification, contact)
        else:
            send_email_notification(contact)
            
        return db_contact
        
    except Exception as e:
        logger.error(f"Contact submission error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error processing contact form"
        )

@router.get("/test-smtp")
async def test_smtp_connection():
    """Test endpoint to verify SMTP connection"""
    email = os.getenv("EMAIL_ADDRESS")
    password = os.getenv("EMAIL_PASSWORD")
    
    if not email or not password:
        raise HTTPException(
            status_code=400,
            detail="Email credentials not configured in .env file"
        )
    
    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.ehlo()
            server.starttls()
            server.login(email, password)
            return {"status": "success", "message": "SMTP authentication successful"}
    except smtplib.SMTPAuthenticationError as e:
        raise HTTPException(
            status_code=400,
            detail=f"SMTP authentication failed: {e}. Verify your app password."
        )
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"SMTP connection error: {str(e)}"
        )


