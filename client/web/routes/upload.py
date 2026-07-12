import os

from flask import (
    Blueprint,
    current_app,
    request,
    redirect,
    url_for,
    flash
)

from flask_login import (
    login_required,
    current_user
)

from client.web.extensions import db
from client.web.models.video import Video
from client.web.services.tcp_service import upload_to_server


upload = Blueprint(
    "upload",
    __name__
)


# =====================================================
# Upload Video
# =====================================================
@upload.route("/upload", methods=["POST"])
@login_required
def upload_file():

    # -------------------------------------------------
    # Check File
    # -------------------------------------------------
    if "video" not in request.files:

        flash(
            "Tidak ada file yang dipilih.",
            "danger"
        )

        return redirect(
            url_for("dashboard.index")
        )

    file = request.files["video"]

    if file.filename == "":

        flash(
            "Silakan pilih file video.",
            "warning"
        )

        return redirect(
            url_for("dashboard.index")
        )

    # -------------------------------------------------
    # Temporary Folder
    # -------------------------------------------------
    temp_folder = current_app.config[
        "TEMP_UPLOAD_FOLDER"
    ]

    os.makedirs(
        temp_folder,
        exist_ok=True
    )

    temp_path = os.path.join(
        temp_folder,
        file.filename
    )

    # -------------------------------------------------
    # Save Temporary File
    # -------------------------------------------------
    file.save(temp_path)

    filesize = os.path.getsize(temp_path)

    # -------------------------------------------------
    # Upload via TCP
    # -------------------------------------------------
    success = upload_to_server(temp_path)

    # -------------------------------------------------
    # Upload Success
    # -------------------------------------------------
    if success:

        video = Video(

            filename=file.filename,

            filesize=filesize,

            filepath=file.filename,

            user_id=current_user.id

        )

        db.session.add(video)

        db.session.commit()

        os.remove(temp_path)

        flash(
            "Video berhasil diupload.",
            "success"
        )

    # -------------------------------------------------
    # Upload Failed
    # -------------------------------------------------
    else:

        if os.path.exists(temp_path):

            os.remove(temp_path)

        flash(
            "Upload video gagal.",
            "danger"
        )

    return redirect(
        url_for("dashboard.index")
    )