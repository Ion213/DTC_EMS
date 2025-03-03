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
from website.models.database_models import Event, Activities,Schedule,Sched_activities,Attendance

admin_manage_schedule = Blueprint('admin_manage_schedule', __name__)



#render schedule template
@admin_manage_schedule.route('/manage_schedule_render_template', methods=['GET'])
@login_required
@role_required_multiple('admin', 'ssg')
def manage_schedule_render_template():
    events=Event.query.all()
    return render_template('admin_manage_schedule.jinja2',events=events)
#----------------------------------

#render upcoming schedule data (api)
@admin_manage_schedule.route('/render_schedule_data_upcoming', methods=['GET'])
@login_required
@role_required_multiple('admin', 'ssg')
def render_schedule_data_upcoming():
    try:
        schedule = Schedule.query.filter(func.date(Schedule.scheduled_date) > datetime.now(manila_tz).date()).all()
        all_schedule = []
        
        for s in schedule:

            start_TIme = Sched_activities.query.filter_by(sched_id=s.id).order_by(Sched_activities.start_time.asc()).first()
            end_Time = Sched_activities.query.filter_by(sched_id=s.id).order_by(Sched_activities.end_time.desc()).first()

            combined_datetimeS= datetime.combine(s.scheduled_date, start_TIme.start_time.time()).replace(second=0, microsecond=0)
            combined_datetimeE= datetime.combine(s.scheduled_date, end_Time.end_time.time()).replace(second=0, microsecond=0)



            schedule_data={
                'id': s.id,
                'event_name': s.event_name, 
                'scheduled_date': s.scheduled_date.strftime('%Y-%B-%d-%A'),
                'total_fines': f'₱{s.total_fines}', 

                'scheduled_date_S': combined_datetimeS.strftime('%Y-%m-%d %H:%M'),
                'scheduled_date_E': combined_datetimeE.strftime('%Y-%m-%d %H:%M'),

            }
            all_schedule.append(schedule_data)

        return jsonify({'data': all_schedule})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})
#--------------------------------------------------   

#render ongoing schedule data (api)
@admin_manage_schedule.route('/render_schedule_data_ongoing', methods=['GET'])
@login_required
@role_required_multiple('admin', 'ssg')
def render_schedule_data_ongoing():
    try:
        schedule = Schedule.query.filter(func.date(Schedule.scheduled_date) == datetime.now(manila_tz).date()).all()
        all_schedule = []
        
        for s in schedule:

            start_TIme = Sched_activities.query.filter_by(sched_id=s.id).order_by(Sched_activities.start_time.asc()).first()
            end_Time = Sched_activities.query.filter_by(sched_id=s.id).order_by(Sched_activities.end_time.desc()).first()

            combined_datetimeS= datetime.combine(s.scheduled_date, start_TIme.start_time.time()).replace(second=0, microsecond=0)
            combined_datetimeE= datetime.combine(s.scheduled_date, end_Time.end_time.time()).replace(second=0, microsecond=0)


            schedule_data={
                'id': s.id,
                'event_name': s.event_name, 
                'scheduled_date': s.scheduled_date.strftime('%Y-%B-%d-%A'),
                'total_fines': f'₱{s.total_fines}', 

                'scheduled_date_S': combined_datetimeS.strftime('%Y-%m-%d %H:%M'),
                'scheduled_date_E': combined_datetimeE.strftime('%Y-%m-%d %H:%M'),

            }
            all_schedule.append(schedule_data)

        return jsonify({'data': all_schedule})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})
#---------------------------------------------------------------

#render completed schedule data (api)
@admin_manage_schedule.route('/render_schedule_data_completed', methods=['GET'])
@login_required
@role_required_multiple('admin', 'ssg')
def render_schedule_data_completed():
    try:
        schedule = Schedule.query.filter(func.date(Schedule.scheduled_date) < datetime.now(manila_tz).date()).all()
        all_schedule = []
        
        for s in schedule:

            start_TIme = Sched_activities.query.filter_by(sched_id=s.id).order_by(Sched_activities.start_time.asc()).first()
            end_Time = Sched_activities.query.filter_by(sched_id=s.id).order_by(Sched_activities.end_time.desc()).first()

            combined_datetimeS= datetime.combine(s.scheduled_date, start_TIme.start_time.time()).replace(second=0, microsecond=0)
            combined_datetimeE= datetime.combine(s.scheduled_date, end_Time.end_time.time()).replace(second=0, microsecond=0)


            schedule_data={
                'id': s.id,
                'event_name': s.event_name, 
                'scheduled_date': s.scheduled_date.strftime('%Y-%B-%d-%A'),
                'total_fines': f'₱{s.total_fines}', 

                'scheduled_date_S': combined_datetimeS.strftime('%Y-%m-%d %H:%M'),
                'scheduled_date_E': combined_datetimeE.strftime('%Y-%m-%d %H:%M'),

            }
            all_schedule.append(schedule_data)

        return jsonify({'data': all_schedule})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})
    
