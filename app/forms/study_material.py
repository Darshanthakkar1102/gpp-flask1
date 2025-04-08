from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import SelectField, SubmitField
from wtforms.validators import DataRequired

class StudyMaterialForm(FlaskForm):
    department_id = SelectField('Department', coerce=int, validators=[DataRequired()])
    semester = SelectField('Semester', choices=[(str(i), str(i)) for i in range(1, 9)], validators=[DataRequired()])
    subject_id = SelectField('Subject', coerce=int, validators=[DataRequired()])
    file = FileField('Upload File', validators=[
        FileRequired(),
        FileAllowed(['pdf', 'doc', 'docx', 'ppt', 'pptx', 'zip'], 'Please upload allowed file types only!')
    ])
    submit = SubmitField('Upload Material')
