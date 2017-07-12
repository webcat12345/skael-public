import logging
import requests
from requests.exceptions import Timeout, RequestException

from http import HTTPStatus
from flask import current_app

from skael.utils.exceptions import IntegrationException


class MailgunIntegration(object):
    """
    Wraps the mailgun API in skael-specific convenient ways.
    """

    @staticmethod
    def send_email(email_from, email_to, subject, body):
        """
        Handles sending an email through the mailgun API.

        :param str email_from: The origin email.
        :param str email_to: The destination email.
        :param str subject: Subject line for the email.
        :param str body: The contents of the email.
        :rtype: requests.Response
        :return: The response object
        """
        try:
            requests.Response()
            response = requests.post(
                'https://api.mailgun.net/v3/{0}/messages'.format(
                    current_app.config['MAILGUN_ORIGIN_DOMAIN']
                ),
                auth=('api', current_app.config['MAILGUN_API_KEY']),
                data={
                    'from': email_from,
                    'to': email_to,
                    'subject': subject,
                    'html': body
                }
            )

            if response.status_code == HTTPStatus.OK:
                return response.json
        except (Timeout, RequestException) as e:
            logging.error(
                'Failed to send email through mailgun: {0}'.format(
                    e
                )
            )

        raise IntegrationException(
            'Sending email failed.'
        )