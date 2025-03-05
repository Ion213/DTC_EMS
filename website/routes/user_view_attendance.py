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
from website.security.user_regulator import role_required

from werkzeug.security import generate_password_hash

from pytz import timezone
manila_tz = timezone('Asia/Manila')
from datetime import datetime
from sqlalchemy import or_,and_,extract
from sqlalchemy.sql import func
import random
import traceback

from website import db
from website.models.database_models import Department,User,Attendance,Payment,Schedule,Sched_activities,Transaction


user_view_attendance = Blueprint('user_view_attendance', __name__)

@user_view_attendance.route('/user_render_attendance_page/', methods=['GET'])
@login_required
@role_required('student')
def user_render_attendance_page():
    try:
        student_id=current_user.id
        if student_id is None:
            return jsonify({'success': False, 'message': 'Please provide a valid student ID.'}), 400
        # Get IDs of activities the student attended
        attended_activity_ids = db.session.query(Attendance.activity_id).filter(
            Attendance.student_id == student_id,
            Attendance.time_in.isnot(None),
            Attendance.time_out.isnot(None)
        ).subquery()

        # Get IDs of activities where the student missed out (checked in but never checked out)
        missed_out_activity_ids = db.session.query(Attendance.activity_id).filter(
            Attendance.student_id == student_id,
            Attendance.time_in.isnot(None),
            Attendance.time_out.is_(None)
        ).subquery()


        # Get IDs of paid events
        paid_events_ids = db.session.query(Payment.event_id).join(Transaction).filter(
            Transaction.student_id == student_id
        ).subquery()



        # Fines for activities the student missed out on
        missed_out_fines = db.session.query(func.sum(Sched_activities.fines)).filter(
            Sched_activities.id.in_(missed_out_activity_ids),

            Sched_activities.sched_id.notin_(paid_events_ids), 

            Sched_activities.end_time < datetime.now(manila_tz).replace(second=0, microsecond=0),
            Sched_activities.end_time > current_user.date_registered
        ).scalar() or 0  

        # Fines for activities the student was absent from (not attended & not missed out)
        absent_fines = db.session.query(func.sum(Sched_activities.fines)).filter(
            Sched_activities.id.notin_(attended_activity_ids),  # Not attended
            Sched_activities.id.notin_(missed_out_activity_ids),  # Not missed out

            Sched_activities.sched_id.notin_(paid_events_ids), 
            
            Sched_activities.end_time < datetime.now(manila_tz).replace(second=0, microsecond=0),
            Sched_activities.end_time > current_user.date_registered
        ).scalar() or 0 

        # Compute current balance (total fines - paid + missed out + absent)
        current_balance = (absent_fines + (missed_out_fines / 2))

    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500
   

    return render_template(
        'user_view_attendance.jinja2',
        current_balance=current_balance
    )



# Helper function to get attended and missed activity IDs
# Helper function to get attended and missed activity IDs
def get_activity_ids(student_id):
    now = datetime.now(manila_tz)

    # Get attended activities (both time_in and time_out are recorded)
    attended = db.session.query(Attendance.activity_id).join(Sched_activities).filter(
        Attendance.student_id == student_id,
        Attendance.time_in.isnot(None),
        Attendance.time_out.isnot(None),

    ).all()

    # Get missed activities (time_in is recorded but time_out is NULL)
    missed = db.session.query(Attendance.activity_id).join(Sched_activities).filter(
        Attendance.student_id == student_id,
        Attendance.time_in.isnot(None),
        Attendance.time_out.is_(None),

    ).all()

    return [row.activity_id for row in attended], [row.activity_id for row in missed]

#get unpaid event fines
@user_view_attendance.route('/get_student_unpaid_event_fines/', methods=['GET'])
@login_required
@role_required('student')
def get_student_unpaid_event_fines():
    try:
        student_id=current_user.id
        if student_id is None:
            return jsonify({'success': False, 'message': 'Please provide a valid student ID.'}), 400

        attended_ids, missed_ids = get_activity_ids(student_id)

        # Get IDs of paid events
        paid_events_ids = db.session.query(Payment.event_id).join(Transaction).filter(
            Transaction.student_id == student_id
        ).subquery()

        # Query unpaid event fines (without filtering by `end_time` here)
        unpaid_event_fines = db.session.query(Schedule).join(Sched_activities).filter(
            ~Schedule.id.in_(paid_events_ids),  # Events not paid for
            ~Sched_activities.id.in_(attended_ids),  # Activities not attended
            Sched_activities.end_time <=datetime.now(manila_tz).replace(second=0,microsecond=0),
            Sched_activities.end_time >current_user.date_registered
        ).all()

        unpaid_events = []
        for event in unpaid_event_fines:
            unpaid_data = {
                'id': event.id,
                'event_name': event.event_name,
                'scheduled_date': event.scheduled_date.strftime('%Y-%m-%d'),
                'total_fines': 0,
                'activity_counts': 0
            }

            for activity in event.scheduled_activities:
                if activity.id not in attended_ids and activity.end_time <= datetime.now():
                    is_missed = activity.id in missed_ids
                    fines = activity.fines / 2 if is_missed else activity.fines
                    unpaid_data['total_fines'] += fines
                    unpaid_data['activity_counts'] += getattr(activity, 'length', 1)

            if unpaid_data['total_fines'] > 0:  # Only add if fines exist
                unpaid_events.append(unpaid_data)

        return jsonify({'success': True, 'data': unpaid_events})

    except Exception as e:
        print("Error:", e)  # Print error for debugging
        return jsonify({'success': False, 'message': 'An error occurred while fetching unpaid event fines.'}), 500


