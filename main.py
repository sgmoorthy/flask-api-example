import os

from flask import Flask
from flask_restx import Api,Resource
from flask_compress import Compress
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from werkzeug.middleware.proxy_fix import ProxyFix

# Set working directory to project root
os.chdir(os.path.abspath(os.path.dirname(__file__)))

# If available, load environment variables from .env before rest of the package
if os.path.isfile(".env"):
    from dotenv import load_dotenv

    load_dotenv()

from controller import api


########################################################################################################################
# Setup / Configuration
########################################################################################################################

# Instantiate app
app = Flask(__name__)

VERSION = "v2"
api = Api(
    title="flask-api-microservice-example",
    description="for flask API for module",
    version=VERSION,
    prefix=f"/api/{VERSION}",
    doc="/" if os.getenv("FLASK_ENV") == "development" else False,
)

# define DB_CONN_STRING_ENV in .env file for the DB connections 


app.config["SQLALCHEMY_DATABASE_URI"] = os.environ["DB_CONN_STRING_ENV"]
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.wsgi_app = ProxyFix(app.wsgi_app)  # Fixes Swagger UI issues over HTTPS

# Add extensions
db = SQLAlchemy(app)
CORS(app)
api.init_app(app)
Compress(app)



########################################################################################################################
# Routing endpoints
########################################################################################################################


@api.route('/hello')
class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world'}




########################################################################################################################
# Run / Debug
########################################################################################################################

if __name__ == "__main__":
    if os.getenv("FLASK_ENV") == "development":
        app.run()
