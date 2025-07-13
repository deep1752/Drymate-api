from mangum import Mangum
from api.main import app

# 👇 ASGI to Lambda adapter
handler = Mangum(app)
