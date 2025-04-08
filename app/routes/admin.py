from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify, current_app
from flask_security import roles_required, roles_accepted, current_user, login_required
from flask_security.utils import hash_password
from ..models.user import User, Role
from ..models.department import Department
from ..models.project import Project
from ..models.result import Result
from ..models.subject import Subject
from ..models.study_material import StudyMaterial
from ..forms.admin import UserCreationForm, BulkUserUploadForm, ResultUploadForm
from ..forms.study_material import StudyMaterialForm
from ..extensions import db
from datetime import datetime
import pandas as pd
import os

bp = Blueprint('admin', __name__, url_prefix='/admin')

@bp.route('/')
@roles_required('admin')
def index():
    # Get all users and pending users
    pending_users = User.query.filter_by(is_approved=False).all()
    
    # Get users by role
    hod_role = Role.query.filter_by(name='hod').first()
    lecturer_role = Role.query.filter_by(name='lecturer').first()
    student_role = Role.query.filter_by(name='student').first()
    lab_assistant_role = Role.query.filter_by(name='lab_assistant').first()
    librarian_role = Role.query.filter_by(name='librarian').first()
    store_officer_role = Role.query.filter_by(name='store_officer').first()
    
    hods = User.query.filter(User.roles.contains(hod_role)).all() if hod_role else []
    lecturers = User.query.filter(User.roles.contains(lecturer_role)).all() if lecturer_role else []
    students = User.query.filter(User.roles.contains(student_role)).all() if student_role else []
    lab_assistants = User.query.filter(User.roles.contains(lab_assistant_role)).all() if lab_assistant_role else []
    librarians = User.query.filter(User.roles.contains(librarian_role)).all() if librarian_role else []
    store_officers = User.query.filter(User.roles.contains(store_officer_role)).all() if store_officer_role else []
    
    # Get departments
    departments = Department.query.all()
    
    # Get projects
    projects = Project.query.all()
    
    return render_template('admin/index.html', 
                         pending_users=pending_users,
                         hods=hods,
                         lecturers=lecturers,
                         students=students,
                         lab_assistants=lab_assistants,
                         librarians=librarians,
                         store_officers=store_officers,
                         departments=departments,
                         projects=projects)

@bp.route('/approve_user/<int:user_id>', methods=['POST'])
@roles_required('admin')
def approve_user(user_id):
    user = User.query.get_or_404(user_id)
    user.is_approved = True
    user.approval_date = datetime.utcnow()
    user.approved_by = current_user
    db.session.commit()
    flash(f'User {user.email} has been approved.', 'success')
    return redirect(url_for('admin.index'))

@bp.route('/reject_user/<int:user_id>', methods=['POST'])
@roles_required('admin')
def reject_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    flash(f'User {user.email} has been rejected and removed.', 'success')
    return redirect(url_for('admin.index'))

@bp.route('/create_department', methods=['POST'])
@roles_required('admin')
def create_department():
    name = request.form.get('name')
    hod_id = request.form.get('hod_id')
    
    if not name:
        flash('Department name is required.', 'error')
        return redirect(url_for('admin.index', _anchor='departments'))
    
    if Department.query.filter_by(name=name).first():
        flash('Department with this name already exists.', 'error')
        return redirect(url_for('admin.index', _anchor='departments'))
    
    department = Department(name=name)
    if hod_id:
        department.hod_id = hod_id
    
    db.session.add(department)
    db.session.commit()
    
    flash(f'Department {name} has been created.', 'success')
    return redirect(url_for('admin.index', _anchor='departments'))

@bp.route('/edit_department/<int:dept_id>', methods=['POST'])
@roles_required('admin')
def edit_department(dept_id):
    department = Department.query.get_or_404(dept_id)
    name = request.form.get('name')
    hod_id = request.form.get('hod_id')
    
    if not name:
        flash('Department name is required.', 'error')
        return redirect(url_for('admin.index', _anchor='departments'))
    
    existing = Department.query.filter_by(name=name).first()
    if existing and existing.id != dept_id:
        flash('Department with this name already exists.', 'error')
        return redirect(url_for('admin.index', _anchor='departments'))
    
    department.name = name
    department.hod_id = hod_id if hod_id else None
    db.session.commit()
    
    flash(f'Department {name} has been updated.', 'success')
    return redirect(url_for('admin.index', _anchor='departments'))

