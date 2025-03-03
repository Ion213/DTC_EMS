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

user_view_events= Blueprint('user_view_events', __name__)



#render schedule template
@user_view_events.route('/render_user_events_page', methods=['GET'])
@login_required
@role_required_multiple('student')
def render_user_events_page():
    return render_template('user_view_events.jinja2')
#----------------------------------

#render upcoming schedule data (api)
@user_view_events.route('/render_upcoming_events', methods=['GET'])
@login_required
@role_required_multiple('student')
def render_upcoming_events():
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

            }
            all_schedule.append(schedule_data)

        return jsonify({'data': all_schedule})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})
#--------------------------------------------------   

#render ongoing schedule data (api)
@user_view_events.route('/render_ongoing_events', methods=['GET'])
@login_required
@role_required_multiple('student')
def render_ongoing_events():
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
            }
            all_schedule.append(schedule_data)

        return jsonify({'data': all_schedule})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})
#---------------------------------------------------------------

#render completed schedule data (api)
@user_view_events.route('/render_completed_events', methods=['GET'])
@login_required
@role_required_multiple('student')
def render_completed_events():
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

            }
            all_schedule.append(schedule_data)

        return jsonify({'data': all_schedule})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})
    
#render Sched_activities data
@user_view_events.route('/render_activities/<int:sched_id>', methods=['GET'])
@login_required
@role_required_multiple('student')
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