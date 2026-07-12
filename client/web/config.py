import os
from pathlib import Path
from dotenv import load_dotenv

# Root project (UAS_PJAR)
BASE_DIR = Path(__file__).resolve().parents[2]

# Load .env dari root project
load_dotenv(BASE_DIR / ".env")


class Config:

    # =====================================================
    # Flask
    # =====================================================
    SECRET_KEY = os.getenv("SECRET_KEY")


    # =====================================================
    # Database
    # =====================================================
    SQLALCHEMY_DATABASE_URI = (
        f"mysql+pymysql://{os.getenv('DB_USER')}:"
        f"{os.getenv('DB_PASSWORD')}@"
        f"{os.getenv('DB_HOST')}/"
        f"{os.getenv('DB_NAME')}"
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False


    # =====================================================
    # Mail
    # =====================================================
    MAIL_SERVER = os.getenv("MAIL_SERVER")

    MAIL_PORT = int(
        os.getenv("MAIL_PORT", 587)
    )

    MAIL_USE_TLS = True

    MAIL_USE_SSL = False

    MAIL_USERNAME = os.getenv("MAIL_USERNAME")

    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")

    MAIL_DEFAULT_SENDER = MAIL_USERNAME


    # =====================================================
    # Application
    # =====================================================
    BASE_URL = os.getenv("BASE_URL")


    # =====================================================
    # Upload Folder
    # =====================================================
    TEMP_UPLOAD_FOLDER = os.path.join(
        "client",
        "web",
        "temp_uploads"
    )


    # =====================================================
    # TCP Server
    # =====================================================
    TCP_SERVER_IP = os.getenv(
        "TCP_SERVER_IP",
        "127.0.0.1"
    )

    TCP_SERVER_PORT = int(
        os.getenv(
            "TCP_SERVER_PORT",
            5001
        )
    )


    # =====================================================
    # UDP Server
    # =====================================================
    UDP_SERVER_IP = os.getenv(
        "UDP_SERVER_IP",
        "127.0.0.1"
    )

    UDP_SERVER_PORT = int(
        os.getenv(
            "UDP_SERVER_PORT",
            5002
        )
    )


    # =====================================================
    # Upload
    # =====================================================
    MAX_CONTENT_LENGTH = 500 * 1024 * 1024