#attendance
@user_view_attendance.route('/get_attended_data/', methods=['GET'])
@login_required
@role_required('student')
def get_attended_data():
    try:
        # Fetch all scheduled activities that have ended
        current_time = datetime.now(manila_tz).replace(second=0, microsecond=0)

        all_activities = Sched_activities.query.filter(
            Sched_activities.end_time < current_time,
            Sched_activities.end_time > current_user.date_registered
        ).all()

        all_attendance = []

        for activity in all_activities:
            # Check if the student attended this activity
            attendance = Attendance.query.filter(
                Attendance.activity_id == activity.id,
                Attendance.student_id == current_user.id
            ).first()

            if attendance:
                # User attended the event
                if attendance.time_in and attendance.time_out:
                    status = 'Attended: No fines ✅ '
                    fines = 0  # No fines
                
                elif attendance.time_in and not attendance.time_out:
                    fines = activity.fines / 2  # Half fine for missing time out
                    status = f'Missed (Time Out) fine: ₱{fines:.2f}'
                
                else:
                    status = '❌ Attendance record issue'
                    fines = 0  # Edge case

            else:
                # User missed the event
                fines = activity.fines
                status = f'Missed (No Attendance) fine: ₱{fines:.2f}'

            event_data = {
                'time_in': attendance.time_in.strftime('%Y-%B-%d-%A %I:%M %p') if attendance and attendance.time_in else "❌",
                'time_out': attendance.time_out.strftime('%Y-%B-%d-%A %I:%M %p') if attendance and attendance.time_out else "❌",
                'activity_fines': float(activity.fines) if activity.fines else 0.0,  # Ensure fines is a float
                'activity_name': activity.activity_name,
                'event_name': activity.schedule.event_name if activity.schedule else "N/A",
                'status': status
            }
            all_attendance.append(event_data)

        return jsonify({'success': True, 'data': all_attendance})

    except Exception as e:
        # Log the error for debugging purposes
        print(f"Error in get_attended_data: {str(e)}")
        return jsonify({'success': False, 'message': 'An error occurred while fetching attendance data.'}), 500
    


#get activities fines for each events upaid
@user_view_attendance.route('/get_student_unpaid_activities_fines/<int:event_id>', methods=['GET'])
@login_required
@role_required('student')
def get_student_unpaid_activities_fines(event_id):
    try:
        student_id=current_user.id

        if student_id is None or event_id is None:
            return jsonify({'success': False, 'message': 'Invalid student or event ID.'}), 400

        attended_ids, missed_ids = get_activity_ids(student_id)

        # Query unpaid activities fines
        unpaid_activities_fines = Sched_activities.query.filter(
            Sched_activities.sched_id == event_id,
            ~Sched_activities.id.in_(attended_ids),
            Sched_activities.end_time < datetime.now(manila_tz)
        ).all()

        unpaid_activities = []
        for activity in unpaid_activities_fines:
            is_missed = activity.id in missed_ids
            fines = activity.fines / 2 if is_missed else activity.fines

            unpaid_activities.append({
                'activity_name': activity.activity_name,
                'time_in': '✅' if is_missed else '❌',
                'time_out': '❌',
                'fines': fines,
            })

        return jsonify({'success': True, 'data': unpaid_activities if unpaid_activities else []})

    except Exception as e:
        return jsonify({'success': False, 'message': traceback.format_exc()}), 500
    

#get transaction record
@user_view_attendance.route('/get_student_transaction_history/', methods=['GET'])
@login_required
@role_required('student')
def get_student_transaction_history():
    try:

        student_id=current_user.id
        if not student_id:
            return jsonify({'success': False, 'message': 'Please provide a valid student ID.'}), 400

        # Fetch all transactions for the given student
        transactions = Transaction.query.filter_by(student_id=student_id).all()

        transactions_data = [
            {
                'id': transac.id,
                'amount_pay': f'₱{transac.amount_pay:.2f}',
                'selected_fines_total_amount': f'₱{transac.selected_fines_total_amount:.2f}',
                'current_balance': f'₱{transac.current_balance:.2f}',
                'changes_amount': f'₱{transac.changes_amount:.2f}',
                'transaction_code': transac.transaction_code,
                'transaction_date': transac.transaction_date.strftime('%Y-%B-%d-%A %I:%M %p') if transac.transaction_date else 'N/A',
            }
            for transac in transactions
        ]

        return jsonify({'data': transactions_data})

    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500
    
#transaction details
@user_view_attendance.route('/get_transaction_events/<int:transaction_id>', methods=['GET'])
@login_required
@role_required('student')
def get_transaction_events(transaction_id):
    try:
        # Use distinct event_id to prevent duplicate events
        payments = db.session.query(
            Schedule.event_name,
            Schedule.scheduled_date,
            db.func.min(Payment.date_paid).label('date_paid')
        ).join(Schedule).filter(Payment.transaction_id == transaction_id).group_by(Payment.event_id, Schedule.event_name,Schedule.scheduled_date).all()

        if not payments:
            return jsonify({'success': False, 'message': 'No events found for this transaction'}), 404

        event_details = [
            {
                'event_name': event_name,
                'scheduled_date': scheduled_date.strftime('%Y-%m-%d') if date_paid else "N/A",
            }
            for event_name, date_paid,scheduled_date in payments
        ]

        return jsonify({'success': True, 'data': event_details})

    except Exception as e:
        print("Error:", str(e))  # Log the error
        return jsonify({'success': False, 'message': 'Internal Server Error'}), 500


    
