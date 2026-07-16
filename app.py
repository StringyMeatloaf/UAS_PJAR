from flask import (
    Flask,
    redirect,
    url_for
)

from flask_login import current_user

# =====================================================
# Configuration
# =====================================================
from client.web.config import Config

# =====================================================
# Extensions
# =====================================================
from client.web.extensions import (
    db,
    login_manager,
    mail
)

# =====================================================
# Models
# =====================================================
from client.web.models.user import User

# =====================================================
# Blueprints (Disesuaikan namanya agar tidak bentrok dengan fungsi/modul)
# =====================================================
from client.web.routes.auth import auth as auth_bp
from client.web.routes.dashboard import dashboard_bp  # <-- Diubah dari 'dashboard' menjadi 'dashboard_bp'
from client.web.routes.upload import upload as upload_bp
from client.web.routes.stream import stream as stream_bp


# =====================================================
# Flask Application
# =====================================================

app = Flask(
    __name__,
    template_folder="client/web/templates",
    static_folder="client/web/static"
)
app.config.from_object(Config)

# =====================================================
# Initialize Extensions
# =====================================================
db.init_app(app)
mail.init_app(app)
login_manager.init_app(app)


# =====================================================
# Register Blueprints
# =====================================================
app.register_blueprint(auth_bp)
app.register_blueprint(dashboard_bp)  # <-- Mendaftarkan variabel blueprint yang benar
app.register_blueprint(upload_bp)
app.register_blueprint(stream_bp)

# =====================================================
# Flask-Login
# =====================================================
@login_manager.user_loader
def load_user(user_id):
    return db.session.get(
        User,
        int(user_id)
    )


# =====================================================
# Home
# =====================================================
@app.route("/")
def home():
    if current_user.is_authenticated:
        # Jika nama registrasi blueprint dashboard Anda adalah "dashboard",
        # dan nama fungsi di dalamnya adalah "index", maka setingan ini sudah benar.
        return redirect(
            url_for("dashboard.index")
        )

    return redirect(
        url_for("auth.login")
    )


# =====================================================
# Run Application
# =====================================================
# Di dalam app.py (Windows)
if __name__ == "__main__":
    app.run(
        host="0.0.0.0",  # <--- WAJIB DITAMBAHKAN agar bisa diakses oleh VM
        port=5000,       # Pastikan portnya sesuai (5000)
        debug=True
    )