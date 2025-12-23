from flask import Blueprint

# Define Blueprints
auth_bp = Blueprint('auth', __name__)
admin_bp = Blueprint('admin', __name__)
dosen_bp = Blueprint('dosen', __name__)
mahasiswa_bp = Blueprint('mahasiswa', __name__)
general_bp = Blueprint('general', __name__)

# Import routes to register them with blueprints
from . import auth, admin, dosen, mahasiswa, general
