from flask import Flask
import logging

import skael.config

logger = logging.getLogger(__name__)

__all__ = ["app"]

app = Flask("skael")
app.config.from_object(skael.config)
