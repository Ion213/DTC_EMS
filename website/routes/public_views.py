#libraries needed
from flask import (
    Blueprint, 
    render_template, 
    request, 
    redirect, 
    url_for, 
    flash
)
from flask_login import (
                        LoginManager,
                         login_user,
                         logout_user,
                         login_required,
                         current_user
                         )


from website.security.limiter import limiter 
from sqlalchemy.sql import func

from website.models.database_models import Sched_activities,Schedule
from pytz import timezone
manila_tz = timezone('Asia/Manila')
from datetime import datetime

public_views = Blueprint('public_views', __name__)

# ✅ Function to handle role-based redirection
def redirect_user_based_on_role(role):
    if role in ['admin', 'ssg']:
        return redirect(url_for('admin_manage_event.manage_event_render_template'))
    elif role == 'student':
        return redirect(url_for('user_side.user_side_render_template'))
    return redirect(url_for('user_auth.admin_login_render_template'))


@public_views.route('/', methods=['GET', 'POST'])
def home():
    if current_user.is_authenticated:
        return redirect_user_based_on_role(current_user.role)
    

    now = datetime.now(manila_tz).date()

    # Separate events based on time
    upcoming_events = Schedule.query.filter(func.date(Schedule.scheduled_date) > now).order_by(Schedule.scheduled_date.asc()).all()
    ongoing_events = Schedule.query.filter(func.date(Schedule.scheduled_date) == now).order_by(Schedule.scheduled_date.asc()).all()

    
    return render_template('public_home.html',upcoming_events=upcoming_events, ongoing_events=ongoing_events)


