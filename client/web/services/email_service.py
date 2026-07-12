from flask_mail import Message
from flask import current_app
from client.web.extensions import mail


def send_verification_email(user):

    verify_link = (
        f"{current_app.config['BASE_URL']}"
        f"/verify/{user.verification_token}"
    )

    html = f"""
    <h2>MediaShare</h2>

    <p>Halo <b>{user.username}</b>,</p>

    <p>Terima kasih telah mendaftar di MediaShare.</p>

    <p>
        Klik tombol di bawah untuk mengaktifkan akun Anda.
    </p>

    <p>
        <a href="{verify_link}"
        style="
            background:#0d6efd;
            color:white;
            padding:12px 20px;
            text-decoration:none;
            border-radius:6px;
            display:inline-block;
        ">
            Verify My Account
        </a>
    </p>

    <hr>

    <p>
        Jika tombol tidak dapat diklik,
        gunakan link berikut:
    </p>

    <p>{verify_link}</p>

    <br>

    <small>MediaShare Team</small>
    """

    msg = Message(
        subject="Verify Your MediaShare Account",
        recipients=[user.email],
        html=html
    )

    mail.send(msg)