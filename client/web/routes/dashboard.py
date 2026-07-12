from flask import Blueprint, render_template
from flask_login import login_required, current_user
from client.web.models.video import Video

# 1. Ganti nama variabel dari 'dashboard' menjadi 'dashboard_bp'
dashboard_bp = Blueprint(
    "dashboard",
    __name__
)


# 2. Ganti dekoratornya menggunakan 'dashboard_bp'
@dashboard_bp.route("/dashboard")
@login_required
def index():

    videos = Video.query.filter_by(
        user_id=current_user.id
    ).all()

    return render_template(
        "dashboard.html",
        user=current_user,
        videos=videos
    )