@bp.route('/delete_department/<int:dept_id>', methods=['POST'])
@roles_required('admin')
def delete_department(dept_id):
    department = Department.query.get_or_404(dept_id)
    name = department.name
    
    # Check if department has any users
    if department.students or department.lecturers:
        flash('Cannot delete department that has users assigned to it.', 'error')
        return redirect(url_for('admin.index', _anchor='departments'))
    
    db.session.delete(department)
    db.session.commit()
    
    flash(f'Department {name} has been deleted.', 'success')
    return redirect(url_for('admin.index', _anchor='departments'))

@bp.route('/users', methods=['GET'])
@roles_required('admin')
def users():
    # Get all users
    users = User.query.order_by(User.created_at.desc()).all()
    
    # Get role counts for the stats cards
    role_counts = {}
    roles = Role.query.all()
    for role in roles:
        role_counts[role.name] = User.query.join(User.roles).filter(Role.name == role.name).count()
    
    # Get all departments for filtering
    departments = Department.query.all()
    
    # Get form for CSRF token
    form = UserCreationForm()

    return render_template('admin/users.html', 
                         users=users,
                         roles=roles,
                         departments=departments,
                         form=form,
                         role_counts=role_counts)

@bp.route('/users/create', methods=['POST'])
@roles_required('admin')
def create_user():
    form = UserCreationForm(request.form)
    
    if form.validate():
        try:
            # Check if email already exists (case-insensitive)
            existing_user = User.query.filter(User.email.ilike(form.email.data)).first()
            if existing_user:
                return jsonify({'email': ['This email address is already registered']}), 400

            # Create new user
            user = User(
                email=form.email.data.lower(),  # Store email in lowercase
                first_name=form.first_name.data,
                last_name=form.last_name.data,
                phone=form.phone.data,
                department_id=int(form.department.data),
                password=hash_password('changeme123'),
                is_approved=True,
                created_at=datetime.utcnow()
            )
            
            # Get selected roles
            role_names = request.form.getlist('roles')
            if not role_names:
                return jsonify({'roles': ['Please select at least one role']}), 400
                
            for role_name in role_names:
                role = Role.query.filter_by(name=role_name).first()
                if role:
                    user.roles.append(role)
                else:
                    return jsonify({'roles': ['Invalid role selected']}), 400
            
            db.session.add(user)
            db.session.commit()
            return jsonify({
                'status': 'success', 
                'message': 'User created successfully! Temporary password: changeme123'
            })
            
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f'Error creating user: {str(e)}')
            if 'UNIQUE constraint' in str(e) and 'email' in str(e):
                return jsonify({'email': ['This email address is already registered']}), 400
            return jsonify({'error': 'An error occurred while creating the user'}), 500
    
    # Format validation errors
    errors = {}
    for field, field_errors in form.errors.items():
        errors[field] = field_errors
    return jsonify(errors), 400

