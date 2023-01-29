# Import flask and libs
from flask import Flask, render_template
# Import SQLAlchemy
from flask_sqlalchemy import SQLAlchemy

# Define the WSGI application object
from config import TEMPLATE_DIR, STATIC_DIR

app = Flask(__name__, static_folder=STATIC_DIR, template_folder=TEMPLATE_DIR)
app.config.from_object('config')
db = SQLAlchemy(app)


# HTTP 404
@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404


from app.controllers.dashboard_controller import dashboard_controller as dashboard_controller_module
from app.controllers.java_controller import java_controller as java_controller_module

# Register blueprint(s)
app.register_blueprint(dashboard_controller_module)
app.register_blueprint(java_controller_module)
