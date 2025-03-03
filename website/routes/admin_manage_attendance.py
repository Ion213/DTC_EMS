#libraries needed
from flask import (
    Blueprint, 
    render_template, 
    request, 
    redirect, 
    url_for, 
    flash,
    jsonify
)
from flask_login import (
                        LoginManager,
                         login_user,
                         logout_user,
                         login_required,
                         current_user
                         )

from website.security.user_regulator import role_required_multiple

from pytz import timezone
from sqlalchemy import func
from datetime import datetime,time
manila_tz = timezone('Asia/Manila')
from sqlalchemy import or_,and_,extract
from website import db
from website.models.database_models import Schedule,User,Department,Sched_activities,Attendance


admin_manage_attendance = Blueprint('admin_manage_attendance', __name__)

#------------------------------------------------------------------------
#attendance routes and api 
#------------------------------------------------------------------------
#render manage attendance template
@admin_manage_attendance.route('/manage_attendance_render_template', methods=['GET'])
@login_required
@role_required_multiple('admin', 'ssg')
def manage_attendance_render_template():
    now = datetime.now(manila_tz).time()  # Get current Manila time as a time object

    # Get today's ongoing event
    ongoing_event = Schedule.query.filter(
        func.date(Schedule.scheduled_date) == datetime.now(manila_tz).date()
    ).first()

    # Default empty list
    ongoing_activities = []

    if ongoing_event:
        # Fetch activities
        ongoing_activities = Sched_activities.query.filter(
            Sched_activities.sched_id == ongoing_event.id
        ).all()

        # Sort activities:
        # - Ongoing first (end_time >= now), past last (end_time < now)
        # - Within each group, sort by start_time
        ongoing_activities.sort(key=lambda act: (act.end_time.time() < now, act.start_time.time()))

    return render_template(
        'admin_manage_attendance.jinja2',
        ongoing_event=ongoing_event,
        ongoing_activities=ongoing_activities,
    )
'''
@admin_manage_attendance.route('/manage_attendance_render_template', methods=['GET'])
@login_required
@role_required_multiple('admin', 'ssg')
def manage_attendance_render_template():
    ongoing_event = Schedule.query.filter(
        func.date(Schedule.scheduled_date) == datetime.now(manila_tz).date()
    ).first()

    # Ensure ongoing_activities is always initialized
    ongoing_activities = []

    if ongoing_event:
        ongoing_activities = Sched_activities.query.filter(
            Sched_activities.sched_id == ongoing_event.id,
            #Sched_activities.end_time>datetime.now(manila_tz)
        ).order_by(Sched_activities.start_time.asc()).all()

    return render_template(
        'admin_manage_attendance.jinja2',
        ongoing_event=ongoing_event,
        ongoing_activities=ongoing_activities,
    )
'''




#-----------------ongoing events
#get attendance data
@admin_manage_attendance.route('/manage_attendance_get_data/<int:activity_id>', methods=['GET'])
@login_required
@role_required_multiple('admin', 'ssg')
def manage_attendance_get_data(activity_id):
    try:
        # Fetch attendance data
        attendance = Attendance.query.filter(Attendance.activity_id == activity_id).all()
        all_attendees = []
        
        for a in attendance:
            schedule_data = {
                'id': a.id if a.id else None,
                'activity_id': a.activity_id if a.activity_id else None,
                'activity_name': a.sched_activities.activity_name if a.sched_activities.activity_name else None,
                'student_id': a.student_id if a.student_id else None,
                'student_name': f"{a.user.first_name} {a.user.last_name}" if a.user and a.user.first_name and a.user.last_name else None,
                'time_in': a.time_in.strftime('%I:%M %p') if a.time_in else None,  # Format datetime
                'time_out': a.time_out.strftime('%I:%M %p') if a.time_out else None,  # Format datetime
                'departments': f"{a.user.department.department_name}| {a.user.department.section}| {a.user.department.year}" if a.user else None,
            }
            all_attendees.append(schedule_data)  # Append the dictionary to the list

        # Return the entire list of attendees
        return jsonify({'data': all_attendees})

    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