@bp.route('/bulk_upload', methods=['GET', 'POST'])
@roles_required('admin')
def bulk_upload():
    form = BulkUserUploadForm()
    if form.validate_on_submit():
        try:
            print(f"Processing file upload with roles: {form.default_roles.data}")
            df = pd.read_csv(request.files[form.csv_file.name])
            print(f"CSV columns: {df.columns.tolist()}")
            
            # Get or create selected roles
            user_roles = []
            for role_name in form.default_roles.data:
                role = Role.query.filter_by(name=role_name).first()
                if not role:
                    role = Role(name=role_name)
                    db.session.add(role)
                    db.session.flush()
                user_roles.append(role)
            
            success_count = 0
            error_count = 0
            
            for _, row in df.iterrows():
                try:
                    # Check if user already exists
                    if User.query.filter_by(email=row['email']).first():
                        error_count += 1
                        continue
                    
                    # Get or create department
                    department = None
                    if 'department' in row and row['department']:
                        department = Department.query.filter_by(name=row['department']).first()
                        if not department:
                            department = Department(name=row['department'])
                            db.session.add(department)
                            db.session.flush()  # Get the ID without committing
                    
                    # Handle additional roles from CSV if present
                    roles_to_assign = user_roles.copy()  # Start with the roles selected in the form
                    if 'roles' in row and row['roles']:
                        additional_role_names = [r.strip() for r in str(row['roles']).split(',')]
                        for role_name in additional_role_names:
                            if role_name:  # Skip empty strings
                                role = Role.query.filter_by(name=role_name).first()
                                if not role:
                                    role = Role(name=role_name)
                                    db.session.add(role)
                                    db.session.flush()
                                if role not in roles_to_assign:
                                    roles_to_assign.append(role)
                    
                    user = User(
                        email=row['email'],
                        password=hash_password('changeme123'),  # Temporary password
                        first_name=row['first_name'],
                        last_name=row['last_name'],
                        phone=str(row['phone']),
                        department_id=department.id if department else None,
                        active=True,
                        is_approved=True,
                        approval_date=datetime.utcnow(),
                        approved_by=current_user,
                        roles=roles_to_assign
                    )
                    db.session.add(user)
                    success_count += 1
                except Exception as e:
                    error_count += 1
                    continue
            
            db.session.commit()
            flash(f'Bulk upload completed. {success_count} users created, {error_count} failed. '
                  f'Temporary password for all users: changeme123', 'success')
            return redirect(url_for('admin.index'))
            
        except Exception as e:
            print(f"Error processing file: {str(e)}")
            flash(f'Error processing file: {str(e)}', 'error')
            return redirect(url_for('admin.index'))
    
    return render_template('admin/bulk_upload.html', form=form)

@bp.route('/api/departments/<int:dept_id>')
@roles_required('admin')
def get_department(dept_id):
    department = Department.query.get_or_404(dept_id)
    return jsonify({
        'id': department.id,
        'name': department.name,
        'hod_id': department.hod_id if department.hod else None
    })

@bp.route('/project/<int:project_id>')
@roles_required('admin')
def get_project(project_id):
    project = Project.query.get_or_404(project_id)
    return jsonify({
        'id': project.id,
        'name': project.name,
        'description': project.description,
        'department_id': project.department_id,
        'group_leader': project.group_leader,
        'members': project.members,
        'marks': project.marks
    })

@bp.route('/create_project', methods=['POST'])
@roles_required('admin')
def create_project():
    name = request.form.get('name')
    if not name:
        flash('Project name is required.', 'error')
        return redirect(url_for('admin.index', _anchor='projects'))
    
    project = Project(
        name=name,
        description=request.form.get('description', ''),
        department_id=request.form.get('department_id'),
        group_leader=request.form.get('group_leader'),
        members=request.form.get('members'),
        marks=None  # Marks will be added through Jury file
    )
    
    db.session.add(project)
    db.session.commit()
    
    flash(f'Project {name} has been created.', 'success')
    return redirect(url_for('admin.index', _anchor='projects'))

@bp.route('/edit_project/<int:project_id>', methods=['POST'])
@roles_required('admin')
def edit_project(project_id):
    project = Project.query.get_or_404(project_id)
    
    name = request.form.get('name')
    if not name:
        flash('Project name is required.', 'error')
        return redirect(url_for('admin.index', _anchor='projects'))
    
    project.name = name
    project.description = request.form.get('description', '')
    project.department_id = request.form.get('department_id')
    project.group_leader = request.form.get('group_leader')
    project.members = request.form.get('members')
    # Don't update marks - they will be added through Jury file
    
    db.session.commit()
    
    flash(f'Project {name} has been updated.', 'success')
    return redirect(url_for('admin.index', _anchor='projects'))

@bp.route('/delete_project/<int:project_id>', methods=['POST'])
@roles_required('admin')
def delete_project(project_id):
    project = Project.query.get_or_404(project_id)
    name = project.name
    
    db.session.delete(project)
    db.session.commit()
    
    flash(f'Project {name} has been deleted.', 'success')
    return redirect(url_for('admin.index', _anchor='projects'))

