from app import create_app
from app.extensions import db
from app.models.subject import Subject
from app.models.department import Department

app = create_app()

def add_sample_subjects():
    # Get Computer department
    computer_dept = Department.query.filter_by(name='Computer Engineering').first()
    if not computer_dept:
        return
    
    # Sample subjects for Computer Engineering
    subjects = [
        # Semester 1
        {'name': 'Engineering Mathematics-I', 'semester': 1},
        {'name': 'Engineering Physics', 'semester': 1},
        {'name': 'Basic Electronics', 'semester': 1},
        
        # Semester 2
        {'name': 'Engineering Mathematics-II', 'semester': 2},
        {'name': 'Programming in C', 'semester': 2},
        {'name': 'Digital Electronics', 'semester': 2},
        
        # Semester 3
        {'name': 'Data Structures', 'semester': 3},
        {'name': 'Database Management Systems', 'semester': 3},
        {'name': 'Object Oriented Programming', 'semester': 3},
        
        # Semester 4
        {'name': 'Operating Systems', 'semester': 4},
        {'name': 'Computer Networks', 'semester': 4},
        {'name': 'Web Development', 'semester': 4},
        
        # Semester 5
        {'name': 'Software Engineering', 'semester': 5},
        {'name': 'Artificial Intelligence', 'semester': 5},
        {'name': 'Cloud Computing', 'semester': 5},
        
        # Semester 6
        {'name': 'Machine Learning', 'semester': 6},
        {'name': 'Information Security', 'semester': 6},
        {'name': 'Mobile App Development', 'semester': 6},
    ]
    
    for subject_data in subjects:
        subject = Subject(
            name=subject_data['name'],
            semester=subject_data['semester'],
            department_id=computer_dept.id
        )
        db.session.add(subject)
    
    try:
        db.session.commit()
        print("Sample subjects added successfully!")
    except Exception as e:
        db.session.rollback()
        print(f"Error adding subjects: {str(e)}")

if __name__ == '__main__':
    with app.app_context():
        add_sample_subjects()