#filter
@admin_manage_attendance.route('/add_filter_users', methods=['GET'])
@login_required
@role_required_multiple('admin','ssg')
def add_filter_users():
    try:
        input = request.args.get('input', '').lower()
        if input:
            # Query the database for users matching the name in first_name or last_name
            filtered_users = User.query.filter(
                and_(
                    User.role == 'student',
                    or_(
                        func.lower(User.first_name).ilike(f"%{input}%"),
                        func.lower(User.last_name).ilike(f"%{input}%"),
                        (func.lower(User.first_name) + "" + func.lower(User.last_name)).ilike(f"%{input}%"),  # Match full name no space
                        (func.lower(User.first_name) + " " + func.lower(User.last_name)).ilike(f"%{input}%"),  # Match full name with space
                        (func.lower(User.last_name) + "" + func.lower(User.first_name)).ilike(f"%{input}%") , # Match full name reverse no space
                        (func.lower(User.last_name) + " " + func.lower(User.first_name)).ilike(f"%{input}%") , #  Match full name reverse with space

                        
                    )
                )
            ).all()

            users=[]
            for user in filtered_users:

                user_data={
                    'id': user.id,
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                    'department':user.department.department_name +" "+ user.department.year +"-"+ user.department.section
                }
                users.append(user_data)

            return jsonify({'user': users})
        else:
            return jsonify({"user": []})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})      
    
    
#add attendeess IN
@admin_manage_attendance.route('/add_attendees_in/<activity_id>/<user_id>', methods=['POST'])
@login_required
@role_required_multiple('admin', 'ssg')
def add_attendees_in(activity_id, user_id):
    try:
        if not activity_id:
            return jsonify({'success': False, 'message': 'No selected activity ❌'})
        if not user_id:
            return jsonify({'success': False, 'message': 'No selected Student ❌'})
        
        student=User.query.filter_by(
            id=user_id
        ).first()

        activity=Sched_activities.query.get(activity_id)
        if not activity:
            return jsonify({'success': False, 'message': f'No events and activity selected ❌'})

        # Check if the attendees already exists
        already_attended = Attendance.query.filter_by(
            activity_id=activity_id,
            student_id=user_id  # Ensure that you use the correct column name
        ).first()

        if already_attended:
            if already_attended.time_in:
                return jsonify({'success': False, 'message': f'{student.first_name} {student.last_name} Already Time In ❌'})

        # Create a new attendance record
        attendeeAdd = Attendance(
            activity_id=activity_id, 
            student_id=user_id,  # Ensure the column matches your model
            time_in=datetime.now(manila_tz).replace(second=0, microsecond=0)  # Set the correct time zone
        )
        db.session.add(attendeeAdd)
        db.session.commit()

        return jsonify({'success': True, 'message': f'{student.first_name} {student.last_name} Time In successfully ✅'})

    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)})
    
#add attendeess OUT
@admin_manage_attendance.route('/add_attendees_out/<activity_id>/<user_id>', methods=['POST'])
@login_required
@role_required_multiple('admin', 'ssg')
def add_attendees_out(activity_id, user_id):
    try:
        if not activity_id:
            return jsonify({'success': False, 'message': 'No selected activity ❌'})
        if not user_id:
            return jsonify({'success': False, 'message': 'No selected Student ❌'})
        
        student=User.query.filter_by(
            id=user_id
        ).first()

        activity=Sched_activities.query.get(activity_id)
        if not activity:
            return jsonify({'success': False, 'message': f'No events and activity selected ❌'})

        # Check if the attendees already exists
        already_attended = Attendance.query.filter_by(
            activity_id=activity_id,
            student_id=user_id  # Ensure that you use the correct column name
        ).first()

        if already_attended:
            if already_attended.time_out:
                return jsonify({'success': False, 'message': f'{student.first_name} {student.last_name} Already Time Out ❌'})

        if not already_attended:
            return jsonify({'success': False, 'message': f'{student.first_name} {student.last_name} Please Time In first ❌'})
        
        attendeeAdd = Attendance.query.filter_by(
            activity_id=activity_id,
            student_id=user_id
            ).first()
        attendeeAdd.time_out = datetime.now(manila_tz).replace(second=0,microsecond=0)
        db.session.commit()
        return jsonify({'success': True, 'message': f'{student.first_name} {student.last_name} Time Out Successfully ✅'})
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)})
    
