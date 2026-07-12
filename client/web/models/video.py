from datetime import datetime

from client.web.extensions import db


class Video(db.Model):

    __tablename__ = "videos"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    filename = db.Column(
        db.String(255),
        nullable=False
    )

    filesize = db.Column(
        db.BigInteger,
        nullable=False
    )

    filepath = db.Column(
        db.String(255),
        nullable=False
    )

    uploaded_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )