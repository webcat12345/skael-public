import codecs
import logging
import sys

from skael.app import app
import skael.views

logging.basicConfig(level=logging.DEBUG, format="[%(asctime)s] %(levelname)-8s [%(name)s] %(message)s",
                    stream=(codecs.getwriter("utf-8")(sys.stdout.buffer, "replace")
                            if hasattr(sys.stdout, "buffer")
                            else None))