#render Sched_activities data
@admin_manage_schedule.route('/render_sched_activities_data/<int:sched_id>', methods=['GET'])
@login_required
@role_required_multiple('admin', 'ssg')
def render_sched_activities_data(sched_id):
    try:
        # Fetch all activities associated with the given event_id
        activities = Sched_activities.query.filter_by(sched_id=sched_id).all()
        event_name=Schedule.query.filter_by(id=sched_id)
        all_activities=[]
        # Create a list of dictionaries containing activity details
        for a in activities:

            activities_data = {

                    'activity_name': a.activity_name,
                    'start_time': a.start_time.strftime('%I:%M %p'),  # Format datetime as string
                    'end_time': a.end_time.strftime('%I:%M %p'),      # Format datetime as string
                    'start_time_M': a.start_time.strftime('%Y-%m-%d %H:%M'),  # Format datetime as string
                    'end_time_M': a.end_time.strftime('%Y-%m-%d %H:%M'), 
                    'fines': a.fines,
                }
            
            all_activities.append(activities_data)
            
        # Return the list of activities as a JSON response
        return jsonify({'success': True, 'data': all_activities})

    except Exception as e:
        # Handle any errors and return a meaningful response
        return jsonify({'success': False, 'message': str(e)}), 500
#------------------------------------------------------------------------


#add schedule  
@admin_manage_schedule.route('/add_schedule', methods=['POST'])
@login_required
@role_required_multiple('admin', 'ssg')
def add_schedule():
    try:
        event_id = request.form.get('eventT')
        scheduled_date_str = request.form.get('schedule_dateT')
        scheduled_dateV = datetime.strptime(scheduled_date_str, '%Y-%m-%d')

        # Check if the schedule date is empty
        if not scheduled_date_str:
            return jsonify({'success': False, 'message': 'Schedule Date cannot be empty'})
        
        events= Event.query.get(event_id)
        activities=Activities.query.filter_by(event_id=event_id).all()

        if not activities:
            return jsonify({'success': False, 'message': 'Please add activity first in this event'})

        # Check if the schedule date is in future
        if scheduled_dateV.date()< datetime.now(manila_tz).date():
            return jsonify({'success': False, 'message': 'Schedule date must be in the future'})

        # Check if the schedule date is in future
        for activity in activities:
            if (scheduled_dateV.date() == datetime.now(manila_tz).date() and
                    activity.start_time < datetime.now(manila_tz).time()):
                return jsonify({'success': False, 'message': 'Activities in today\'s schedule must be in the future'})
        
        # Check for conflicting sched
        name_conflict_year = Schedule.query.filter(
            Schedule.event_name == events.event,
            Schedule.scheduled_date > datetime.now(manila_tz).date(),
            extract('year', Schedule.scheduled_date) == scheduled_dateV.year
        ).first()

        date_conflict = Schedule.query.filter(
            Schedule.scheduled_date == scheduled_dateV
        ).first()
        
        if name_conflict_year:
            return jsonify({'success': False, 'message': 'Cannot schedule same event in the same year'})

        if date_conflict:
            return jsonify({'success': False, 'message': 'The selected date conflicts with an already scheduled event'})

        # Prepare scheduled activities and fees
        scheduled_activities = []

        for activity in activities:

            if not activity.start_time or not activity.end_time:
                return jsonify({'success': False, 'message': f'Activity "{activity.activity_name}" must have valid start and end times'})
            
            start_timeWdate = datetime.strptime(f"{scheduled_date_str} {activity.start_time}", "%Y-%m-%d %H:%M:%S").replace(second=0, microsecond=0)
            end_timeWdate = datetime.strptime(f"{scheduled_date_str} {activity.end_time}", "%Y-%m-%d %H:%M:%S").replace(second=0, microsecond=0)
            
            scheduled_activities.append(Sched_activities(
                activity_name=activity.activity_name,
                start_time=start_timeWdate,
                end_time=end_timeWdate,
                fines=activity.fines,
                sched_id=None  # Temporary, set after schedule is added
            ))

        

        # Add and commit all together
        scheduleAdd = Schedule(
            event_name=events.event,
            total_fines = sum(activity.fines for activity in activities),
            scheduled_date=scheduled_dateV,
        )
        db.session.add(scheduleAdd)
        db.session.flush()  # Get schedule ID without committing

        # Update sched_id for activities and fees
        for activity in scheduled_activities:
            activity.sched_id = scheduleAdd.id

        db.session.add_all(scheduled_activities)
        db.session.commit()

        return jsonify({'success': True, 'message': 'Schedule Added successfully'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)})
