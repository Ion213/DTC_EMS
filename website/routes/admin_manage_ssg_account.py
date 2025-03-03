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

from website import db
from website.models.database_models import User

admin_manage_ssg_account = Blueprint('admin_manage_ssg_account', __name__)


#rendeder ssg account template
@admin_manage_ssg_account.route('/manage_ssg_account_render_template', methods=['GET'])
@login_required
@role_required('admin')
def manage_ssg_account_render_template():
    return render_template('admin_manage_ssg_account.jinja2')

#render ssg data
@admin_manage_ssg_account.route('/render_ssg_account_data', methods=['GET'])
@login_required
@role_required('admin')
def render_ssg_account_data():
    try:

        ssg=User.query.filter_by(role='ssg').all()
        all_ssg = []
        
        for sg in ssg:
            ssg_data = {
                'id': sg.id,
                'email':sg.email,
                'password':sg.password,
                'date_registered':sg.date_registered.strftime('%Y-%B-%d-%A %I:%M %p') if sg.date_registered else None,
                'date_updated':sg.date_updated.strftime('%Y-%B-%d-%A %I:%M %p') if sg.date_updated else None,
            }
            
            all_ssg.append(ssg_data)
        return jsonify({'data': all_ssg})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})
    

#add ssg account
@admin_manage_ssg_account.route('/add_ssg_account', methods=['POST'])
@login_required
@role_required('admin')
def add_ssg_account():
    try:

        emailV = request.form.get('emailT')
        passwordV = request.form.get('passwordT')
        role="ssg"


        if not emailV:
            return jsonify({'success': False, 'message': 'Email cannot be empty'})
        if not passwordV:
            return jsonify({'success': False, 'message': 'Password cannot be empty'})
        
        #hashed_password = generate_password_hash(passwordV, method='pbkdf2:sha512')

        existing_email= User.query.filter_by(
            email=emailV
            ).first()

        if existing_email:
            return jsonify({'success': False, 'message': 'email already used'})

        ssgAdd = User(
            email=emailV,
            password=passwordV,
            role=role,
            date_registered=datetime.now(manila_tz).replace(second=0,microsecond=0)
            )
        db.session.add(ssgAdd)
        db.session.commit()
        return jsonify({'success': True})

    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)})



#delete student account
@admin_manage_ssg_account.route('/delete_ssg_account/<int:ssg_id>', methods=['DELETE'])
@login_required
@role_required('admin')
def delete_ssg_account(ssg_id):
    try:
        # Fetch the ssg by ID and delete it
        ssgDel = User.query.get(ssg_id)
        if not ssgDel:
            return jsonify({'success': False, 'message': 'SSG not found'})
        db.session.delete(ssgDel)
        db.session.commit()
        return jsonify({'success': True, 'message': 'SSG Account deleted successfully'})

    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)})

#update ssg account
@admin_manage_ssg_account.route('/update_ssg_account', methods=['PUT'])
@login_required
@role_required('admin')
def update_ssg_account():
    try:
        selected_ssg_account_idV = request.form.get('selected_ssg_account_idT')
        update_emailV = request.form.get('update_emailT')
        update_passwordV = request.form.get('update_passwordT')


        if not selected_ssg_account_idV:
            return jsonify({'success': False, 'message': 'SSG not found'})
        if not update_emailV:
            return jsonify({'success': False, 'message': 'SSG email cannot be empty'})
        if not update_passwordV:
            return jsonify({'success': False, 'message': 'SSG Password cannot be empty'})

        existing_email = User.query.filter(
            User.id != selected_ssg_account_idV,
            User.email == update_emailV
            ).first()

        if existing_email:
            return jsonify({'success': False, 'message': 'Email Already Used'})
        


        # Update the ssg account
        ssgUp = User.query.get(selected_ssg_account_idV)
        ssgUp.email=update_emailV
        ssgUp.password=update_passwordV
        ssgUp.date_updated=datetime.now(manila_tz).replace(microsecond=0,second=0)
        db.session.commit()
        return jsonify({'success': True, 'message': 'SSG account updated successfully'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)})

