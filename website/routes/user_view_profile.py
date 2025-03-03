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
from website.models.database_models import Schedule,User


user_view_profile= Blueprint('user_side', __name__)

#------------------------------------------------------------------------
#activities routes and api 
#------------------------------------------------------------------------
#render profile page user
@user_view_profile.route('/user_side_render_template/', methods=['GET', 'POST'])
@login_required
@role_required_multiple('student')
def user_side_render_template():
    user_id=current_user.id
    return render_template('user_view_profile.jinja2',user_id=user_id if user_id else None)


