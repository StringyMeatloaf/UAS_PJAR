from flask_login import LoginManager
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy


# =====================================================
# Database
# =====================================================
db = SQLAlchemy()


# =====================================================
# Authentication
# =====================================================
login_manager = LoginManager()

login_manager.login_view = "auth.login"

login_manager.login_message = (
    "Silakan login terlebih dahulu."
)

login_manager.login_message_category = "warning"


# =====================================================
# Email
# =====================================================
mail = Mail()