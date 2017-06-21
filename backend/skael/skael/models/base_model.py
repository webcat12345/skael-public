from datetime import datetime
import uuid

from skael.models import db


class BaseTable(db.Model):
    """Base table which all tables should inherit from."""

    __abstract__ = True

    id = db.Column(
        db.Integer,
        autoincrement=True,
        primary_key=True,
        nullable=False,
        unique=True
    )

    public_id = db.Column(
        db.String(36),
        unique=True,
        nullable=False,
        index=True
    )

    created_at = db.Column(
        db.TIMESTAMP,
        nullable=False,
        default=datetime.utcnow()
    )

    def __init__(self):
        self.public_id = str(uuid.uuid4())