#add attendees using qrcode IN
@admin_manage_attendance.route('/add_attendeesQR_in/<int:activity_id>/<string:student_id>', methods=['POST'])
@login_required
def add_attendeesQR_in(activity_id,student_id):
    try:
        if not activity_id:
            return jsonify({'success': False, 'message': 'No selected activity ❌'})
        
        if not student_id:
            return jsonify({'success': False, 'message': 'Invalid QR code data ❌'})

        activity = Sched_activities.query.get(activity_id)
        if not activity:
            return jsonify({'success': False, 'message': 'Activity not found❌'})
            
        student = User.query.filter_by(student_ID=student_id).first()
        if not student:
            return jsonify({'success': False, 'message': 'Student not found ❌'})

        # Check if the attendees already exists
        already_attended = Attendance.query.filter_by(
            activity_id=activity_id,
            student_id=student.id  # Ensure that you use the correct column name
        ).first()

        if already_attended:
            if already_attended.time_in:
                return jsonify({'success': False, 'message': f'{student.first_name} {student.last_name} Already Time In ❌'})
        # Create a new attendance record
        attendeeAdd = Attendance(
            activity_id=activity_id, 
            student_id=student.id ,  # Ensure the column matches your model
            time_in=datetime.now(manila_tz).replace(second=0, microsecond=0)  # Set the correct time zone
        )
        db.session.add(attendeeAdd)
        db.session.commit()

        return jsonify({'success': True, 'message': f'{student.first_name} {student.last_name} Time In successfully ✅'})

    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)})
    
#add attendees using qrcode OUT
@admin_manage_attendance.route('/add_attendeesQR_out/<int:activity_id>/<string:student_id>', methods=['POST'])
@login_required
def add_attendeesQR_out(activity_id,student_id):
    try:
        if not activity_id:
            return jsonify({'success': False, 'message': 'No selected activity ❌'})
        
        if not student_id:
            return jsonify({'success': False, 'message': 'Invalid QR code data ❌'})

        activity = Sched_activities.query.get(activity_id)
        if not activity:
            return jsonify({'success': False, 'message': 'Activity not found❌'})
            
        student = User.query.filter_by(student_ID=student_id).first()
        if not student:
            return jsonify({'success': False, 'message': 'Student not found ❌'})

        # Check if the attendees already exists
        already_attended = Attendance.query.filter_by(
            activity_id=activity_id,
            student_id=student.id  # Ensure that you use the correct column name
        ).first()

        if already_attended:
            if already_attended.time_out:
                return jsonify({'success': False, 'message': f'{student.first_name} {student.last_name} Already Time Out ❌'})

        if not already_attended:
            return jsonify({'success': False, 'message': f'{student.first_name} {student.last_name} Please Time In first ❌'})
        
        attendeeAdd = Attendance.query.filter_by(
            activity_id=activity_id,
            student_id=student.id
            ).first()
        attendeeAdd.time_out = datetime.now(manila_tz).replace(second=0,microsecond=0)
        db.session.commit()
        return jsonify({'success': True, 'message': f'{student.first_name} {student.last_name} Time Out Successfully ✅'})

    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)})
    
#delete ongoing
@admin_manage_attendance.route('/delete_attendees/<int:attendee_id>', methods=['DELETE'])
@login_required
@role_required_multiple('admin','ssg')
def delete_attendees(attendee_id):
    try:
        # Fetch the attendance record by ID
        attendanceDel = Attendance.query.get(attendee_id)
        
        # If the attendance record doesn't exist, return an error message
        if not attendanceDel:
            return jsonify({'success': False, 'message': 'Attendee not found'})

        # Fetch the student associated with this attendance record
        student = User.query.get(attendanceDel.student_id)  # assuming 'student_id' is the correct column
        
        # If no student is found, return an error message
        if not student:
            return jsonify({'success': False, 'message': 'Student not found'})

        # Delete the attendance record from the database
        db.session.delete(attendanceDel)
        db.session.commit()

        # Return a success message
        return jsonify({'success': True, 'message': f'{student.first_name} {student.last_name} removed successfully'})

    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)})
    






#----------completed event-------------------------------
#get completed events
@admin_manage_attendance.route('/get_completed_events/', methods=['GET'])
def get_completed_events():
    # Fetch completed events
    completed_events = Schedule.query.filter(func.date(Schedule.scheduled_date) < datetime.now(manila_tz).date()).all()

    events_data = []
    for event in completed_events:
        events_data.append({
            "id": event.id,
            "event_name": event.event_name,
            "scheduled_date": event.scheduled_date.strftime('%Y-%B-%d-%A'),
            "activities": [
                {"id": activity.id, 
                 "name": activity.activity_name,
                 "start_time":activity.start_time.strftime('%I:%M %p'),
                "end_time":activity.end_time.strftime('%I:%M %p')
                 }
                for activity in event.scheduled_activities  # Fetch related activities
            ]
        })

    return jsonify(events_data)

#get attendance
@admin_manage_attendance.route('/get_attendance/<int:activity_id>', methods=['GET'])
def get_attendance(activity_id):
    attendance_records = Attendance.query.filter_by(activity_id=activity_id).all()

    attendance_data = []
    for record in attendance_records:
        attendance_data.append({
            "student_id": record.student_id,
            "time_in": record.time_in.strftime('%I:%M %p'),
            "time_out": record.time_out.strftime('%I:%M %p')
        })

    return jsonify(attendance_data)


   
#add attendeess IN - OUT
@admin_manage_attendance.route('/add_attendees_in_out/<activity_id>/<user_id>', methods=['POST'])
@login_required
@role_required_multiple('admin', 'ssg')
def add_attendees_in_out(activity_id, user_id):
    try:
        if not activity_id:
            return jsonify({'success': False, 'message': 'No selected activity ❌'})
        if not user_id:
            return jsonify({'success': False, 'message': 'No selected Student ❌'})
        
        student=User.query.filter_by(
            id=user_id
        ).first()

        activity=Sched_activities.query.get(activity_id)
        if not activity:
            return jsonify({'success': False, 'message': f'No events and activity selected ❌'})

        # Check if the attendees already exists
        already_attended = Attendance.query.filter_by(
            activity_id=activity_id,
            student_id=user_id  # Ensure that you use the correct column name
        ).first()

        if already_attended:

            if already_attended.time_in and already_attended.time_out:
                return jsonify({'success': False, 'message': f'{student.first_name} {student.last_name} Already attended ❌'})

            if already_attended.time_in and not already_attended.time_out:
                attendeeAdd = Attendance.query.filter_by(
                        activity_id=activity_id,
                        student_id=user_id
                    ).first()
                attendeeAdd.time_out = activity.end_time
                db.session.commit()
                return jsonify({'success': True, 'message': f'{student.first_name} {student.last_name} Attended successfully ✅'})
            

            # Create a new attendance record
        attendeeAdd = Attendance(
                activity_id=activity_id, 
                student_id=user_id,  # Ensure the column matches your model
                time_in=activity.start_time,  # Set the correct time zone
                time_out=activity.end_time
            )
        db.session.add(attendeeAdd)
        db.session.commit()
        return jsonify({'success': True, 'message': f'{student.first_name} {student.last_name} Attended successfully ✅'})

        

    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)})


   
#delete
@admin_manage_attendance.route('/delete_attendees_ended/<int:attendee_id>', methods=['DELETE'])
@login_required
@role_required_multiple('admin','ssg')
def delete_attendees_ended(attendee_id):
    try:
        # Fetch the attendance record by ID
        attendanceDel = Attendance.query.get(attendee_id)
        
        # If the attendance record doesn't exist, return an error message
        if not attendanceDel:
            return jsonify({'success': False, 'message': 'Attendee not found'})

        # Fetch the student associated with this attendance record
        student = User.query.get(attendanceDel.student_id)  # assuming 'student_id' is the correct column
        
        # If no student is found, return an error message
        if not student:
            return jsonify({'success': False, 'message': 'Student not found'})

        # Delete the attendance record from the database
        db.session.delete(attendanceDel)
        db.session.commit()

        # Return a success message
        return jsonify({'success': True, 'message': f'{student.first_name} {student.last_name} removed successfully'})

    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)})
    







