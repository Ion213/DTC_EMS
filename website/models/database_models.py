from website import db
from sqlalchemy.sql import func
from sqlalchemy import Enum
from pytz import timezone
from datetime import datetime,time
from flask_login import UserMixin

manila_tz = timezone('Asia/Manila')

#------------create event model---------------------
class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    event = db.Column(db.String(255),nullable=False)
    event_description = db.Column(db.String(500))
    date_created = db.Column(db.DateTime)
    date_updated= db.Column(db.DateTime, nullable=True)
    status = db.Column(db.String(20),nullable=True)
    event_activities = db.relationship('Activities', backref='event', lazy=True, cascade="all, delete-orphan")


class Activities(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    activity_name = db.Column(db.String(255),nullable=False)
    start_time = db.Column(db.Time,nullable=False)
    end_time = db.Column(db.Time,nullable=False)
    fines = db.Column(db.Float,nullable=True)
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'), nullable=False)



#------------schedule models---------------  
class Schedule(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    event_name=  db.Column(db.String(255),nullable=False)
    scheduled_date = db.Column(db.DateTime,nullable=False)
    scheduled_activities= db.relationship('Sched_activities', backref='schedule', lazy=True, cascade="all, delete-orphan")
    total_fines=db.Column(db.Float,nullable=True)
    payments = db.relationship('Payment', backref='schedule', lazy=True, cascade="all, delete-orphan")
    


class Sched_activities(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    activity_name = db.Column(db.String(255),nullable=False)
    start_time = db.Column(db.DateTime,nullable=False)
    end_time = db.Column(db.DateTime,nullable=False)
    fines = db.Column(db.Float,nullable=True)
    sched_id= db.Column(db.Integer, db.ForeignKey('schedule.id'), nullable=False)
    attendances = db.relationship('Attendance', backref='sched_activities', lazy=True, cascade="all, delete-orphan")
    

class Attendance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    time_in = db.Column(db.DateTime,nullable=True)
    time_out = db.Column(db.DateTime,nullable=True)

    activity_id = db.Column(db.Integer, db.ForeignKey('sched_activities.id'), nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)


# ------------ Payment Model -----------------
class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    current_balance = db.Column(db.Float, default=0.0, nullable=False)
    amount_pay = db.Column(db.Float, default=0.0, nullable=False)
    selected_fines_total_amount = db.Column(db.Float, default=0.0, nullable=False)
    changes_amount = db.Column(db.Float, default=0.0, nullable=False)
    transaction_code = db.Column(db.String(500),unique=True, nullable=False)  # No unique constraint
    transaction_date = db.Column(db.DateTime, nullable=True)

    # Relationship with Payment
    payments = db.relationship(
        'Payment', backref='transaction', cascade="all, delete-orphan", lazy=True
    )


class Payment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    event_id = db.Column(db.Integer, db.ForeignKey('schedule.id'), nullable=False)
    transaction_id = db.Column(db.Integer, db.ForeignKey('transaction.id'), nullable=False)
    date_paid = db.Column(db.DateTime, nullable=True)






 #------------------------  

class Department(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    department_name = db.Column(db.String(100), nullable=False)
    year = db.Column(db.String(100), nullable=False)
    section = db.Column(db.String(100), nullable=True)
    user = db.relationship('User', backref='department', lazy=True, cascade="all, delete-orphan")

    
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True, nullable=True)
    password = db.Column(db.String(150), nullable=False)
    student_ID = db.Column(db.String(20), unique=True, nullable=True)  # Only for students
    first_name = db.Column(db.String(100), nullable=True)             # Only for students
    last_name = db.Column(db.String(100), nullable=True)              # Only for students
    date_registered = db.Column(db.DateTime, nullable=True)
    date_updated = db.Column(db.DateTime, nullable=True)
    role = db.Column(db.String(50), nullable=False, default='student')  # 'student' or 'admin'
    is_verified = db.Column(db.Boolean, default=False)  # New field for email verification
    department_id = db.Column(db.Integer, db.ForeignKey('department.id'), nullable=True)  # Only for students
    attendances = db.relationship('Attendance', backref='user', lazy=True, cascade="all, delete-orphan") # Only for students
    transaction = db.relationship('Transaction', backref='user', lazy=True, cascade="all, delete-orphan")  # Track student payments

