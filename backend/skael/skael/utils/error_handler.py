from flask import jsonify

from skael.utils.exceptions import BaseSkaelException


def register_error_handlers(_app):
    @_app.errorhandler(BaseSkaelException)
    def handle_all_errors(e):
        response = jsonify({'msg': e.msg})
        response.status_code = e.status_code
        return response
