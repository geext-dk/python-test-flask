from flask import Blueprint

async_sample_data = Blueprint('async_sample_data', __name__)

from . import views