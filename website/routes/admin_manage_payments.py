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

from werkzeug.security import generate_password_hash

from pytz import timezone
manila_tz = timezone('Asia/Manila')
from datetime import datetime
from sqlalchemy import or_,and_,extract
from sqlalchemy.sql import func
import random
import re
import traceback
import string

from website import db
from website.models.database_models import Department,User,Attendance,Payment,Schedule,Sched_activities,Transaction




admin_manage_payments = Blueprint('admin_manage_payments', __name__)


@admin_manage_payments.route('/payments_page', methods=['GET'])
@login_required
@role_required_multiple('admin', 'ssg')
def payments_page():

    return render_template('admin_manage_payments.html')



#filter
@admin_manage_payments.route('/get_student', methods=['GET'])
@login_required
@role_required_multiple('admin','ssg')
def get_student():
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

#get balance
@admin_manage_payments.route('/get_student_balance/<int:student_id>', methods=['GET'])
@login_required
@role_required_multiple('admin', 'ssg')
def get_student_balance(student_id):
    try:
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

            Sched_activities.end_time < datetime.now(manila_tz).replace(second=0, microsecond=0)
        ).scalar() or 0  

        # Fines for activities the student was absent from (not attended & not missed out)
        absent_fines = db.session.query(func.sum(Sched_activities.fines)).filter(
            Sched_activities.id.notin_(attended_activity_ids),  # Not attended
            Sched_activities.id.notin_(missed_out_activity_ids),  # Not missed out

            Sched_activities.sched_id.notin_(paid_events_ids), 
            
            Sched_activities.end_time < datetime.now(manila_tz).replace(second=0, microsecond=0)
        ).scalar() or 0 

        # Compute current balance (total fines - paid + missed out + absent)
        current_balance = (absent_fines + (missed_out_fines / 2))


        return jsonify({'success': True, 'balance': current_balance})

    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

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
@admin_manage_payments.route('/get_unpaid_event_fines/<int:student_id>', methods=['GET'])
@login_required
@role_required_multiple('admin', 'ssg')
def get_unpaid_event_fines(student_id):
    try:
        if student_id is None:
            return jsonify({'success': False, 'message': 'Please provide a valid student ID.'}), 400

        attended_ids, missed_ids = get_activity_ids(student_id)

        # Get IDs of paid events
        paid_events_ids = db.session.query(Payment.event_id).join(Transaction).filter(
            Transaction.student_id == student_id
        ).subquery()

        # Query unpaid event fines (without filtering by `end_time` here)
        unpaid_event_fines = Schedule.query.filter(
            ~Schedule.id.in_(paid_events_ids),  # Events not paid for
            Schedule.scheduled_activities.any(
                ~Sched_activities.id.in_(attended_ids)  # Activities not attended
            )
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
    


#get activities fines for each events upaid
@admin_manage_payments.route('/get_unpaid_activities_fines/<int:student_id>/<int:event_id>', methods=['GET'])
@login_required
@role_required_multiple('admin', 'ssg')
def get_unpaid_activities_fines(student_id, event_id):
    try:
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
    
    
    
#get payments amount to pay
@admin_manage_payments.route('/get_payments_amount/<int:student_id>', methods=['GET'])
@login_required
@role_required_multiple('admin', 'ssg')
def get_payments_amount(student_id):
    try:
        if student_id is None:
            return jsonify({'success': False, 'message': 'Please provide a valid student ID.'}), 400

        attended_ids, missed_ids = get_activity_ids(student_id)

        # Get IDs of paid events
        paid_events_ids = db.session.query(Payment.event_id).join(Transaction).filter(
            Transaction.student_id == student_id
        ).subquery()

        # Query unpaid event fines
        unpaid_event_fines = Schedule.query.filter(
            ~Schedule.id.in_(paid_events_ids),  # Use ~ for negation
            Schedule.scheduled_activities.any(
                ~Sched_activities.id.in_(attended_ids),
            ),
            Sched_activities.end_time < datetime.now(manila_tz)

        ).all()

        unpaid_events = []
        for event in unpaid_event_fines:
            unpaid_data = {
                'id': event.id,
                'event_name': event.event_name,
                'total_fines': 0,
                'scheduled_date':event.scheduled_date.strftime('%Y-%m-%d')
            }

            for activity in event.scheduled_activities:
                if activity.id not in attended_ids :
                    is_missed = activity.id in missed_ids
                    fines = activity.fines / 2 if is_missed else activity.fines
                    
                    unpaid_data['total_fines'] += fines

            unpaid_events.append(unpaid_data)

        return jsonify({'success': True, 'data': unpaid_events})

    except Exception as e:
        return jsonify({'success': False, 'message': traceback.format_exc()}), 500



#payments submit
def generate_transaction_code():
    """Generate a unique 12-character alphanumeric transaction code."""
    while True:
        random_code = ''.join(random.choices(string.ascii_letters + string.digits, k=12))
        if not db.session.query(db.exists().where(Transaction.transaction_code == random_code)).scalar():
            return random_code

@admin_manage_payments.route('/submit_payment/<int:student_id>', methods=['POST'])
@login_required
@role_required_multiple('admin', 'ssg')
def submit_payment(student_id):
    """Process student payments and create transaction records."""
    data = request.get_json()

    try:
        if not student_id:
            return jsonify({'success': False, 'message': 'Invalid student ID.'}), 400

        if not data or 'event_ids' not in data or not data['event_ids']:
            return jsonify({'success': False, 'message': 'Please select at least one event to pay for.'}), 400

        event_ids = data['event_ids']
        amount_pay = float(data.get('amount_pay', 0.0))
        selected_fines_total_amount = float(data.get('total_fine', 0.0)) 

        if amount_pay < selected_fines_total_amount:
            return jsonify({'success': False, 'message': 'Invalid payment amount.'}), 400

        reference_code = generate_transaction_code()
        changes_amount = max(0, amount_pay - selected_fines_total_amount)
        current_balance = 0.0  

        # Create a Transaction record
        transaction = Transaction(
            student_id=student_id,
            selected_fines_total_amount=selected_fines_total_amount,
            amount_pay=amount_pay,
            current_balance=current_balance,
            changes_amount=changes_amount,
            transaction_code=reference_code,
            transaction_date=datetime.now(manila_tz).replace(second=0, microsecond=0)
        )
        db.session.add(transaction)
        db.session.flush()  # Get transaction ID before creating payments

        payments = []
        for event_id in event_ids:
            event = Schedule.query.get(event_id)
            if not event:
                db.session.rollback()
                return jsonify({'success': False, 'message': f'Event ID {event_id} not found.'}), 404

            # Create a Payment record linked to the Transaction
            payment = Payment(
                event_id=event_id,
                transaction_id=transaction.id,
                date_paid=datetime.now(manila_tz).replace(second=0, microsecond=0)
            )
            payments.append(payment)
            db.session.add(payment)

        db.session.commit()

        return jsonify({'success': True, 'message': 'Payment processed successfully!', 'total_paid': amount_pay}), 200

    except Exception as e:
        db.session.rollback()
        print("Error:", str(e))  # Debugging log
        return jsonify({'success': False, 'message': 'Internal Server Error'}), 500
    




#get transaction record
@admin_manage_payments.route('/get_student_transaction_records/<int:student_id>', methods=['GET'])
@login_required
@role_required_multiple('admin', 'ssg')
def get_student_transaction_records(student_id):
    try:
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
    
#delete transaction
@admin_manage_payments.route('/delete_transaction/<string:transac_id>', methods=['DELETE'])
@login_required
@role_required_multiple('admin', 'ssg')
def delete_transaction(transac_id):
    try:
        # Find the transaction by transaction_code
        transaction = Transaction.query.filter_by(id=transac_id).first()

        if not transaction:
            return jsonify({'success': False, 'message': 'Transaction not found.'}), 404

        # Delete the transaction
        db.session.delete(transaction)
        db.session.commit()

        return jsonify({'success': True, 'message': 'Transaction deleted successfully.'})

    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500
    

#transaction details
@admin_manage_payments.route('/get_admin_transaction_events/<int:transaction_id>', methods=['GET'])
@login_required
@role_required_multiple('admin', 'ssg')
def get_admin_transaction_events(transaction_id):
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


    


