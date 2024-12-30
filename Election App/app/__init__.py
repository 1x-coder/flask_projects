from flask import Flask
from app.routes import main

app = Flask(
    __name__,
    template_folder='templates',
    static_folder='static'
)

app.register_blueprint(main)