#!/usr/bin/python3
from models.amenity import Amenity
from models.city import City
from models import storage
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
from flask import Blueprint
app_views = Blueprint("app_views", __name__, url_prefix="/api/v1")
from api.v1.views.index import *
from api.v1.views.states import *