@bp.route('/import_projects', methods=['POST'])
@roles_required('admin')
def import_projects():
    if 'csv_file' not in request.files:
        flash('No file uploaded.', 'error')
        return redirect(url_for('admin.index', _anchor='projects'))
    
    file = request.files['csv_file']
    if file.filename == '':
        flash('No file selected.', 'error')
        return redirect(url_for('admin.index', _anchor='projects'))
    
    if not file.filename.endswith('.csv'):
        flash('Please upload a CSV file.', 'error')
        return redirect(url_for('admin.index', _anchor='projects'))
    
    try:
        # Save the file temporarily
        temp_path = os.path.join(current_app.config['UPLOAD_FOLDER'], 'temp.csv')
        file.save(temp_path)
        
        # Import projects from CSV
        projects = Project.import_from_csv(temp_path)
        
        # Add all projects to database
        for project in projects:
            db.session.add(project)
        
        db.session.commit()
        os.remove(temp_path)  # Clean up temp file
        
        flash(f'Successfully imported {len(projects)} projects.', 'success')
    except Exception as e:
        flash(f'Error importing projects: {str(e)}', 'error')
    
    return redirect(url_for('admin.index', _anchor='projects'))

@bp.route('/edit_user/<int:user_id>', methods=['GET', 'POST'])
@roles_required('admin')
def edit_user(user_id):
    user = User.query.get_or_404(user_id)
    form = UserCreationForm(obj=user)
    
    if request.method == 'GET':
        # Set initial form data
        form.email.data = user.email
        form.first_name.data = user.first_name
        form.last_name.data = user.last_name
        form.phone.data = user.phone
        form.department.data = user.department_id if user.department else 0
        form.roles.data = [role.name for role in user.roles]
    
    if form.validate_on_submit():
        # Get the department
        department = Department.query.get(form.department.data) if form.department.data != 0 else None
        
        # Get or create the roles
        user_roles = []
        for role_name in form.roles.data:
            role = Role.query.filter_by(name=role_name).first()
            if not role:
                role = Role(name=role_name)
                db.session.add(role)
                db.session.flush()
            user_roles.append(role)
        
        # Update user details
        user.email = form.email.data
        user.first_name = form.first_name.data
        user.last_name = form.last_name.data
        user.phone = form.phone.data
        user.department_id = department.id if department else None
        user.roles = user_roles
        
        db.session.commit()
        flash(f'User {user.email} has been updated.', 'success')
        return redirect(url_for('admin.index'))
    
    return render_template('admin/edit_user.html', form=form, user=user)

@bp.route('/delete_user/<int:user_id>', methods=['POST'])
@roles_required('admin')
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    email = user.email
    db.session.delete(user)
    db.session.commit()
    flash(f'User {email} has been deleted.', 'success')
    return redirect(url_for('admin.index'))

