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

import random
import re
from werkzeug.security import generate_password_hash,check_password_hash

from pytz import timezone
from datetime import datetime,time
manila_tz = timezone('Asia/Manila')

from website import db
from website.models.database_models import User,Department


# ✅ Function to handle role-based redirection
def redirect_user_based_on_role(role):
    if role in ['admin', 'ssg']:
        return redirect(url_for('admin_manage_event.manage_event_render_template'))
    elif role == 'student':
        return redirect(url_for('user_side.user_side_render_template'))
    return redirect(url_for('user_auth.admin_login_render_template'))


#create blueprint/routes
user_auth = Blueprint('user_auth', __name__)
@user_auth.route('/admin_login_render_template', methods=['GET', 'POST'])
def admin_login_render_template():

    if current_user.is_authenticated:
        return redirect_user_based_on_role(current_user.role)
    
    if request.method == 'POST':
        try:
            email = request.form.get('emailT')
            password = request.form.get('passwordT')

            if not email or not password:
                return jsonify({'success': False, 'message': 'Please input email and password'})
            
            # Fetch user by email and password
            valid_user = User.query.filter_by(
                email=email,
                password=password
                ).first()
            
            if valid_user:
                login_user(valid_user,remember=True)
                if valid_user.role in ['admin', 'ssg']:  
                    return jsonify({
                            'success': True, 
                            'message': 'Login Successfully',
                            'redirect_url': url_for('admin_manage_event.manage_event_render_template')
                        })
                else:
                    return jsonify({
                            'success': True, 
                            'message': 'Login Successfully',
                            'redirect_url': url_for('user_side.user_side_render_template')
                        })

            return jsonify({'success': False, 'message': 'Invalid credentials'})

        except Exception as e:
            return jsonify({'success': False, 'message': f'Error {e}'})

    return render_template('public_user_auth.html')


#logout user
@user_auth.route('/user_logout', methods=['POST'])  # Ensure this is POST, not GET
@login_required
def user_logout():
    logout_user()  # Example if using Flask-Login
    return jsonify({
        'success': True,
        'redirect_url': url_for('user_auth.admin_login_render_template')
    })


#signup
# Function to generate a unique 6-digit Student ID
def generate_student_id():
    while True:
        random_id = str(random.randint(100000, 999999))  # Generates exactly 6 digits
        if not User.query.filter_by(student_ID=random_id).first():  # Ensures uniqueness
            return random_id



# User Signup Route
@user_auth.route('/user_signup', methods=['POST', 'GET'])
def user_signup():
    if current_user.is_authenticated:
        return redirect_user_based_on_role(current_user.role)
    departments = Department.query.all()  # Fetch departments

    if request.method == 'POST':
        try:
            # Get form data
            first_name = request.form.get('first_nameT')
            last_name = request.form.get('last_nameT')
            email = request.form.get('emailT')
            password = request.form.get('passwordT')
            department_id = request.form.get('departmentT')

            # Validate required fields
            if not all([first_name, last_name, email, password, department_id]):
                return jsonify({'success': False, 'message': 'All fields are required.'})

            # Validate email format
            email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
            if not re.match(email_pattern, email):
                return jsonify({'success': False, 'message': 'Invalid email format.'})

            # Check if user already exists
            
            # Generate a unique student ID
            student_ID = generate_student_id()
            # Hash password before saving

            #hashed_password = generate_password_hash(password, method='pbkdf2:sha256')

            existing_student_ID = User.query.filter_by(
            student_ID=student_ID
            ).first()
            existing_student_name = User.query.filter_by(
            first_name=first_name,
            last_name=last_name
            ).first()
            existing_student_email= User.query.filter_by(
            email=email
            ).first()

            if existing_student_ID:
                return jsonify({'success': False, 'message': 'Student ID already used'})
            if existing_student_name:
                return jsonify({'success': False, 'message': 'Student already exists'})
            if existing_student_email:
                return jsonify({'success': False, 'message': 'Student email already used'})
            

            

            # Create new user
            new_user = User(
                student_ID=student_ID,
                first_name=first_name,
                last_name=last_name,
                email=email,
                password=password,  # Store hashed password
                date_registered=datetime.now(manila_tz).replace(second=0, microsecond=0),
                department_id=department_id
            )

            # Save to database
            db.session.add(new_user)
            db.session.commit()

            return jsonify({
                'success': True, 
                'message': 'Signup successful! You can now log in.',
                'redirect_url': url_for('user_auth.admin_login_render_template')
            })

        except Exception as e:
            db.session.rollback()  # Rollback if there's an error
            return jsonify({'success': False, 'message': str(e)})

    return render_template('user_signup.jinja2', departments=departments if departments else [])