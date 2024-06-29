from flask import request, jsonify, abort, Response
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import current_app as app
from marshmallow.exceptions import ValidationError
from mongoengine.errors import NotUniqueError
from werkzeug.exceptions import UnprocessableEntity, Conflict

import helper.validator as validator
from model.course import Course, User, Bulletin, Attendance, CalendarEvent, Billing, Score
from helper.schema import CourseSchema, BulletinSchema, AttendanceSchema, CalendarEventSchema, BillingSchema, ScoreSchema

class CourseListAPI(Resource):
    @jwt_required()
    def get(self):
        courses = Course.objects()
        serialized_payload = CourseSchema(many=True).dump(courses)
        return serialized_payload, 200
    
    @jwt_required()
    def post(self):
        serialized_payload = validator.add_course()
        course = Course(**serialized_payload)
        course.save()
        serialized_payload = CourseSchema().dump(course)
        return serialized_payload, 200

class CourseAPI(Resource):
    @jwt_required()
    def get(self, course_id):
        course = Course.objects.get(id=course_id)
        serialized_payload = CourseSchema().dump(course)
        return serialized_payload, 200
    
    @jwt_required()
    def put(self, course_id):
        course = Course.objects.get(id=course_id)
        user = User.objects.get(id=get_jwt_identity())
        serialized_payload = validator.add_course()
        for key, value in serialized_payload.items():
            setattr(course, key, value)
        course.save()
        serialized_payload = CourseSchema().dump(course)
        return serialized_payload, 200
    
    @jwt_required()
    def delete(self, course_id):        
        course = Course.objects.get(id=course_id)
        course.delete()
        app.logger.info("Course with id %s deleted", course_id)
        msg={"message": "Course: {} deleted".format(course_id)}
        return msg, 200

class ScoreAPI(Resource):
    @jwt_required()
    def get(self, score_id=None):
        if score_id:
            score = Score.objects.get(id=score_id)
            serialized_payload = ScoreSchema().dump(score)
            return serialized_payload, 200
        else:
            user_id = get_jwt_identity()
            scores = Score.objects(user=user_id)
            serialized_payload = ScoreSchema(many=True).dump(scores)
            return serialized_payload, 200

    @jwt_required()
    def post(self):
        try:
            serialized_payload = ScoreSchema().load(request.json)
            user_id = get_jwt_identity()
            user = User.objects.get(id=user_id)
            course = Course.objects.get(id=serialized_payload['course']['id'])
            score = Score(
                user=user,
                course=course,
                score=serialized_payload['score'],
                date=datetime.utcnow()
            )
            score.save()
            serialized_payload = ScoreSchema().dump(score)
            return serialized_payload, 201

        except ValidationError as e:
            app.logger.error(f"Validation error: {e.messages}")
            abort(400, str(e.messages))

        except (User.DoesNotExist, Course.DoesNotExist) as e:
            app.logger.error(f"User or Course not found: {str(e)}")
            abort(404, "User or Course not found.")

        except NotUniqueError:
            app.logger.error("Duplicate score entry.")
            abort(409, "Duplicate score entry.")

        except Exception as e:
            app.logger.error(f"Unexpected error: {str(e)}")
            abort(500, "An unexpected error occurred.")

class ScoreListAPI(Resource):
    @jwt_required()
    def get(self):
        try:
            user_id = get_jwt_identity()
            scores = Score.objects(user=user_id)
            serialized_payload = ScoreSchema(many=True).dump(scores)
            return serialized_payload, 200
        
        except User.DoesNotExist:
            app.logger.error(f"User with id {user_id} not found.")
            abort(404, "User not found.")
        
        except Exception as e:
            app.logger.error(f"Unexpected error: {str(e)}")
            abort(500, "An unexpected error occurred.")
              
class BulletinListAPI(Resource):
    @jwt_required()
    def get(self):
        bulletin = Bulletin.objects()
        serialized_payload = BulletinSchema(many=True).dump(bulletin)
        return serialized_payload, 200

class BulletinAPI(Resource):
    @jwt_required()
    def get(self, bulletin_id):
        app.logger.info("bulletin id: {}".format(bulletin_id))
        bulletin = Bulletin.objects.get(id=bulletin_id)
        serialized_payload = BulletinSchema().dump(bulletin)
        return serialized_payload, 200
    
