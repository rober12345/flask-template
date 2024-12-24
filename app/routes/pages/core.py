from flask import render_template, Blueprint, request, redirect, url_for
import requests

core_bp = Blueprint('core', __name__)

@core_bp.route('/')
def home_route():
    return render_template('pages/home.html')

@core_bp.route('/predict')
def predict_route():
    try:
        response = requests.get('http://127.0.0.1:5000/api/predict/plot')
        if response.status_code == 200:
            return render_template('pages/predict.html')
        else:
            return render_template('pages/predict.html', error="Failed to generate plot.")
    except Exception as e:
        return render_template('pages/predict.html', error=f"Error: {e}")





# Flask modules
from flask import Blueprint, render_template

core_bp = Blueprint("core", __name__, url_prefix="/")


@core_bp.route("/")
def home_route():
    return render_template("templates/pages/home.html")
