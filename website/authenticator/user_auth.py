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


from itsdangerous import URLSafeTimedSerializer
from website import mail
from flask_mail import Message
from itsdangerous import SignatureExpired, BadSignature

from website import dtc_email


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

                if not valid_user.is_verified:
                    return jsonify({'success': False, 'message': 'Account not verified. Please check your email.'})


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


# Secure email verification
def send_verification_email(email, confirm_url):
    msg = Message('Confirm Your Email', sender=dtc_email, recipients=[email])
    msg.body = f'Click the link to verify your email: {confirm_url}'
    mail.send(msg)

# Secure serializer (initialize in flask_app)
def get_serializer():
    return URLSafeTimedSerializer('ion21')  # Use actual secret key


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
                department_id=department_id,
                is_verified=False
            )

            # Save to database
            db.session.add(new_user)
            db.session.commit()

           # Generate verification token
            serializer = get_serializer()
            token = serializer.dumps(email, salt='email-confirm')
            confirm_url = url_for('user_auth.confirm_email', token=token, _external=True)

            # Send verification email
            send_verification_email(email, confirm_url)

            return jsonify({
                'success': True,
                'message': 'Signup successful! Please check your email inbox or spam to verify your account.',
                'redirect_url': url_for('user_auth.admin_login_render_template')
            })

        except Exception as e:
            db.session.rollback()  # Rollback if there's an error
            return jsonify({'success': False, 'message': str(e)})

    return render_template('user_signup.jinja2', departments=departments if departments else [])



# Confirm verification with 5-minute expiration
@user_auth.route('/confirm_email/<token>', methods=['GET'])
def confirm_email(token):
    serializer = get_serializer()
    try:
        # Validate the token with a  expiration
        email = serializer.loads(token, salt='email-confirm', max_age=500)

        user = User.query.filter_by(email=email).first()
        if not user:
            return render_template("email_verification.jinja2", message="Invalid or expired token", success=False)

        if user.is_verified:
            return render_template("email_verification.jinja2", message="This email has already been verified.", success=False)

        # Mark user as verified
        user.is_verified = True
        db.session.commit()

        return render_template("email_verification.jinja2", message="Your email has been verified successfully!", success=True)

    except SignatureExpired:
        return render_template("email_verification.jinja2", message="The confirmation link has expired. Please request a new one.", success=False)

    except BadSignature:
        return render_template("email_verification.jinja2", message="Invalid confirmation link.", success=False)




#verify resend
@user_auth.route('/resend_verification_email', methods=['POST'])
def resend_verification_email():
    email = request.form.get('emailT')

    if not email:
        return render_template("email_verification.jinja2", message="Email is required.", success=False)

    user = User.query.filter_by(email=email).first()
    if not user:
        return render_template("email_verification.jinja2", message="User not found.", success=False)

    if user.is_verified:
        return render_template("email_verification.jinja2", message="This email is already verified.", success=False)

    # Generate a new verification token
    serializer = get_serializer()
    token = serializer.dumps(email, salt='email-confirm')
    confirm_url = url_for('user_auth.confirm_email', token=token, _external=True)

    # Send the verification email
    send_verification_email(email, confirm_url)

    return render_template("email_verification.jinja2", message="A new verification email has been sent. Check your email inbox or spam.", success=False)




# Forgot Password Route (Request Reset)
@user_auth.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        email = request.form.get('emailT')

        # Check if email exists
        user = User.query.filter_by(email=email).first()
        if not user:
            return jsonify({'success': False, 'message': 'Email not found'})
        
        if not user.is_verified:
            return jsonify({'success': False, 'message': 'This email is not verified. Please verify it first'})

        # Generate reset token
        serializer = get_serializer()
        token = serializer.dumps(email, salt='password-reset')
        reset_url = url_for('user_auth.reset_password', token=token, _external=True)

        # Send reset email
        msg = Message('Password Reset Request', sender=dtc_email, recipients=[email])
        msg.body = f'Click the link to reset your password: {reset_url}'
        mail.send(msg)

        return jsonify({'success': True, 'message': 'Password reset link sent. Check your email inbox or spam.'})

    return render_template('forgot_password.jinja2')


# Reset Password Route (Token Validation)
@user_auth.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    serializer = get_serializer()
    try:
        email = serializer.loads(token, salt='password-reset', max_age=500)  # Token expires in minutes
        user = User.query.filter_by(email=email).first()
        
        if request.method == 'POST':
            new_password = request.form.get('new_passwordT')

            if not new_password:
                return jsonify({'success': False, 'message': 'Password cannot be empty'})
            
            if len(new_password) < 6:
                return jsonify({'success': False, 'message': 'Password must be greater than 6 characters'})

            # Update password (plaintext for now, but hashing recommended)
            user.password = new_password  # Change to generate_password_hash(new_password) in production
            db.session.commit()

            return jsonify({'success': True, 'message': 'Password reset successfully', 'redirect_url': url_for('user_auth.admin_login_render_template')})

        return render_template('reset_password.jinja2', token=token)

    except SignatureExpired:
        return render_template("reset_password.jinja2", message="Reset link expired.", success=False)
    except BadSignature:
        return render_template("reset_password.jinja2", message="Invalid reset link.", success=False)


#student change password
@user_auth.route('/change_password', methods=['POST'])
@login_required
def change_password():
    try:
        current_password = request.form.get('current_password')
        new_password = request.form.get('new_password')

        # Validate input
        if not current_password or not new_password:
            return jsonify({'success': False, 'message': 'All fields are required'})

        if len(new_password) != 6:
            return jsonify({'success': False, 'message': 'New password must be exactly 6 characters'})
        
        if new_password == current_user.password or  new_password==current_password:
            return jsonify({'success': False, 'message': 'Please provide a new password'})

        # Check if the current password matches the stored password
        if current_user.password != current_password:
            return jsonify({'success': False, 'message': 'Current password is incorrect'})

        # Update the password
        current_user.password = new_password
        db.session.commit()

        return jsonify({'success': True, 'message': 'Password updated successfully'})

    except Exception as e:
        return jsonify({'success': False, 'message': f'Error: {e}'})
