from dotenv import load_dotenv
import os


load_dotenv()


# JWT configuration
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM", "HS256")

# Database configuration
DATABASE_URL = os.getenv("DATABASE_URL")

# Other common values
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 15))
REFRESH_TOKEN_EXPIRE_DAYSF = int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS", 7))