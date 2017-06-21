import logging
import sqlalchemy
from sqlalchemy.dialects.postgresql import psycopg2

from sqlalchemy.exc import IntegrityError

from skael.models import db
from skael.utils.exceptions import DAOException


def exec_and_commit(f, obj, *, skip_commit=False):
    """
    A helper method to exec a sql statement and (optionally) commit.

    :param function f: The function to execute.
    :param object obj: The SQL object to create.
    :param bool skip_commit: Tells if we need to insert but not commit. Highly
    useful if an operation can fail midway through, so that we can rollback.
    :raises: DAOException
    :rtype: NoneType
    """
    try:
        f(obj)
        if not skip_commit:
            db.session.commit()
    except (sqlalchemy.exc.IntegrityError, IntegrityError) as e:
        logging.error(
            'Failed to commit object {0} due to exception {1}'.format(
                obj,
                e
            )
        )

        raise DAOException('Error processing request.')

