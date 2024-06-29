from utils import db
from model.user import User

class Course(db.Document):
    user = db.ReferenceField(User)
    kode_mk = db.StringField(required=True, unique=True)
    semester = db.StringField(required=True)
    nama_mk = db.StringField(required=False)
    sks = db.IntField(required=False)
    description = db.StringField(required=False)
    
class Bulletin(db.Document):
    name = db.StringField(required=True)
    content =  db.StringField(required=False)
    course = db.ReferenceField(Course)

class Attendance(db.Document):
    user = db.ReferenceField(User, required=True)
    course = db.ReferenceField(Course, required=True)
    date = db.DateTimeField(required=True)
    status = db.StringField(choices=["Present", "Absent", "Late"], required=True)

class CalendarEvent(db.Document):
    user = db.ReferenceField(User, required=True)
    title = db.StringField(required=True)
    description = db.StringField()
    start_time = db.DateTimeField(required=True)
    end_time = db.DateTimeField(required=True)

class Billing(db.Document):
    user = db.ReferenceField(User, required=True)
    course = db.ReferenceField(Course, required=True)
    amount_due = db.FloatField(required=True)
    due_date = db.DateTimeField(required=True)
    status = db.StringField(choices=["paid", "unpaid"], default="unpaid")

class Score(db.Document):
    user = db.ReferenceField(User, required=True)
    course = db.ReferenceField(Course, required=True)
    score = db.FloatField(required=True)
    date = db.DateTimeField(required=True)