from flask import Blueprint
from flask_restful import Api
from resource.user import RegisterAPI, LoginAPI, UserManagementAPI, UserManagementListAPI

authz_blueprint = Blueprint("user_api", __name__)
authz_blueprint_api = Api(authz_blueprint)

authz_blueprint_api.add_resource(RegisterAPI, "/user")
authz_blueprint_api.add_resource(LoginAPI, "/login")
authz_blueprint_api.add_resource(UserManagementListAPI, "/manage/user")
authz_blueprint_api.add_resource(UserManagementAPI, "/manage/user/<string:user_id>")
