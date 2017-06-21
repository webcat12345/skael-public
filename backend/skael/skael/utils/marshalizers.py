from marshmallow import Schema, fields
from marshmallow import post_dump


class _BaseSchema(Schema):
    public_id = fields.String()

    @post_dump
    def replace_with_none(self, data):
        """
        Handles taking a marshalled object and replacing any missing fields
        with a `None`, so that callers can serialize to null.

        :param dict data: The marshalled data.
        :rtype: dict
        :return: A marshalled object with missing values converted to `None`.
        """
        for k in self.fields.keys():
            if not data.get(k, False):
                data[k] = None

        return data


class UserSanitizedMarshal(_BaseSchema):
    """
    The sanitized version of `UserMarshal`. This contains data we'd be all
    right with any caller seeing.

    Information ought to be added here on a need-to-have basis.
    """
    username = fields.String()
    is_validated = fields.String()


class UserMarshal(UserSanitizedMarshal):
    """
    An extension of `UserSanitizedModel`. Is returned whenever the caller is
    authorized for the requested user. Some calls may potentially return this
    info as being tacked on. This class holds information we may not want to
    leak to some users, but the user itself ought to be able to see it.

    For instance, we may not want to return emails to any user, but if the
    user himself requests his own data, we should return it.
    """
    email = fields.String()
