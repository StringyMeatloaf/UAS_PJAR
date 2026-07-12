# client/web/routes/stream.py
import os
from flask import Blueprint, Response, stream_with_context
from flask_login import login_required
from shared.constants import UPLOAD_FOLDER

stream = Blueprint(
    "stream",
    __name__,
    url_prefix="/stream"
)

@stream.route("/video_feed/<filename>")
@login_required
def video_feed(filename):
    """
    Route ini mengalirkan video secara parsial (chunk) menggunakan HTTP biasa.
    Browser secara otomatis membaca audio dan video bersamaan, serta 
    mendukung kendali Play/Pause secara native tanpa socket UDP kustom.
    """
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    
    if not os.path.exists(filepath):
        return "Video tidak ditemukan", 404

    def generate():
        with open(filepath, "rb") as video_file:
            # Baca file per 4096 bytes (4KB) dan langsung kirim ke browser
            while True:
                chunk = video_file.read(4096)
                if not chunk:
                    break
                yield chunk

    # Menggunakan mimetype video/mp4 (atau sesuaikan dengan format video Anda)
    return Response(
        stream_with_context(generate()), 
        mimetype="video/mp4",
        headers={"Accept-Ranges": "bytes"}
    )