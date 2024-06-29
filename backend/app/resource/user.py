from flask import request
from datetime import timedelta
from flask_restful import Resource
from mongoengine.errors import FieldDoesNotExist, NotUniqueError, DoesNotExist

from marshmallow.exceptions import ValidationError
from helper.schema import UserSchema, LoginSchema
from model.user import User

from flask_jwt_extended import create_access_token
from flask_jwt_extended import jwt_required
from helper.rbac import user_level_required, USER_LEVELS  # Import the custom decorator and user levels

from flask import current_app as app


# class RegisterAPI(Resource):
#     def post(self):
#         try:
#             data = request.get_json()
#             result = UserSchema().load(data)
#             user = User(**result)
#             user.hash_password()
#             user.save()
#             return UserSchema().dump(user), 200
#         except ValidationError as e:
#             return {'errors': e.messages}, 400
#         except FieldDoesNotExist:
#             return {'error': 'Request is missing required fields'}, 400
#         except NotUniqueError:
#             return {'error': 'username address already exists'}, 400

# class LoginAPI(Resource):
#     def post(self):
#         try:
#             payload = LoginSchema().load(request.get_json())
#             user = User.objects.get_or_404(username=payload['username'])
#             authorized = user.check_password(payload['password'])
#             if not authorized:
#                 return {'error': 'Email or password invalid'}, 401
#             expires = timedelta(days=7)
#             access_token = create_access_token(identity=str(user.id), expires_delta=expires)
#             return {'token': access_token}, 200

#         except Exception as e:
#             app.logger.error("Error: {}".format(e))
#             return {'message': "Server error"}, 500
        
class LoginAPI(Resource):
    def post(self):
        try:
            payload = LoginSchema().load(request.get_json())
            user = User.objects.get(username=payload['username'])
            if not user.check_password(payload['password']):
                return {'error': 'Invalid username or password'}, 401
            
            # Create access token with custom claims
            expires = timedelta(days=7)
            additional_claims = {"user_level": user.userlevel}
            access_token = create_access_token(identity=str(user.id), expires_delta=expires, additional_claims=additional_claims)
            return {'token': access_token}, 200
        except ValidationError as e:
            return {'errors': e.messages}, 400
        except DoesNotExist:
            return {'error': 'Invalid username or password'}, 401
        except Exception as e:
            return {'message': str(e)}, 500
        
class RegisterAPI(Resource):
    def post(self):
        try:
            data = request.get_json()
            result = UserSchema().load(data)
            user = User(**result)
            user.hash_password()
            user.save()
            return UserSchema().dump(user), 200
        except ValidationError as e:
            return {'errors': e.messages}, 400
        except FieldDoesNotExist:
            return {'error': 'Request is missing required fields'}, 400
        except NotUniqueError:
            return {'error': 'username address already exists'}, 400

class UserManagementListAPI(Resource):
    @jwt_required()
    @user_level_required(USER_LEVELS["super_admin"]) 
    def post(self):
        data = request.get_json()
        user = User(**data)
        user.hash_password()
        user.save()
        return UserSchema().dump(user), 200

    @jwt_required()
    @user_level_required(USER_LEVELS["super_admin"])
    def get(self):
        users = User.objects
        return UserSchema(many=True).dump(users), 200

class UserManagementAPI(Resource):
    @jwt_required()
    @user_level_required(USER_LEVELS["super_admin"])  
    def get(self, user_id):
        user = User.objects.get(id=user_id)
        return UserSchema().dump(user), 200

    @jwt_required()
    @user_level_required(USER_LEVELS["super_admin"]) 
    def put(self, user_id):
        data = request.get_json()
        user = User.objects.get(id=user_id)
        user.update(**data)
        return UserSchema().dump(user), 200

    @jwt_required()
    @user_level_required(USER_LEVELS["super_admin"]) 
    def delete(self, user_id):
        user = User.objects.get(id=user_id)
        user.delete()
        msg = {"message": f"User {user_id} deleted"}
        return msg, 200
