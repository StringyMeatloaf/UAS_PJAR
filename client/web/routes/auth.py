import secrets

from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    flash
)

from flask_login import (
    login_user,
    logout_user,
    login_required,
    current_user
)

from werkzeug.security import (
    generate_password_hash,
    check_password_hash
)

from client.web.extensions import db
from client.web.models.user import User
from client.web.services.email_service import send_verification_email


auth = Blueprint(
    "auth",
    __name__
)


# =====================================================
# REGISTER
# =====================================================
@auth.route("/register", methods=["GET", "POST"])
def register():

    if current_user.is_authenticated:
        return redirect(url_for("dashboard.index"))

    if request.method == "POST":

        username = request.form.get("username", "").strip()
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")

        if not username or not email or not password:

            flash(
                "Semua field harus diisi.",
                "danger"
            )

            return redirect(
                url_for("auth.register")
            )

        existing_user = User.query.filter(
            (User.username == username) |
            (User.email == email)
        ).first()

        if existing_user:

            flash(
                "Username atau Email sudah digunakan.",
                "danger"
            )

            return redirect(
                url_for("auth.register")
            )

        verification_token = secrets.token_urlsafe(32)

        new_user = User(

            username=username,

            email=email,

            password=generate_password_hash(password),

            is_verified=False,

            verification_token=verification_token

        )

        db.session.add(new_user)
        db.session.commit()

        send_verification_email(new_user)

        flash(

            "Registrasi berhasil. Silakan cek email untuk verifikasi akun.",

            "success"

        )

        return redirect(
            url_for("auth.login")
        )

    return render_template(
        "register.html"
    )


# =====================================================
# VERIFY EMAIL
# =====================================================
@auth.route("/verify/<token>")
def verify(token):

    user = User.query.filter_by(
        verification_token=token
    ).first()

    if user is None:

        flash(
            "Link verifikasi tidak valid.",
            "danger"
        )

        return redirect(
            url_for("auth.login")
        )

    user.is_verified = True
    user.verification_token = None

    db.session.commit()

    flash(
        "Email berhasil diverifikasi.",
        "success"
    )

    return redirect(
        url_for("auth.login")
    )


# =====================================================
# LOGIN
# =====================================================
@auth.route("/login", methods=["GET", "POST"])
def login():

    if current_user.is_authenticated:
        return redirect(url_for("dashboard.index"))

    if request.method == "POST":

        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")

        user = User.query.filter_by(
            email=email
        ).first()

        if user is None:

            flash(
                "Email tidak ditemukan.",
                "danger"
            )

            return redirect(
                url_for("auth.login")
            )

        if not user.is_verified:

            flash(
                "Silakan verifikasi email terlebih dahulu.",
                "warning"
            )

            return redirect(
                url_for("auth.login")
            )

        if not check_password_hash(
            user.password,
            password
        ):

            flash(
                "Password salah.",
                "danger"
            )

            return redirect(
                url_for("auth.login")
            )

        login_user(user)

        flash(
            f"Selamat datang, {user.username}.",
            "success"
        )

        return redirect(
            url_for("dashboard.index")
        )

    return render_template(
        "login.html"
    )


# =====================================================
# LOGOUT
# =====================================================
@auth.route("/logout")
@login_required
def logout():

    logout_user()

    flash(
        "Berhasil logout.",
        "success"
    )

    return redirect(
        url_for("auth.login")
    )