@bp.route('/upload-results', methods=['GET', 'POST'])
@login_required
@roles_required('admin')
def upload_results():
    form = ResultUploadForm()
    if form.validate_on_submit():
        try:
            csv_file = form.result_file.data
            print(f"Reading CSV file...")
            # Save file temporarily
            csv_file.save('temp_results.csv')
            # Read CSV file into pandas DataFrame
            df = pd.read_csv('temp_results.csv')
            print(f"Found {len(df)} rows in CSV")
            
            success_count = 0
            # Process each row in the DataFrame
            for _, row in df.iterrows():
                try:
                    # Create or update result record
                    result = Result.query.filter_by(
                        student_id=row['St_Id'],
                        exam_id=row['examid']
                    ).first()
                    
                    if not result:
                        result = Result()
                        print(f"Creating new result for student {row['St_Id']}")
                    else:
                        print(f"Updating existing result for student {row['St_Id']}")
                    
                    # Map CSV data to Result model fields
                    result.student_id = row['St_Id']
                    result.exam_id = row['examid']
                    result.exam_type = row['extype']
                    result.exam_name = row['exam']
                    # Parse declaration date with the correct format
                    try:
                        result.declaration_date = pd.to_datetime(row['DECLARATIONDATE'], format='%m/%d/%Y %I:%M:%S %p').date()
                    except Exception as e:
                        print(f"Error parsing date {row['DECLARATIONDATE']}: {str(e)}")
                        result.declaration_date = None
                    result.academic_year = row['AcademicYear']
                    result.semester = int(row['sem'])
                    result.student_name = row['name']
                    result.institute_code = row['instcode']
                    result.institute_name = row['instName']
                    result.course_name = row['CourseName']
                    result.branch_code = str(row['BR_CODE'])
                    result.branch_name = row['BR_NAME']
                    
                    # Store subject results as JSON
                    subjects = {}
                    for i in range(1, 16):  # Process SUB1 to SUB15
                        sub_code = row.get(f'SUB{i}')
                        if pd.notna(sub_code):
                            subjects[f'SUB{i}'] = {
                                'code': sub_code,
                                'name': row.get(f'SUB{i}NA', ''),
                                'credits': float(row.get(f'SUB{i}CR', 0)),
                                'grade': row.get(f'SUB{i}GR', ''),
                            }
                    result.subject_results = subjects
                    
                    # Calculate total credits and grade points
                    total_credits = 0
                    total_grade_points = 0
                    for sub in subjects.values():
                        total_credits += sub['credits']
                        grade = sub['grade']
                        # Convert grade to grade points
                        grade_points = {
                            'AA': 10, 'AB': 9, 'BB': 8, 'BC': 7, 'CC': 6, 'CD': 5, 'DD': 4, 'FF': 0
                        }.get(grade, 0)
                        total_grade_points += sub['credits'] * grade_points
                    
                    result.total_credits = total_credits
                    result.total_grade_points = total_grade_points
                    result.sgpa = total_grade_points / total_credits if total_credits > 0 else 0.0
                    result.result_status = 'FAIL' if 'FF' in [s['grade'] for s in subjects.values()] else 'PASS'
                    
                    db.session.add(result)
                    success_count += 1
                    
                except Exception as e:
                    print(f"Error processing row for student {row.get('St_Id', 'unknown')}: {str(e)}")
                    continue
            
            try:
                print(f"Committing {success_count} results to database...")
                db.session.commit()
                flash(f'Successfully uploaded {success_count} results!', 'success')
            except Exception as e:
                print(f"Error during commit: {str(e)}")
                db.session.rollback()
                flash(f'Error saving results to database: {str(e)}', 'danger')
            
            return redirect(url_for('admin.upload_results'))
            
        except Exception as e:
            print(f"Error processing CSV file: {str(e)}")
            db.session.rollback()
            flash(f'Error uploading results: {str(e)}', 'danger')
            return redirect(url_for('admin.upload_results'))
    
    return render_template('admin/upload_results.html', form=form)

@bp.route('/view-results')
@login_required
@roles_required('admin')
def view_results():
    page = request.args.get('page', 1, type=int)
    branch = request.args.get('branch', '')
    exam_type = request.args.get('exam_type', '')
    semester = request.args.get('semester', '')
    
    # Base query
    query = Result.query
    
    # Apply filters
    if branch:
        query = query.filter(Result.branch_code == branch)
    if exam_type:
        query = query.filter(Result.exam_type == exam_type)
    if semester:
        query = query.filter(Result.semester == semester)
    
    # Get unique filter options for dropdowns
    branches = db.session.query(Result.branch_code, Result.branch_name).distinct().all()
    exam_types = db.session.query(Result.exam_type).distinct().all()
    semesters = db.session.query(Result.semester).distinct().order_by(Result.semester).all()
    
    # Paginate results
    results = query.order_by(Result.declaration_date.desc()).paginate(
        page=page, per_page=50, error_out=False)
    
    return render_template('admin/view_results.html',
                         results=results,
                         branches=branches,
                         exam_types=exam_types,
                         semesters=semesters,
                         current_branch=branch,
                         current_exam_type=exam_type,
                         current_semester=semester)

@bp.route('/result/<string:student_id>/<string:exam_id>')
@login_required
def view_result_details(student_id, exam_id):
    result = Result.query.filter_by(
        student_id=student_id,
        exam_id=exam_id
    ).first_or_404()
    
    # Check if user has permission to view this result
    if not current_user.has_role('admin') and current_user.student_id != student_id:
        abort(403)
    
    return render_template('admin/result_details.html', result=result)

