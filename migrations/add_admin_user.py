from app import create_app
from app.extensions import db, security
from app.models.user import User, Role
from flask_security.utils import hash_password

app = create_app()

def add_admin_user():
    with app.app_context():
        # Create roles if they don't exist
        roles = ['admin', 'hod', 'lecturer', 'student']
        for role_name in roles:
            role = Role.query.filter_by(name=role_name).first()
            if not role:
                role = Role(name=role_name)
                db.session.add(role)
        
        try:
            db.session.commit()
            print("Roles created successfully!")
        except Exception as e:
            db.session.rollback()
            print(f"Error creating roles: {str(e)}")
            return
        
        # Create admin user
        admin_role = Role.query.filter_by(name='admin').first()
        if not admin_role:
            print("Admin role not found!")
            return
        
        admin = User.query.filter_by(email='admin@gppalanpur.in').first()
        if not admin:
            admin = User(
                email='admin@gppalanpur.in',
                password=hash_password('admin123'),
                active=True,
                roles=[admin_role]
            )
            db.session.add(admin)
            
            try:
                db.session.commit()
                print("Admin user created successfully!")
            except Exception as e:
                db.session.rollback()
                print(f"Error creating admin user: {str(e)}")
        else:
            print("Admin user already exists!")

if __name__ == '__main__':
    add_admin_user()
