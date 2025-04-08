from flask import Blueprint, render_template, abort, send_from_directory
from flask_login import login_required, current_user
from app.models.result import Result
from app.models.study_material import StudyMaterial
from app.models.subject import Subject
from app.models.department import Department
from flask import current_app
import os

bp = Blueprint('student', __name__)

@bp.route('/my-results')
@login_required
def my_results():
    if not current_user.student_id:
        abort(403)  # Forbidden if user is not a student
        
    # Get all results for the student
    results = Result.query.filter_by(
        student_id=current_user.student_id
    ).order_by(Result.declaration_date.desc()).all()
    
    return render_template('student/my_results.html', results=results)

@bp.route('/my-result/<string:exam_id>')
@login_required
def view_result(exam_id):
    if not current_user.student_id:
        abort(403)
        
    result = Result.query.filter_by(
        student_id=current_user.student_id,
        exam_id=exam_id
    ).first_or_404()
    
    return render_template('student/result_view.html', result=result)

@bp.route('/study-materials')
@login_required
def study_materials():
    if not current_user.has_role('student'):
        abort(403)  # Forbidden if user is not a student
        
    # Get study materials for student's department and semester
    materials = StudyMaterial.query.filter_by(
        department_id=current_user.department_id,
        semester=current_user.semester
    ).all()
    
    return render_template('student/study_materials.html', materials=materials)

@bp.route('/download-material/<int:material_id>')
@login_required
def download_material(material_id):
    if not current_user.has_role('student'):
        abort(403)
        
    material = StudyMaterial.query.get_or_404(material_id)
    
    # Only allow students to download materials from their department and semester
    if material.department_id != current_user.department_id or material.semester != current_user.semester:
        abort(403)
    
    upload_dir = os.path.join(current_app.config['UPLOAD_FOLDER'], 'study_materials')
    return send_from_directory(upload_dir, material.file_path, as_attachment=True)
