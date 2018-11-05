import datetime
import jwt

from sqlalchemy.sql import func
from flask import current_app

from src import bcrypt, db


class User(db.Model):

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(128), unique=True, nullable=False)
    email = db.Column(db.String(128), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=True)
    active = db.Column(db.Boolean(), default=True, nullable=False)
    created_date = db.Column(db.DateTime, default=func.now(), nullable=False)

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = bcrypt.generate_password_hash(
            password, current_app.config.get('BCRYPT_LOG_ROUNDS')).decode()

    def to_json(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'active': self.active
        }

    def encode_auth_token(self, user_id):
        """Generates the auth token.

        Payload metadata i.e. the JWT "claims":
        `exp`:      token expiration date
        `iat`:      (issued at) - token generation date
        `sub`:      the subject of the token e.g. the user whom it identifies
        """
        try:
            payload = {
                'exp':
                datetime.datetime.utcnow() + datetime.timedelta(
                    days=0,
                    seconds=3),
                    # days=current_app.config.get('TOKEN_EXPIRATION_DAYS'),
                    # seconds=current_app.config.get(
                    #     'TOKEN_EXPIRATION_SECONDS')),
                'iat':
                datetime.datetime.utcnow(),
                'sub':
                user_id
            }
            return jwt.encode(
                payload,
                current_app.config.get('SECRET_KEY'),
                algorithm='HS256')
        except Exception as ex:
            return ex

    # @staticmethod
    # def decode_auth_token(auth_token):
    #     """Decodes the auth token and returns the user_id

    #     Parameters
    #     ----------
    #         auth_token : str
    #             jwt auth_token

    #     Returns
    #     -------
    #     number | string
    #         user_id as a number or string
    #     """
    #     try:
    #         payload = jwt.decode(auth_token,
    #                              current_app.config.get('SECRET_KEY'))
    #         return payload['sub']
    #     except jwt.ExpiredSignatureError:
    #         return 'Signature expired. Please log in again.'
    #     except jwt.InvalidTokenError:
    #         return 'Invalid token. Please log in again.'

    @staticmethod
    def decode_auth_token(auth_token):
        """Decodes the auth token and returns the user_id

        Parameters
        ----------
            auth_token : str
                jwt auth_token

        Returns
        -------
        number | string
            user_id as a number or string
        """
        try:
            payload = jwt.decode(auth_token,
                                 current_app.config.get('SECRET_KEY'))
            return payload['sub']
        except jwt.ExpiredSignatureError:
            return 'Signature expired. Please log in again.'
        except jwt.InvalidTokenError:
            return 'Invalid token. Please log in again.'
