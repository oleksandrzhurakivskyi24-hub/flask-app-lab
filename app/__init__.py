import os
from flask import Flask

app = Flask(__name__)

app.config["SECRET_KEY"] = os.environ.get(
    "SECRET_KEY",
    os.urandom(24).hex(),
)

from app import views
from app.users import user_bp
from app.products import products_bp

app.register_blueprint(user_bp)
app.register_blueprint(products_bp)