import os
HOST = os.environ.get("HOST", "0.0.0.0")
PORT = os.environ.get("PORT", 5000)
PORT = int(PORT)

CURRENT_VERSION_API = "v1"

DEBUG = os.getenv("DEBUG", None)
if DEBUG is None:
    DEBUG = False
else:
    DEBUG = True

MONGO = {
    "user": os.environ.get('MONGODB_USERNAME', "siwp2005"),
    "pw": os.environ.get('MONGODB_PASSWORD', "siwp2005-password"),
    "host": os.environ.get('MONGODB_HOSTNAME', "0.0.0.0"),
    "port": os.environ.get('MONGODB_PORT', "27017"),
    "db": os.environ.get("MONGODB_DATABASE", "siwp2005-final-project-db"),
}
DB_URI = (
    "mongodb://%(user)s:%(pw)s@%(host)s:%(port)s/%(db)s?authSource=admin" % MONGO
)

SECRET_KEY= os.environ.get("SECRET_KEY")
if SECRET_KEY is None:
    SECRET_KEY = os.urandom(24)

LOG_FORMAT = "[%(asctime)s] {%(pathname)s:%(lineno)d} \
    %(levelname)s in %(module)s: %(message)s"
LOG_CONFIG = {
    "version": 1,
    "formatters": {
        "default": {
            "format": LOG_FORMAT,
        }
    },
    "handlers": {
        "wsgi": {
            "class": "logging.StreamHandler",
            "stream": "ext://flask.logging.wsgi_errors_stream",
            "formatter": "default",
        }
    },
    "root": {"level": "INFO", "handlers": ["wsgi"]},
}

USERNAME_ADMIN=os.environ.get("USERNAME_ADMIN", "admin")
PASSWORD_ADMIN=os.environ.get("PASSWORD_ADMIN", "admin")