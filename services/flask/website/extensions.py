"""
@author:    Zuicie
@date:      December 09, 2024

Initialize extensions needed for create_app.
"""

from flask_bootstrap import Bootstrap5
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy


bootstrap = Bootstrap5()
db = SQLAlchemy()
migrate = Migrate()

