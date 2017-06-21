from http import HTTPStatus


class BaseSkaelException(Exception):
    """
    The base exception class used for all other base exceptions.

    Exceptions are typically broken out into a layered level. I.e., a request
    comes in: first it hits the endpoint, then it might hit an interface, and
    then an integration.
    """
    __abstract__ = True

    def __init__(self, msg, status_code=HTTPStatus.BAD_REQUEST):
        self.msg = msg
        self.status_code = status_code


class FacadeException(BaseSkaelException):
    """
    An exception raised in facades.
    """
    pass


class DAOException(BaseSkaelException):
    """
    An exception raised in daos.
    """
    pass


class EndpointException(BaseSkaelException):
    """
    An exception raised in endpoints.
    """
    pass


class IntegrationException(BaseSkaelException):
    """
    An exception raised in integration classes. I.e., mailgun.
    """
    pass
