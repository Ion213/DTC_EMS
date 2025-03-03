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

from pytz import timezone
manila_tz = timezone('Asia/Manila')
from datetime import datetime
from sqlalchemy import or_,and_,extract
from sqlalchemy.sql import func

from website import db
from website.models.database_models import Department,User

admin_manage_department = Blueprint('admin_manage_department', __name__)

#render departmnet template
@admin_manage_department.route('/manage_department_render_template', methods=['GET'])
@login_required
@role_required('admin')
def manage_department_render_template():
    return render_template('admin_manage_department.jinja2')

#render department data
@admin_manage_department.route('/render_department_data', methods=['GET'])
@login_required
@role_required('admin')
def render_department_data():
    try:
        departments = Department.query.all()
        all_departments = []
        
        for d in departments:
            department_data = {
                'id': d.id,
                'department_name': d.department_name,
                'year': d.year,
                'section': d.section
            }
            
            all_departments.append(department_data)

        return jsonify({'data': all_departments})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

#add department
@admin_manage_department.route('/add_department', methods=['POST'])
@login_required
@role_required('admin')
def add_department():
    try:

        department_nameV = request.form.get('department_nameT')
        yearV = request.form.get('yearT')
        sectionV = request.form.get('sectionT')

        if not department_nameV:
            return jsonify({'success': False, 'message': 'Department Name cannot be Empty'})
        if not yearV:
            return jsonify({'success': False, 'message': 'Department Year cannot be Empty'})
        if not sectionV:
            return jsonify({'success': False, 'message': 'Department Section cannot be Empty'})

        existing_department = Department.query.filter_by(
            department_name=department_nameV,
            year=yearV,
            section=sectionV
            ).first()
        if existing_department:
            return jsonify({'success': False, 'message': 'Department already exist'})
        
        departmentAdd = Department(
            department_name=department_nameV, 
            year=yearV,
            section=sectionV
            )
        db.session.add(departmentAdd)
        db.session.commit()
        return jsonify({'success': True})

    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)})
    
#delete department  
@admin_manage_department.route('/delete_department/<int:department_id>', methods=['DELETE'])
@login_required
@role_required('admin')
def delete_department(department_id):
    try:
        # Fetch the event by ID and delete it
        departmentDel = Department.query.get(department_id)
        if not departmentDel:
            return jsonify({'success': False, 'message': 'Department not found'})
        
        User.query.filter_by(department_id=departmentDel.id).delete()

        db.session.delete(departmentDel)
        db.session.commit()
        return jsonify({'success': True, 'message': 'Department deleted successfully'})

    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)})
    
#update department
@admin_manage_department.route('/update_department', methods=['PUT'])
@login_required
@role_required('admin')
def update_department():
    try:
        selected_department_id = request.form.get('selected_department_idT')
        update_department_name = request.form.get('update_department_nameT')
        update_department_year = request.form.get('update_yearT')
        update_department_section = request.form.get('update_sectionT')

        if not selected_department_id:
            return jsonify({'success': False, 'message': 'Department not found'})


        if not update_department_name:
            return jsonify({'success': False, 'message': 'Department name cannot be empty'})

        if not update_department_year:
            return jsonify({'success': False, 'message': 'Department Year cannot be empty'})
        
        if not update_department_section:
            return jsonify({'success': False, 'message': 'Department Section cannot be empty'})


        existing_department = Department.query.filter(
            Department.id != selected_department_id, 
            Department.department_name ==update_department_name,
            Department.year==update_department_year,
            Department.section==update_department_section
            ).first()
        
        if existing_department:
            return jsonify({'success': False, 'message': 'Department already exist'})

        departmentUp = Department.query.get(selected_department_id)
        departmentUp.department_name = update_department_name
        departmentUp.year = update_department_year
        departmentUp.section = update_department_section
        db.session.commit()

        return jsonify({'success': True, 'message': 'Department updated successfully'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)})