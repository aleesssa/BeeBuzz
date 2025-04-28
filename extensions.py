from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# Initialize db in another file to overcome circular error
db = SQLAlchemy()
migrate = Migrate()