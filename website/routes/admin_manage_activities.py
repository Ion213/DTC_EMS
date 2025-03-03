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
from website.models.database_models import Event, Activities,Schedule


admin_manage_activities = Blueprint('admin_manage_activities', __name__)

#------------------------------------------------------------------------
#activities routes and api 
#------------------------------------------------------------------------

#render manage activity html
@admin_manage_activities.route('/manage_activities_render_template/<int:event_id>', methods=['GET'])
@login_required
@role_required_multiple('admin','ssg')
def manage_activities_render_template(event_id):
    selected_event=Event.query.get(event_id)
    return render_template('admin_manage_activities.jinja2',selected_event=selected_event)


#render activities data
@admin_manage_activities.route('/render_activities_data/<int:event_id>', methods=['GET'])
@login_required
@role_required_multiple('admin','ssg')
def render_activities_data(event_id):
    try:
        # Fetch all activities associated with the given event_id
        activities = Activities.query.filter_by(event_id=event_id).all()
        all_activities=[]
        # Create a list of dictionaries containing activity details
        for a in activities:


            activities_data = {

                    'activity_name': a.activity_name,
                    'start_time': a.start_time.strftime('%I:%M %p'),  # Format datetime as string
                    'end_time': a.end_time.strftime('%I:%M %p'),      # Format datetime as string
                    'fines': a.fines,
                    'event_id': a.event_id,
                    'id': a.id
                }
            
            all_activities.append(activities_data)

            
        # Return the list of activities as a JSON response
        return jsonify({'success': True, 'data': all_activities})

    except Exception as e:
        # Handle any errors and return a meaningful response
        return jsonify({'success': False, 'message': str(e)}), 500


#add activity
@admin_manage_activities.route('/add_activity', methods=['POST'])
@login_required
@role_required_multiple('admin','ssg')
def add_activity():
    try:
        # Get the selected event ID from the form data
        event_id = request.form.get('selected_event_idT')
        activity_nameV = request.form.get('activity_nameT')
        start_time_str = request.form.get('start_timeT')
        end_time_str = request.form.get('end_timeT')
        finesV = request.form.get('finesT')  # Default fine to 0 if not provided
        
        # Validate form inputs
        if not event_id:
            return jsonify(success=False, message="Event not found empty.")
        if not activity_nameV:
            return jsonify(success=False, message="Activity name cannot be empty.")
        if not start_time_str:
            return jsonify(success=False, message="Start time cannot be empty.")
        if not end_time_str:
            return jsonify(success=False, message="End time cannot be empty.")
        if not finesV:
            finesV=0
        

        # Convert time strings to time objects
        start_timeV = datetime.strptime(start_time_str, '%H:%M').time()
        end_timeV = datetime.strptime(end_time_str, '%H:%M').time()

        # Validate time logic
        if start_timeV >= end_timeV:
            return jsonify(success=False, message="Start time must be earlier than end time.")
        if end_timeV <= start_timeV:
            return jsonify(success=False, message="Activity end time must be after start time.")
        
        # Check for conflicts with existing activities
        existing_activity = Activities.query.filter(
            Activities.event_id==event_id, 
            func.lower(Activities.activity_name)==func.lower(activity_nameV)
        ).first()

        conflicting_activity1 = Activities.query.filter(
            Activities.event_id == event_id,
            Activities.start_time < end_timeV,
            Activities.start_time > start_timeV,
        ).first()

        conflicting_activity2 = Activities.query.filter(
            Activities.event_id == event_id,
            Activities.end_time > start_timeV,
            Activities.end_time < end_timeV,
        ).first()

        if existing_activity:
            return jsonify(success=False, message="An activity with the same name already exists.")
        if conflicting_activity1 or conflicting_activity2:
            return jsonify(success=False, message="The activity conflicts with an existing activity time schedule.")

        # Create and save the new activity
        new_activity = Activities(
            event_id=event_id,
            activity_name=activity_nameV,
            start_time=start_timeV,
            end_time=end_timeV,
            fines=finesV
        )
        db.session.add(new_activity)
        db.session.commit()

        return jsonify(success=True, message="Activity added successfully!")

    except Exception as e:
        db.session.rollback()
        return jsonify(success=False, message=f"An error occurred: {str(e)}")

    
# Delete event activity
@admin_manage_activities.route('/delete_activity/<int:activity_id>', methods=['DELETE'])
@login_required
@role_required_multiple('admin','ssg')
def delete_activity(activity_id):
    activityDel = Activities.query.get(activity_id)
    
    try:
        if activityDel:
            db.session.delete(activityDel)
            db.session.commit()
            return jsonify({'success': True, 'message': 'Event activity deleted successfully'})
        else:

            return jsonify({'success': False, 'message': 'Event activity not found'})
    except Exception as e:
        db.session.rollback()  # Rollback the session in case of error
        return jsonify({'success': False, 'message': str(e)})


# Update Activities
@admin_manage_activities.route('/update_activities', methods=['PUT'])
@login_required
@role_required_multiple('admin','ssg')
def update_activity():
    try:
        # Get form data from the request
        selected_event_id = request.form.get('selected_event_idT')
        selected_activity_id = request.form.get('selected_activity_idT')
        update_activity_name = request.form.get('update_activity_nameT')
        update_start_str = request.form.get('update_activity_startT')
        update_end_str = request.form.get('update_activity_endT')
        update_fines = request.form.get('update_finesT')

        # Check if required fields are empty
        if not update_activity_name:
            return jsonify({'success': False, 'message': 'Activity name cannot be empty'})

        if not update_start_str:
            return jsonify({'success': False, 'message': 'Activity start time cannot be empty'})

        if not update_end_str:
            return jsonify({'success': False, 'message': 'Activity end time cannot be empty'})
        
        if not update_fines:
            update_fines=0

        # Convert the start and end times to datetime objects
        update_start = datetime.strptime(update_start_str, '%H:%M').time()
        update_end = datetime.strptime(update_end_str, '%H:%M').time()

        # Check for time conflicts
        if update_start >= update_end:
            return jsonify({'success': False, 'message': 'Start time must be before end time'})

        # Check for conflicting activities
        existing_activity = Activities.query.filter(
            Activities.event_id == selected_event_id,
            Activities.id != selected_activity_id,

            func.lower(Activities.activity_name) == func.lower(update_activity_name)
        ).first()

        conflicting_activity1 = Activities.query.filter(
            Activities.event_id == selected_event_id,
            Activities.id != selected_activity_id,
            Activities.start_time < update_end,
            Activities.start_time > update_start
        ).first()

        conflicting_activity2 = Activities.query.filter(
            Activities.event_id == selected_event_id,
            Activities.id != selected_activity_id,
            Activities.end_time > update_start,
            Activities.end_time < update_end
        ).first()

        if existing_activity:
            return jsonify({'success': False, 'message': 'An activity with the same name already exists in this event'})

        if conflicting_activity1 or conflicting_activity2:
            return jsonify({'success': False, 'message': 'There is a time conflict with an existing activity'})

        # Update the activity
        activity_to_update = Activities.query.get(selected_activity_id)
        activity_to_update.event_id = selected_event_id
        activity_to_update.activity_name = update_activity_name
        activity_to_update.start_time = update_start
        activity_to_update.end_time = update_end
        activity_to_update.fines = update_fines
        db.session.commit()

        return jsonify({'success': True, 'message': 'Activity updated successfully'})

    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)})