@bp.route('/get_semesters/<int:dept_id>')
@roles_required('admin')
def get_semesters(dept_id):
    # Get unique semesters for the department from subjects
    semesters = db.session.query(Subject.semester)\
        .filter(Subject.department_id == dept_id)\
        .distinct()\
        .order_by(Subject.semester)\
        .all()
    return jsonify([sem[0] for sem in semesters])

@bp.route('/get_subjects/<int:dept_id>/<int:semester>')
@login_required
def get_subjects(dept_id, semester):
    # Get unique subjects to avoid duplicates
    subjects = Subject.query\
        .filter_by(department_id=dept_id, semester=semester)\
        .distinct(Subject.code)\
        .order_by(Subject.name)\
        .all()
    return jsonify([{'id': s.id, 'name': s.name, 'code': s.code} for s in subjects])

@bp.route('/study_materials')
@login_required
@roles_accepted('admin', 'faculty')
def study_materials():
    # Create form instance
    form = StudyMaterialForm()
    
    # Set choices for department dropdown
    departments = Department.query.all()
    form.department_id.choices = [(d.id, d.name) for d in departments]
    
    # Initialize subject choices as empty list
    form.subject_id.choices = []
    
    # Get all study materials
    materials = StudyMaterial.query.all()
    
    return render_template('admin/tabs/study_materials.html', 
                         form=form,
                         materials=materials)

@bp.route('/upload_study_material', methods=['POST'])
@login_required
@roles_accepted('admin', 'faculty')
def upload_study_material():
    form = StudyMaterialForm(request.form)
    
    # Set choices for department dropdown
    departments = Department.query.all()
    form.department_id.choices = [(d.id, d.name) for d in departments]
    
    # Set choices for subject dropdown based on selected department and semester
    if form.department_id.data and form.semester.data:
        subjects = Subject.query.filter_by(
            department_id=form.department_id.data,
            semester=form.semester.data
        ).all()
        form.subject_id.choices = [(s.id, s.name) for s in subjects]
    else:
        form.subject_id.choices = []
    
    if form.validate_on_submit():
        department_id = form.department_id.data
        semester = form.semester.data
        subject_id = form.subject_id.data
        file = request.files['file']
        
        if not all([department_id, semester, subject_id, file]):
            flash('All fields are required', 'error')
            return redirect(url_for('admin.study_materials'))
        
        if file:
            # Create uploads directory if it doesn't exist
            upload_dir = os.path.join(current_app.config['UPLOAD_FOLDER'], 'study_materials')
            os.makedirs(upload_dir, exist_ok=True)
            
            # Save file
            filename = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{file.filename}"
            file_path = os.path.join(upload_dir, filename)
            file.save(file_path)
            
            # Create study material record
            material = StudyMaterial(
                semester=semester,
                department_id=department_id,
                subject_id=subject_id,
                file_path=filename,
                uploaded_by=current_user.id
            )
            db.session.add(material)
            db.session.commit()
            
            flash('Study material uploaded successfully', 'success')
        else:
            flash('Please select a file to upload', 'error')
        
        return redirect(url_for('admin.study_materials'))
    
    return render_template('admin/tabs/study_materials.html', form=form)

@bp.route('/delete_study_material/<int:material_id>', methods=['POST'])
@login_required
def delete_study_material(material_id):
    material = StudyMaterial.query.get_or_404(material_id)
    
    # Only allow faculty members to delete their own uploads or admins to delete any
    if not current_user.has_role('admin') and material.uploaded_by != current_user.id:
        flash('You can only delete your own uploaded materials.', 'error')
        return redirect(url_for('admin.study_materials'))
    
    # Delete file
    file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], 'study_materials', material.file_path)
    if os.path.exists(file_path):
        os.remove(file_path)
    
    # Delete database record
    db.session.delete(material)
    db.session.commit()
    
    flash('Study material deleted successfully', 'success')
    return redirect(url_for('admin.study_materials'))
