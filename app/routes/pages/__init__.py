"""
# Flask modules
# from flask import Blueprint

# Blueprint modules
#from .core import core_bp

#pages_bp = Blueprint("pages", __name__, url_prefix="/")


#pages_bp.register_blueprint(core_bp)
"""

from flask import Blueprint, render_template

# Define the main blueprint for pages
pages_bp = Blueprint("pages", __name__, template_folder='../../templates')

# Define the home route directly here
@pages_bp.route('/')
def home():
    return render_template('pages/home.html')





