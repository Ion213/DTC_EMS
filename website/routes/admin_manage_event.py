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
manila_tz = timezone('Asia/Manila')
from datetime import datetime
from sqlalchemy import or_,and_,extract
from sqlalchemy.sql import func

from website import db
from website.models.database_models import Event, Activities,Schedule

admin_manage_event = Blueprint('admin_manage_event', __name__)
#------------------------------------------------------------------------
#event routes and api 
#------------------------------------------------------------------------
#render manage_event html
@admin_manage_event.route('/manage_event_render_template', methods=['GET'])
@login_required
@role_required_multiple('admin','ssg')
def manage_event_render_template():
    return render_template('admin_manage_event.jinja2')

#render event data (api)
@admin_manage_event.route('/render_event_data', methods=['GET'])
@login_required
@role_required_multiple('admin','ssg')
def render_event_data():
    try:
        events = Event.query.all()
        all_events = []
        
        for e in events:

            total_fines = sum(fine.fines for fine in e.event_activities)
            formatted_fines = '{:,.2f}'.format(total_fines)

            activity_count = len(e.event_activities) 

            event_data = {
                'id': e.id,
                'event': e.event,
                'event_description': e.event_description,
                'date_created': e.date_created.strftime('%Y-%B-%d-%A %I:%M %p'),
                'date_updated': e.date_updated.strftime('%Y-%B-%d-%A %I:%M %p') if e.date_updated else None,
                'activity_count' : activity_count,
                'total_fines':formatted_fines
            }
            
            all_events.append(event_data)

        return jsonify({'data': all_events})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

#add event (api)
@admin_manage_event.route('/add_event', methods=['POST'])
@login_required
@role_required_multiple('admin','ssg')
def add_event():
    try:
        # Get the event and description values from the form
        eventV = request.form.get('eventT')
        event_descriptionV = request.form.get('event_descriptionT')
        # Check if the event name is empty
        if not eventV:
            return jsonify({'success': False, 'message': 'Event name cannot be empty'})

        # Check if the event already exists
        existing_event = Event.query.filter(func.lower(Event.event) == func.lower(eventV)).first()
        if existing_event:
            return jsonify({'success': False, 'message': 'Event name already exists'})

        # If description is empty, set it to an empty string
        if not event_descriptionV:
            event_descriptionV = ""

        # Create a new event
        eventAdd = Event(
            event=eventV, 
            event_description=event_descriptionV,
            date_created=datetime.now(manila_tz).replace(second=0,microsecond=0)
            )
        db.session.add(eventAdd)
        db.session.commit()
        return jsonify({'success': True})

    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)})


# Delete event (api)
@admin_manage_event.route('/delete_event/<int:event_id>', methods=['DELETE'])
@login_required
@role_required_multiple('admin','ssg')
def delete_event(event_id):
    try:
        # Fetch the event by ID and delete it
        event_to_delete = Event.query.get(event_id)
        if not event_to_delete:
            return jsonify({'success': False, 'message': 'Event not found'})
        Activities.query.filter_by(event_id=event_to_delete.id).delete()
        db.session.delete(event_to_delete)
        db.session.commit()
        return jsonify({'success': True, 'message': 'Event deleted successfully'})

    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)})


# Update event (api)
@admin_manage_event.route('/update_event', methods=['PUT'])
@login_required
@role_required_multiple('admin','ssg')
def update_event():
    try:
        event_id = request.form.get('selected_event_id')
        event = request.form.get('update_event')
        event_description = request.form.get('update_event_description')

        # Check if the event name is empty
        if not event:
            return jsonify({'success': False, 'message': 'Event name cannot be empty'})

        # Check if the event name already exists
        existing_event = Event.query.filter(Event.id != event_id, func.lower(Event.event) == func.lower(event)).first()
        if existing_event:
            return jsonify({'success': False, 'message': 'Event name already exists'})

        # Update the event
        eventUp = Event.query.get(event_id)
        eventUp.event = event
        eventUp.event_description = event_description
        eventUp.date_updated= datetime.now(manila_tz).replace(second=0, microsecond=0)
        db.session.commit()

        return jsonify({'success': True, 'message': 'Event updated successfully'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)})
    
    #---------------------------------------------------------------------------------------------

    
