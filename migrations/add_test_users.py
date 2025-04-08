from app import create_app
from app.extensions import db
from app.models.user import User, Role
from flask_security.utils import hash_password

app = create_app()

def add_test_users():
    with app.app_context():
        # Get roles
        faculty_role = Role.query.filter_by(name='lecturer').first()
        student_role = Role.query.filter_by(name='student').first()
        
        if not faculty_role or not student_role:
            print("Required roles not found! Please run add_admin_user.py first.")
            return
        
        # Create test faculty user
        test_faculty = User.query.filter_by(email='faculty@test.com').first()
        if not test_faculty:
            test_faculty = User(
                email='faculty@test.com',
                password=hash_password('faculty123'),
                active=True,
                approved=True,  # Make sure the account is approved
                roles=[faculty_role]
            )
            db.session.add(test_faculty)
        else:
            # Update existing faculty user to ensure it's approved
            test_faculty.active = True
            test_faculty.approved = True
        
        # Create test student user
        test_student = User.query.filter_by(email='student@test.com').first()
        if not test_student:
            test_student = User(
                email='student@test.com',
                password=hash_password('student123'),
                active=True,
                approved=True,  # Make sure the account is approved
                roles=[student_role]
            )
            db.session.add(test_student)
        else:
            # Update existing student user to ensure it's approved
            test_student.active = True
            test_student.approved = True
        
        try:
            db.session.commit()
            print("Test users created/updated successfully!")
        except Exception as e:
            db.session.rollback()
            print(f"Error creating/updating test users: {str(e)}")

if __name__ == '__main__':
    add_test_users()
