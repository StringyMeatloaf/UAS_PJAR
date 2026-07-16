from flask import Blueprint, Response
from flask_login import login_required
from client.web.services.udp_service import stream_generator

stream = Blueprint(
    "stream",
    __name__,
    url_prefix="/stream"
)

@stream.route("/video_feed/<filename>")
@login_required
def video_feed(filename):
    """
    Route ini menyalurkan raw video byte stream yang diambil dari UDP server.
    Mimetype video/mp4 memaksa browser menggunakan HTML5 video player native
    sehingga tombol Play, Pause, Slider, dan AUDIO otomatis berfungsi 100%!
    """
    return Response(
        stream_generator(filename),
        mimetype="video/mp4",
        headers={"Accept-Ranges": "bytes"}
    )