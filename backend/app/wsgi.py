import multiprocessing
import os
import gunicorn.app.base
from app import create_app
import config
from mongoengine import Document, connect, fields
from flask_bcrypt import generate_password_hash
from os import environ
import logging
# Set up logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# init admin user
def create_default_user():
     mongo_data = config.MONGO
     connect(
        username=mongo_data['user'],
        password=mongo_data['pw'],
        host=config.DB_URI
     )

     class User(Document):
        username = fields.StringField(required=True, unique=True)
        password = fields.StringField(required=True, min_length=6)
        userlevel = fields.IntField(default=0)
        description = fields.StringField(requuired=False)

          
        def hash_password(self):
            self.password = generate_password_hash(self.password).decode('utf8')


     # Check if an admin user already exists
     existing_admin = User.objects(username=environ.get('USERNAME_ADMIN', "siwp_admin")).first()
     if existing_admin:
        logger.info("Admin user already exists. Skipping creation.")
        return None
     else:
        # Create the admin user only if it doesn't already exist
        data = User(
            username=environ.get('USERNAME_ADMIN', "siwp_admin"),
            password=environ.get('PASSWORD_ADMIN', "siwp_password"),
        )
        data.hash_password()
        data.save()
        return None



def number_of_workers():
    return (multiprocessing.cpu_count() * 2) + 1


class StandaloneApplication(gunicorn.app.base.BaseApplication):
    def __init__(self, app, options=None):
        self.options = options or {}
        self.application = app
        super().__init__()

    def load_config(self):
        config = {key: value for key, value in self.options.items()
                  if key in self.cfg.settings and value is not None}
        for key, value in config.items():
            self.cfg.set(key.lower(), value)

    def load(self):
        return self.application


if __name__ == '__main__':
    PORT = os.environ.get("PORT", 5000)
    # n_worker = number_of_workers()
    n_worker = 2
    options = {
        'bind': '%s:%s' % ('0.0.0.0', PORT),
        'workers': 2,
    }
    
    create_default_user()
    app = create_app()
    StandaloneApplication(app, options).run()
