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
import re

from website import db
from website.models.database_models import Department,User,Attendance

admin_manage_student_account = Blueprint('admin_manage_student_account', __name__)

#generate student id
@admin_manage_student_account.route('/generate_student_id', methods=['GET'])
@login_required
@role_required('admin')
def generate_student_id():
    while True:
        random_id = str(random.randint(100000, 999999))  # Generates exactly 6 digits
        if not User.query.filter_by(student_ID=random_id).first():  # Ensures uniqueness
            return jsonify({'random_id': random_id})

#rendeder student account template
@admin_manage_student_account.route('/manage_student_account_render_template', methods=['GET'])
@login_required
@role_required('admin')
def manage_student_account_render_template():
    departments=Department.query.all()
    return render_template('admin_manage_student_account.jinja2',departments=departments)

#render student data
@admin_manage_student_account.route('/render_student_account_data', methods=['GET'])
@login_required
@role_required('admin')
def render_student_account_data():
    try:

        student=User.query.filter_by(role='student').all()
        all_students = []
        
        for st in student:
            dep=Department.query.get(st.department_id)
            students_data = {
                'id': st.id,
                'student_ID':st.student_ID,
                'first_name':st.first_name,
                'last_name':st.last_name,
                'email':st.email,
                'password':st.password,
                'date_registered':st.date_registered.strftime('%Y-%B-%d-%A %I:%M %p') if st.date_registered else None,
                'date_updated':st.date_updated.strftime('%Y-%B-%d-%A %I:%M %p') if st.date_updated else None,

                'dep_id':dep.id,
                'department':dep.department_name,
                'year':dep.year,
                'section':dep.section,

            }
            
            all_students.append(students_data)
        return jsonify({'data': all_students})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})
    

#add student account
@admin_manage_student_account.route('/add_student_account', methods=['POST'])
@login_required
@role_required('admin')
def add_student_account():
    try:

        student_IDV = request.form.get('student_idT')
        first_nameV = request.form.get('first_nameT')
        last_nameV = request.form.get('last_nameT')
        emailV = request.form.get('emailT')
        passwordV = request.form.get('passwordT')
        selected_department_idV = request.form.get('departmentT')


        if not student_IDV:
            return jsonify({'success': False, 'message': 'Student ID cannot be empty'})
        if not first_nameV:
            return jsonify({'success': False, 'message': 'Student first name cannot be empty'})
        if not last_nameV:
            return jsonify({'success': False, 'message': 'student last name cannot be empty'})
        if not emailV:
            return jsonify({'success': False, 'message': 'student email cannot be empty'})
        if not passwordV:
            return jsonify({'success': False, 'message': 'Student password cannot be empty'})
        if not selected_department_idV:
            return jsonify({'success': False, 'message': 'Department cannot be empty'})
        
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, emailV):
                return jsonify({'success': False, 'message': 'Invalid email format.'})
        
        #hashed_password = generate_password_hash(passwordV, method='pbkdf2:sha512')

        existing_student_ID = User.query.filter_by(
            student_ID=student_IDV
            ).first()
        existing_student_name = User.query.filter_by(
            first_name=first_nameV,
            last_name=last_nameV
            ).first()
        existing_student_email= User.query.filter_by(
            email=emailV
            ).first()
        
        if existing_student_ID:
            return jsonify({'success': False, 'message': 'Student ID already used'})
        if existing_student_name:
            return jsonify({'success': False, 'message': 'Student already exists'})
        if existing_student_email:
            return jsonify({'success': False, 'message': 'Student email already used'})


        studentAdd = User(
            student_ID=student_IDV,
            first_name=first_nameV, 
            last_name=last_nameV,
            email=emailV,
            password=passwordV,
            date_registered=datetime.now(manila_tz).replace(second=0,microsecond=0),
            department_id=selected_department_idV
            )
        db.session.add(studentAdd)
        db.session.commit()
        return jsonify({'success': True})

    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)})

#delete student account
@admin_manage_student_account.route('/delete_student_account/<int:student_id>', methods=['DELETE'])
@login_required
@role_required('admin')
def delete_student_account(student_id):
    try:

        # Fetch the event by ID and delete it
        studentDel = User.query.get(student_id)
        if not studentDel:
            return jsonify({'success': False, 'message': 'Student not found'})
        # Delete attendance records associated with the student (fixing the relationship issue)
        Attendance.query.filter(Attendance.user.has(id=student_id)).delete()
        db.session.delete(studentDel)
        db.session.commit()
        return jsonify({'success': True, 'message': 'Student Account deleted successfully'})

    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)})

#update student account
@admin_manage_student_account.route('/update_student_account', methods=['PUT'])
@login_required
@role_required('admin')
def update_student_account():
    try:
        selected_student_account_idV = request.form.get('selected_student_account_idT')
        update_student_idV = request.form.get('update_student_idT')
        update_first_nameV = request.form.get('update_first_nameT')
        update_last_nameV= request.form.get('update_last_nameT')
        update_emailV = request.form.get('update_emailT')
        update_passwordV = request.form.get('update_passwordT')
        update_departmentV= request.form.get('update_departmentT')

        
        if not selected_student_account_idV:
            return jsonify({'success': False, 'message': 'student not found'})
        if not update_student_idV:
            return jsonify({'success': False, 'message': 'id cannot be empty'})
        if not update_first_nameV:
            return jsonify({'success': False, 'message': 'first name cannot be empty'})
        if not update_last_nameV:
            return jsonify({'success': False, 'message': 'last name cannot be empty'})
        if not update_emailV:
            return jsonify({'success': False, 'message': 'email cannot be empty'})
        if not update_passwordV:
            return jsonify({'success': False, 'message': 'password cannot be empty'})
        if not update_departmentV:
            return jsonify({'success': False, 'message': 'department cannot be empty'})
        
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, update_emailV):
                return jsonify({'success': False, 'message': 'Invalid email format.'})
        
        #hashed_password = generate_password_hash(update_passwordV, method='pbkdf2:sha512')

        existing_student_name = User.query.filter(
            User.id != selected_student_account_idV,
            User.first_name == update_first_nameV,
            User.last_name==update_last_nameV
            ).first()
        
        existing_student_email = User.query.filter(
            User.id != selected_student_account_idV,
            User.email==update_emailV,
            ).first()
        
        if existing_student_name:
            return jsonify({'success': False, 'message': 'Student already exist'})
        
        if existing_student_email:
            return jsonify({'success': False, 'message': 'email already used'})

        # Update the event
        studentUp = User.query.get(selected_student_account_idV)
        studentUp.student_ID=update_student_idV
        studentUp.first_name=update_first_nameV
        studentUp.last_name=update_last_nameV
        studentUp.email=update_emailV
        studentUp.password=update_passwordV
        studentUp.department_id=update_departmentV
        studentUp.date_updated=datetime.now(manila_tz).replace(microsecond=0,second=0)
        db.session.commit()
        return jsonify({'success': True, 'message': 'Student account updated successfully'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)})

