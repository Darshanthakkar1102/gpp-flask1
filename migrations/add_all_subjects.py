from app import create_app
from app.extensions import db
from app.models.subject import Subject
from app.models.department import Department

app = create_app()

def add_all_subjects():
    with app.app_context():
        # Subject data for all departments
        subjects_data = {
            'Information and Communication Technology': {
                1: [
                    ('1313201', 'Fundamentals of ICT', 'Program Core'),
                    ('1313202', 'Elements of Electrical & Electronics Engineering', 'Engineering Sciences'),
                    ('1313203', 'Web Development Practices', 'Program Core'),
                    ('4300001', 'Mathematics', 'Basic Sciences'),
                    ('4300002', 'Communication Skills with English', None),
                    ('4300005', 'Physics', 'Basic Sciences'),
                    ('4300015', 'Sports and Yoga', 'Audit'),
                    ('4310002', 'Induction Program', None)
                ]
            },
            'Computer Engineering': {
                1: [
                    ('3310701', 'Computer Programming', 'Program Core'),
                    ('3310702', 'Digital Electronics', 'Engineering Sciences'),
                    ('3300001', 'Mathematics', 'Basic Sciences'),
                    ('3300002', 'English', None),
                    ('3300003', 'Environment Conservation', 'Basic Sciences'),
                    ('3300004', 'Computer Fundamentals', 'Program Core')
                ]
            },
            'Civil Engineering': {
                1: [
                    ('3310601', 'Engineering Drawing', 'Engineering Sciences'),
                    ('3310602', 'Basic Civil Engineering', 'Program Core'),
                    ('3300001', 'Mathematics', 'Basic Sciences'),
                    ('3300002', 'English', None),
                    ('3300003', 'Environment Conservation', 'Basic Sciences'),
                    ('3300004', 'Workshop Practice', 'Program Core')
                ]
            },
            'Mechanical Engineering': {
                1: [
                    ('3310501', 'Engineering Mechanics', 'Engineering Sciences'),
                    ('3310502', 'Basic Mechanical Engineering', 'Program Core'),
                    ('3300001', 'Mathematics', 'Basic Sciences'),
                    ('3300002', 'English', None),
                    ('3300003', 'Environment Conservation', 'Basic Sciences'),
                    ('3300004', 'Workshop Practice', 'Program Core')
                ]
            },
            'Electrical Engineering': {
                1: [
                    ('3310401', 'Basic Electrical', 'Program Core'),
                    ('3310402', 'Electrical Measurements', 'Engineering Sciences'),
                    ('3300001', 'Mathematics', 'Basic Sciences'),
                    ('3300002', 'English', None),
                    ('3300003', 'Environment Conservation', 'Basic Sciences'),
                    ('3300004', 'Workshop Practice', 'Program Core')
                ]
            }
        }

        # Add subjects for each department
        for dept_name, semesters in subjects_data.items():
            dept = Department.query.filter_by(name=dept_name).first()
            if not dept:
                print(f"Department {dept_name} not found")
                continue

            # Delete existing subjects for this department
            Subject.query.filter_by(department_id=dept.id).delete()

            # Add new subjects
            for semester, subjects in semesters.items():
                for code, name, category in subjects:
                    subject = Subject(
                        code=code,
                        name=name,
                        category=category,
                        semester=semester,
                        department_id=dept.id
                    )
                    db.session.add(subject)

        try:
            db.session.commit()
            print("All subjects added successfully!")
        except Exception as e:
            db.session.rollback()
            print(f"Error adding subjects: {str(e)}")

if __name__ == '__main__':
    add_all_subjects()
