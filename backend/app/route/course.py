from flask import Blueprint
from flask_restful import Api
from resource.course import CourseAPI, CourseListAPI, BulletinAPI, BulletinListAPI, ScoreListAPI, ScoreAPI, AttendanceAPI, CalendarAPI, BillingAPI

course_blueprint = Blueprint("course_api", __name__)
course_api = Api(course_blueprint)

# Courses endpoints
course_api.add_resource(
    CourseListAPI, "/courses"
)
course_api.add_resource(
    CourseAPI, "/courses/<string:course_id>"
)

# Bulletin endpoints
course_api.add_resource(
    BulletinListAPI, "/bulletin"
)
course_api.add_resource(
    BulletinAPI, "/bulletin/<string:bulletin_id>"
)

# Scores endpoints
course_api.add_resource(
    ScoreListAPI, '/scores'
)
course_api.add_resource(
    ScoreAPI, '/scores/<string:score_id>'
)

# Attendance endpoints
course_api.add_resource(
    AttendanceAPI, "/courses/<string:course_id>/attendances"
)

# Calendar endpoints
course_api.add_resource(
    CalendarAPI, "/courses/<string:course_id>/calendar"
)

# Billing endpoints
course_api.add_resource(
    BillingAPI, "/courses/<string:course_id>/billing"
)