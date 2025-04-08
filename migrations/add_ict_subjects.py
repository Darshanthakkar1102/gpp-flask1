from app import create_app
from app.extensions import db
from app.models.subject import Subject
from app.models.department import Department

app = create_app()

def add_ict_subjects():
    with app.app_context():
        # Get ICT department
        ict_dept = Department.query.filter_by(name='Information and Communication Technology').first()
        if not ict_dept:
            print("ICT department not found")
            return
        
        # First, delete existing subjects for ICT department semester 1
        Subject.query.filter_by(department_id=ict_dept.id, semester=1).delete()
        
        # Semester 1 subjects for ICT
        subjects = [
            {
                'code': '1313201',
                'name': 'Fundamentals of ICT',
                'category': 'Program Core',
                'semester': 1
            },
            {
                'code': '1313202',
                'name': 'Elements of Electrical & Electronics Engineering',
                'category': 'Engineering Sciences',
                'semester': 1
            },
            {
                'code': '1313203',
                'name': 'Web Development Practices',
                'category': 'Program Core',
                'semester': 1
            },
            {
                'code': '4300001',
                'name': 'Mathematics',
                'category': 'Basic Sciences',
                'semester': 1
            },
            {
                'code': '4300002',
                'name': 'Communication Skills with English',
                'category': None,
                'semester': 1
            },
            {
                'code': '4300005',
                'name': 'Physics',
                'category': 'Basic Sciences',
                'semester': 1
            },
            {
                'code': '4300015',
                'name': 'Sports and Yoga',
                'category': 'Audit',
                'semester': 1
            },
            {
                'code': '4310002',
                'name': 'Induction Program',
                'category': None,
                'semester': 1
            }
        ]
        
        # Add subjects
        for subject_data in subjects:
            subject = Subject(
                code=subject_data['code'],
                name=subject_data['name'],
                category=subject_data['category'],
                semester=subject_data['semester'],
                department_id=ict_dept.id
            )
            db.session.add(subject)
        
        try:
            db.session.commit()
            print("ICT semester 1 subjects added successfully!")
        except Exception as e:
            db.session.rollback()
            print(f"Error adding subjects: {str(e)}")

if __name__ == '__main__':
    add_ict_subjects()
