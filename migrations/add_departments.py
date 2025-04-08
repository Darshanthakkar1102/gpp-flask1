from app import create_app
from app.extensions import db
from app.models.department import Department

app = create_app()

def add_departments():
    with app.app_context():
        # Add departments
        departments = [
            'Information and Communication Technology',
            'Information Technology',
            'Civil Engineering',
            'Mechanical Engineering',
            'Electrical Engineering',
            'Electronics and Communication Engineering'
        ]
        
        for dept_name in departments:
            dept = Department.query.filter_by(name=dept_name).first()
            if not dept:
                dept = Department(name=dept_name)
                db.session.add(dept)
        
        try:
            db.session.commit()
            print("Departments added successfully!")
        except Exception as e:
            db.session.rollback()
            print(f"Error adding departments: {str(e)}")

if __name__ == '__main__':
    add_departments()