#----------------------------------------------------------------


#delete schedule
@admin_manage_schedule.route('/delete_schedule/<int:sched_id>', methods=['DELETE'])
@login_required
@role_required_multiple('admin', 'ssg')
def delete_schedule(sched_id):
    try:
        # Fetch the schedule first
        scheduleDel = Schedule.query.get(sched_id)
        if not scheduleDel:
            return jsonify({'success': False, 'message': 'Schedule not found'})

        # Delete related attendances first (because they depend on activities)
        Attendance.query.filter(
            Attendance.activity_id.in_(
                db.session.query(Sched_activities.id).filter_by(sched_id=sched_id)
            )
        ).delete(synchronize_session=False)

        # Delete related activities and fees
        Sched_activities.query.filter_by(sched_id=sched_id).delete(synchronize_session=False)

        # Finally, delete the schedule itself
        db.session.delete(scheduleDel)
        db.session.commit()

        return jsonify({'success': True, 'message': 'Schedule canceled successfully'})

    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)})
#--------------------------------------------------------


#update schedule
@admin_manage_schedule.route('/update_schedule', methods=['PUT'])
@login_required
@role_required_multiple('admin', 'ssg')
def update_schedule():
    try:
        selected_schedule_id = request.form.get('update_selected_schedule_idT')
        update_schedule_date_str = request.form.get('update_schedule_dateT')

        activities=Sched_activities.query.filter_by(sched_id=selected_schedule_id).all()

        if not update_schedule_date_str:

            return jsonify({'success': False, 'message': 'Schedule Date cannot be empty'})
        
        update_schedule_dateV = datetime.strptime(update_schedule_date_str, '%Y-%m-%d')
        
        if update_schedule_dateV.date()< datetime.now(manila_tz).date():
            return jsonify({'success': False, 'message': 'Scheduled date must be in the future'}) 
        # Check if the schedule date is in future
        for activity in activities:
            if (update_schedule_dateV.date() == datetime.now(manila_tz).date() and
                    activity.start_time.time() < datetime.now(manila_tz).time()):
                return jsonify({'success': False, 'message': 'Activities in today\'s schedule must be in the future'})

        date_conflict = Schedule.query.filter(
            Schedule.id != selected_schedule_id,
            Schedule.scheduled_date == update_schedule_dateV,
            ).first()
                    
        if date_conflict:
            return jsonify({'success': False, 'message': 'The selected date conflicts with an already scheduled event'}) 


        # Update each activity's date and time
        for activity in activities:
            if not activity.start_time or not activity.end_time:
                return jsonify({'success': False, 'message': f'Activity "{activity.activity_name}" must have valid start and end times'})

            activity.start_time = datetime.strptime(
                f"{update_schedule_date_str} {activity.start_time.time()}","%Y-%m-%d %H:%M:%S").replace(second=0, microsecond=0)

            activity.end_time = datetime.strptime(
                f"{update_schedule_date_str} {activity.end_time.time()}","%Y-%m-%d %H:%M:%S").replace(second=0, microsecond=0)


        scheduleUp = Schedule.query.get(selected_schedule_id)
        scheduleUp.scheduled_date = update_schedule_dateV
        db.session.commit()
        return jsonify({'success': True, 'message': 'Schedule updated successfully'})
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)})
#---------------------------------------------------------------------