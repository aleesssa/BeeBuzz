from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_mail import Mail
from flask_login import LoginManager

# Initialize db in another file to overcome circular error
db = SQLAlchemy()
migrate = Migrate()
mail = Mail()
login_manager = LoginManager()