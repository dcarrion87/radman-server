from flask import Blueprint
from flask import current_app, redirect, request, url_for
from flask_security.decorators import roles_required,login_required
from flask_restful import Api, Resource, url_for
from radman.data.models import Study, Series, Instance, db
from sqlalchemy import exc

api_bp = Blueprint('api', __name__)
api = Api(api_bp)


class Studies(Resource):
    @login_required
    def get(self):
        return {
            'hello': 'studies'
            }

class Series(Resource):
    @login_required
    def get(self):
        return {
            'hello': 'series'
            }

class Instance(Resource):
    @login_required
    def get(self):
        return {
            'hello': 'instance'
            }

api.add_resource(Studies, '/studies')
api.add_resource(Series, '/series')
api.add_resource(Instance, '/instance')
