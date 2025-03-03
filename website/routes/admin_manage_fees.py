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

from sqlalchemy import func
from datetime import datetime,time
from sqlalchemy import or_,and_,extract
from website import db
from website.models.database_models import Event, Fees


admin_manage_fees= Blueprint('admin_manage_fees', __name__)

#------------------------------------------------------------------------
#fees routes and api 
#------------------------------------------------------------------------

#render manage fees html
@admin_manage_fees.route('/manage_fees_render_template/<int:event_id>', methods=['GET'])
@login_required
@role_required_multiple('admin', 'ssg')
def manage_fees_render_template(event_id):
    selected_event=Event.query.get(event_id)
    return render_template('admin_manage_fees.jinja2',selected_event=selected_event)

#render fees data
@admin_manage_fees.route('/render_fees_data/<int:event_id>', methods=['GET'])
@login_required
@role_required_multiple('admin', 'ssg')
def render_fees_data(event_id):
    try:
        # Fetch all fees associated with the given event_id
        fees = Fees.query.filter_by(event_id=event_id).all()
        all_fees=[]
        
        for f in fees:

            fees_data = {
                    'fees_name': f.fees_name,
                    'fees_amount': f.fees_amount,
                    'id': f.id,
                }
            all_fees.append(fees_data)
        
        # Return the list of activities as a JSON response
        return jsonify({'success': True, 'data': all_fees})
    except Exception as e:
        # Handle any errors and return a meaningful response
        return jsonify({'success': False, 'message': str(e)}), 500


# Add event fees
@admin_manage_fees.route('/add_fee', methods=['POST'])
@login_required
@role_required_multiple('admin', 'ssg')
def add_fee():
    try:
        event_idV=request.form.get('selected_event_idT')
        fees_nameV = request.form.get('fees_nameT')
        fees_amountV = request.form.get('fees_amountT',0)

        if not event_idV:
            return jsonify(success=False, message="Event not found")
        # Validate form data
        if not fees_nameV:
            return jsonify(success=False, message="Event fee name cannot be empty")
        if not fees_amountV:
            return jsonify(success=False, message="Event fee amount cannot be empty")

        # Check if fee already exists
        existing_fees = Fees.query.filter_by(event_id=event_idV, fees_name=fees_nameV).first()
        if existing_fees:
            return jsonify(success=False, message="Selected Fee name already exists in this event")

        # Add the new fee
        feesAdd = Fees(
            event_id=event_idV,
            fees_name=fees_nameV,
            fees_amount=fees_amountV
        )
        db.session.add(feesAdd)
        db.session.commit()

        return jsonify(success=True, message="Event Fee Added SUCCESSFULLY")

    except Exception as e:
        db.session.rollback()  # Rollback the session in case of an error
        return jsonify(success=False, message=str(e))


# Delete event fees
@admin_manage_fees.route('/delete_fee/<int:fee_id>', methods=['DELETE'])
@login_required
@role_required_multiple('admin', 'ssg')
def delete_fee(fee_id):
    try:
        feesDel = Fees.query.get(fee_id)
        if feesDel:
            db.session.delete(feesDel)
            db.session.commit()
            return jsonify(success=True, message="Event Fee deleted successfully")
        else:
            return jsonify(success=False, message="Event fee not found")
    except Exception as e:
        db.session.rollback()  # Rollback the session in case of error
        return jsonify(success=False, message=str(e))

# Update event fees
@admin_manage_fees.route('/update_fee', methods=['PUT'])
@login_required
@role_required_multiple('admin', 'ssg')
def update_fee():
    try:
        selected_event_id = request.form.get('selected_event_idT')
        selected_fees_id = request.form.get('selected_fees_idT')
        update_fees_nameV = request.form.get('update_fees_nameT')
        update_fees_amountV = request.form.get('update_fees_amountT',0)

        # Validation
        if not update_fees_nameV:
            return jsonify(success=False, message='Event fee name cannot be empty.')
        if not update_fees_amountV:
            return jsonify(success=False, message='Event fee amount cannot be empty.')

        # Check for conflicting fee name
        existing_fees = Fees.query.filter(
            Fees.id != selected_fees_id,
            Fees.event_id == selected_event_id,
            Fees.fees_name == update_fees_nameV
        ).first()
        
        if existing_fees:
            return jsonify(success=False, message='Selected Fee name already exists in this event')

        # Update the fee
        feesUp = Fees.query.get(selected_fees_id)
        feesUp.event_id = selected_event_id
        feesUp.fees_name = update_fees_nameV
        feesUp.fees_amount = update_fees_amountV
        db.session.commit()
        return jsonify(success=True, message='Event fees updated successfully.')

    except Exception as e:
        db.session.rollback()
        return jsonify(success=False, message=f'An error occurred: {str(e)}')