class AttendanceAPI(Resource):
    @jwt_required()
    def post(self, course_id):
        try:
            serialized_payload = AttendanceSchema().load(request.json)
            user_id = get_jwt_identity()
            user = User.objects.get(id=user_id)
            course = Course.objects.get(id=course_id)
            
            if course.user.id != user.id:
                raise UnprocessableEntity("You do not have permission to add attendance for this course.")
            
            existing_attendance = Attendance.objects(
                user=user,
                course=course,
                date=serialized_payload['date']
            ).first()
            
            if existing_attendance:
                raise Conflict("Attendance entry already exists for this user, course, and date.")
            
            attendance = Attendance(
                user=user,
                course=course,
                date=serialized_payload['date'],
                status=serialized_payload['status']
            )
            attendance.save()
            
            serialized_payload = AttendanceSchema().dump(attendance)
            return serialized_payload, 200
        
        except ValidationError as e:
            app.logger.error(f"Validation error: {e.messages}")
            abort(400, str(e.messages))
        
        except (User.DoesNotExist, Course.DoesNotExist) as e:
            app.logger.error(f"User or Course not found: {str(e)}")
            abort(404, "User or Course not found.")
        
        except NotUniqueError:
            app.logger.error("Duplicate attendance entry.")
            abort(409, "Duplicate attendance entry.")
        
        except UnprocessableEntity as e:
            app.logger.error(f"Unprocessable Entity: {str(e)}")
            abort(422, str(e))
        
        except Exception as e:
            app.logger.error(f"Unexpected error: {str(e)}")
            abort(500, "An unexpected error occurred.")

    @jwt_required()
    def get(self, course_id):
        try:
            user_id = get_jwt_identity()
            user = User.objects.get(id=user_id)
            course = Course.objects.get(id=course_id)
            
            if course.user.id != user.id:
                raise UnprocessableEntity("You do not have permission to view attendance for this course.")
            
            attendances = Attendance.objects(course=course)
            serialized_payload = AttendanceSchema(many=True).dump(attendances)
            
            return serialized_payload, 200
        
        except (User.DoesNotExist, Course.DoesNotExist) as e:
            app.logger.error(f"User or Course not found: {str(e)}")
            abort(404, "User or Course not found.")
        
        except Exception as e:
            app.logger.error(f"Unexpected error: {str(e)}")
            abort(500, "An unexpected error occurred.")

class CalendarAPI(Resource):
    @jwt_required()
    def post(self):
        try:
            serialized_payload = CalendarEventSchema().load(request.json)
            user_id = get_jwt_identity()
            user = User.objects.get(id=user_id)
            
            # Create a new calendar event
            event = CalendarEvent(
                user=user,
                title=serialized_payload['title'],
                description=serialized_payload.get('description'),
                start_time=serialized_payload['start_time'],
                end_time=serialized_payload['end_time']
            )
            event.save()
            
            serialized_event = CalendarEventSchema().dump(event)
            return serialized_event, 201
        
        except ValidationError as e:
            app.logger.error(f"Validation error: {e.messages}")
            abort(400, str(e.messages))
        
        except DoesNotExist:
            app.logger.error(f"User with id {user_id} not found.")
            abort(404, "User not found.")
        
        except Exception as e:
            app.logger.error(f"Unexpected error: {str(e)}")
            abort(500, "An unexpected error occurred.")

    @jwt_required()
    def get(self):
        try:
            user_id = get_jwt_identity()
            user = User.objects.get(id=user_id)
            
            # Fetch all calendar events for the user
            events = CalendarEvent.objects(user=user)
            serialized_events = CalendarEventSchema(many=True).dump(events)
            
            return serialized_events, 200
        
        except DoesNotExist:
            app.logger.error(f"User with id {user_id} not found.")
            abort(404, "User not found.")
        
        except Exception as e:
            app.logger.error(f"Unexpected error: {str(e)}")
            abort(500, "An unexpected error occurred.")

class BillingAPI(Resource):
    @jwt_required()
    def post(self, course_id):
        try:
            user_id = get_jwt_identity()
            user = User.objects.get(id=user_id)
            course = Course.objects.get(id=course_id)
            
            if course.user.id != user.id:
                raise UnprocessableEntity("You do not have permission to create billing for this course.")
            
            # Calculate billing amount based on course details
            billing_amount = course.calculate_billing()
            
            # Create billing entry
            billing = Billing(
                user=user,
                course=course,
                billing_amount=billing_amount
            )
            billing.save()

            serialized_billing = BillingSchema().dump(billing)
            return serialized_billing, 201
        
        except (User.DoesNotExist, Course.DoesNotExist) as e:
            app.logger.error(f"User or Course not found: {str(e)}")
            abort(404, "User or Course not found.")
        
        except UnprocessableEntity as e:
            app.logger.error(f"Unprocessable Entity: {str(e)}")
            abort(422, str(e))
        
        except Exception as e:
            app.logger.error(f"Unexpected error: {str(e)}")
            abort(500, "An unexpected error occurred.")

    @jwt_required()
    def get(self):
        try:
            user_id = get_jwt_identity()
            user = User.objects.get(id=user_id)

            # Fetch all billings for the user
            billings = Billing.objects(user=user)
            serialized_billings = BillingSchema(many=True).dump(billings)

            return serialized_billings, 200
        
        except User.DoesNotExist:
            app.logger.error(f"User with id {user_id} not found.")
            abort(404, "User not found.")
        
        except Exception as e:
            app.logger.error(f"Unexpected error: {str(e)}")
            abort(500, "An unexpected error occurred.")


            