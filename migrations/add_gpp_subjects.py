from app import create_app
from app.models.subject import Subject
from app.models.department import Department
from app.extensions import db

app = create_app()

def add_gpp_subjects():
    with app.app_context():
        # First clear existing subjects
        Subject.query.delete()
        db.session.commit()

        # Get departments
        ict_dept = Department.query.filter_by(name='Information and Communication Technology').first()
        it_dept = Department.query.filter_by(name='Information Technology').first()
        civil_dept = Department.query.filter_by(name='Civil Engineering').first()
        mech_dept = Department.query.filter_by(name='Mechanical Engineering').first()
        electrical_dept = Department.query.filter_by(name='Electrical Engineering').first()
        ec_dept = Department.query.filter_by(name='Electronics and Communication Engineering').first()

        # Add ICT subjects
        ict_subjects = [
            # Semester 1
            (1, 'Mathematics', '4300001', 'Theory'),
            (1, 'communication skills withEnglish', '4300002', 'Theory'),
            (1, 'Computer Programming', '3310701', 'Theory'),
            (1, 'Basic Electronics', '3310702', 'Theory'),
            (1, 'Environmental Conservation', '3311901', 'Theory'),
            
            # Semester 2
            (2, 'Advanced Mathematics', '3320701', 'Theory'),
            (2, 'Web Development', '3320702', 'Theory'),
            (2, 'Digital Electronics', '3320703', 'Theory'),
            (2, 'Data Structures', '3320704', 'Theory'),
            (2, 'Computer Networks Basics', '3320705', 'Theory'),
            
            # Semester 3
            (3, 'Object Oriented Programming', '3330701', 'Theory'),
            (3, 'Database Management Systems', '3330702', 'Theory'),
            (3, 'Operating Systems', '3330703', 'Theory'),
            (3, 'Computer Organization', '3330704', 'Theory'),
            (3, 'Web Programming', '3330705', 'Practical'),
            
            # Semester 4
            (4, 'Software Engineering', '3340701', 'Theory'),
            (4, 'Java Programming', '3340702', 'Theory'),
            (4, 'Computer Networks', '3340703', 'Theory'),
            (4, 'Mobile Application Development', '3340704', 'Practical'),
            (4, 'Network Security', '3340705', 'Theory'),
            
            # Semester 5
            (5, 'Advanced Java', '3350701', 'Theory'),
            (5, 'Python Programming', '3350702', 'Theory'),
            (5, 'Internet of Things', '3350703', 'Theory'),
            (5, 'Cloud Computing', '3350704', 'Theory'),
            (5, 'Project-1', '3350705', 'Practical'),
            
            # Semester 6
            (6, 'Machine Learning', '3360701', 'Theory'),
            (6, 'Full Stack Development', '3360702', 'Practical'),
            (6, 'Project-2', '3360703', 'Practical'),
            (6, 'Industrial Training', '3360704', 'Practical')
        ]

        # Add subjects for ICT
        for sem, name, code, category in ict_subjects:
            subject = Subject(
                name=name,
                code=code,
                category=category,
                semester=sem,
                department_id=ict_dept.id
            )
            db.session.add(subject)
        
        db.session.commit()
        print("Added ICT subjects successfully!")

        # Add IT subjects
        it_subjects = [
            # Semester 1
            (1, 'Basic Mathematics', '3300001', 'Theory'),
            (1, 'English', '3300002', 'Theory'),
            (1, 'Fundamentals of IT', '3310702', 'Theory'),
            (1, 'Basic Electronics', '3310703', 'Theory'),
            (1, 'Environmental Studies', '3311901', 'Theory'),
            
            # Semester 2
            (2, 'Advanced Mathematics', '3320701', 'Theory'),
            (2, 'Programming in C', '3320702', 'Theory'),
            (2, 'Digital Electronics', '3320703', 'Theory'),
            (2, 'Computer Architecture', '3320704', 'Theory'),
            (2, 'Web Design', '3320705', 'Practical'),
            
            # Semester 3
            (3, 'Data Structures', '3330701', 'Theory'),
            (3, 'Database Systems', '3330702', 'Theory'),
            (3, 'Operating Systems', '3330703', 'Theory'),
            (3, 'Object Oriented Programming', '3330704', 'Theory'),
            (3, 'Network Essentials', '3330705', 'Theory'),
            
            # Semester 4
            (4, 'Software Engineering', '3340701', 'Theory'),
            (4, 'Advanced Java', '3340702', 'Theory'),
            (4, 'Computer Networks', '3340703', 'Theory'),
            (4, 'Web Development', '3340704', 'Practical'),
            (4, 'Network Security', '3340705', 'Theory'),
            
            # Semester 5
            (5, 'Enterprise Java', '3350701', 'Theory'),
            (5, 'Python Programming', '3350702', 'Theory'),
            (5, 'Mobile Computing', '3350703', 'Theory'),
            (5, 'Cloud Computing', '3350704', 'Theory'),
            (5, 'Project-1', '3350705', 'Practical'),
            
            # Semester 6
            (6, 'Data Science', '3360701', 'Theory'),
            (6, 'Full Stack Development', '3360702', 'Practical'),
            (6, 'Project-2', '3360703', 'Practical'),
            (6, 'Industrial Training', '3360704', 'Practical')
        ]

        # Add subjects for IT
        for sem, name, code, category in it_subjects:
            subject = Subject(
                name=name,
                code=code,
                category=category,
                semester=sem,
                department_id=it_dept.id
            )
            db.session.add(subject)
        
        db.session.commit()
        print("Added IT subjects successfully!")

        # Add Civil Engineering subjects
        civil_subjects = [
            # Semester 1
            (1, 'Engineering Mathematics-I', '3300001', 'Theory'),
            (1, 'English', '3300002', 'Theory'),
            (1, 'Engineering Physics', '3300003', 'Theory'),
            (1, 'Engineering Drawing', '3310601', 'Practical'),
            (1, 'Workshop Practice', '3310602', 'Practical'),
            
            # Semester 2
            (2, 'Engineering Mathematics-II', '3320601', 'Theory'),
            (2, 'Building Materials', '3320602', 'Theory'),
            (2, 'Surveying-I', '3320603', 'Theory'),
            (2, 'Building Construction', '3320604', 'Theory'),
            (2, 'Civil Engineering Drawing-I', '3320605', 'Practical'),
            
            # Semester 3
            (3, 'Mechanics of Structures', '3330601', 'Theory'),
            (3, 'Building Construction-II', '3330602', 'Theory'),
            (3, 'Surveying-II', '3330603', 'Theory'),
            (3, 'Transportation Engineering', '3330604', 'Theory'),
            (3, 'Civil Engineering Drawing-II', '3330605', 'Practical'),
            
            # Semester 4
            (4, 'Concrete Technology', '3340601', 'Theory'),
            (4, 'Structural Engineering', '3340602', 'Theory'),
            (4, 'Quantity Surveying', '3340603', 'Theory'),
            (4, 'Geotechnical Engineering', '3340604', 'Theory'),
            (4, 'Environmental Engineering', '3340605', 'Theory'),
            
            # Semester 5
            (5, 'Design of Steel Structures', '3350601', 'Theory'),
            (5, 'Highway Engineering', '3350602', 'Theory'),
            (5, 'Water Resource Engineering', '3350603', 'Theory'),
            (5, 'Construction Management', '3350604', 'Theory'),
            (5, 'Project-1', '3350605', 'Practical'),
            
            # Semester 6
            (6, 'Design of RCC Structures', '3360601', 'Theory'),
            (6, 'Estimation and Costing', '3360602', 'Theory'),
            (6, 'Project-2', '3360603', 'Practical'),
            (6, 'Industrial Training', '3360604', 'Practical')
        ]

        # Add subjects for Civil
        for sem, name, code, category in civil_subjects:
            subject = Subject(
                name=name,
                code=code,
                category=category,
                semester=sem,
                department_id=civil_dept.id
            )
            db.session.add(subject)
        
        db.session.commit()
        print("Added Civil Engineering subjects successfully!")

        # Add Mechanical Engineering subjects
        mech_subjects = [
            # Semester 1
            (1, 'Engineering Mathematics-I', '3300001', 'Theory'),
            (1, 'English', '3300002', 'Theory'),
            (1, 'Engineering Physics', '3300003', 'Theory'),
            (1, 'Engineering Drawing', '3310501', 'Practical'),
            (1, 'Workshop Practice', '3310502', 'Practical'),
            
            # Semester 2
            (2, 'Engineering Mathematics-II', '3320501', 'Theory'),
            (2, 'Engineering Mechanics', '3320502', 'Theory'),
            (2, 'Basic Mechanical Engineering', '3320503', 'Theory'),
            (2, 'Manufacturing Processes', '3320504', 'Theory'),
            (2, 'Computer Aided Drawing', '3320505', 'Practical'),
            
            # Semester 3
            (3, 'Strength of Materials', '3330501', 'Theory'),
            (3, 'Thermal Engineering', '3330502', 'Theory'),
            (3, 'Machine Tools', '3330503', 'Theory'),
            (3, 'Metrology and Instrumentation', '3330504', 'Theory'),
            (3, 'Machine Drawing', '3330505', 'Practical'),
            
            # Semester 4
            (4, 'Theory of Machines', '3340501', 'Theory'),
            (4, 'Manufacturing Technology', '3340502', 'Theory'),
            (4, 'Fluid Mechanics', '3340503', 'Theory'),
            (4, 'Industrial Engineering', '3340504', 'Theory'),
            (4, 'CAD/CAM', '3340505', 'Practical'),
            
            # Semester 5
            (5, 'Machine Design', '3350501', 'Theory'),
            (5, 'Heat Transfer', '3350502', 'Theory'),
            (5, 'Power Plant Engineering', '3350503', 'Theory'),
            (5, 'Automobile Engineering', '3350504', 'Theory'),
            (5, 'Project-1', '3350505', 'Practical'),
            
            # Semester 6
            (6, 'Industrial Management', '3360501', 'Theory'),
            (6, 'Refrigeration and Air Conditioning', '3360502', 'Theory'),
            (6, 'Project-2', '3360503', 'Practical'),
            (6, 'Industrial Training', '3360504', 'Practical')
        ]

        # Add subjects for Mechanical
        for sem, name, code, category in mech_subjects:
            subject = Subject(
                name=name,
                code=code,
                category=category,
                semester=sem,
                department_id=mech_dept.id
            )
            db.session.add(subject)
        
        db.session.commit()
        print("Added Mechanical Engineering subjects successfully!")

        # Add Electrical Engineering subjects
        electrical_subjects = [
            # Semester 1
            (1, 'Engineering Mathematics-I', '3300001', 'Theory'),
            (1, 'English', '3300002', 'Theory'),
            (1, 'Engineering Physics', '3300003', 'Theory'),
            (1, 'Basic Electrical', '3310401', 'Theory'),
            (1, 'Workshop Practice', '3310402', 'Practical'),
            
            # Semester 2
            (2, 'Engineering Mathematics-II', '3320401', 'Theory'),
            (2, 'Electrical Engineering Materials', '3320402', 'Theory'),
            (2, 'Basic Electronics', '3320403', 'Theory'),
            (2, 'Electrical Measurements', '3320404', 'Theory'),
            (2, 'Electrical Workshop', '3320405', 'Practical'),
            
            # Semester 3
            (3, 'DC Machines', '3330401', 'Theory'),
            (3, 'Electrical Circuit Analysis', '3330402', 'Theory'),
            (3, 'Digital Electronics', '3330403', 'Theory'),
            (3, 'Power Plant Engineering', '3330404', 'Theory'),
            (3, 'Electrical Drawing', '3330405', 'Practical'),
            
            # Semester 4
            (4, 'AC Machines', '3340401', 'Theory'),
            (4, 'Power Electronics', '3340402', 'Theory'),
            (4, 'Microprocessors', '3340403', 'Theory'),
            (4, 'Transmission and Distribution', '3340404', 'Theory'),
            (4, 'Electrical CAD', '3340405', 'Practical'),
            
            # Semester 5
            (5, 'Industrial Drives', '3350401', 'Theory'),
            (5, 'Power System Protection', '3350402', 'Theory'),
            (5, 'Control Systems', '3350403', 'Theory'),
            (5, 'PLC and SCADA', '3350404', 'Theory'),
            (5, 'Project-1', '3350405', 'Practical'),
            
            # Semester 6
            (6, 'Installation and Maintenance', '3360401', 'Theory'),
            (6, 'Energy Conservation', '3360402', 'Theory'),
            (6, 'Project-2', '3360403', 'Practical'),
            (6, 'Industrial Training', '3360404', 'Practical')
        ]

        # Add subjects for Electrical
        for sem, name, code, category in electrical_subjects:
            subject = Subject(
                name=name,
                code=code,
                category=category,
                semester=sem,
                department_id=electrical_dept.id
            )
            db.session.add(subject)
        
        db.session.commit()
        print("Added Electrical Engineering subjects successfully!")

        # Add Electronics and Communication Engineering subjects
        ec_subjects = [
            # Semester 1
            (1, 'Engineering Mathematics-I', '3300001', 'Theory'),
            (1, 'English', '3300002', 'Theory'),
            (1, 'Engineering Physics', '3300003', 'Theory'),
            (1, 'Basic Electronics', '3310301', 'Theory'),
            (1, 'Workshop Practice', '3310302', 'Practical'),
            
            # Semester 2
            (2, 'Engineering Mathematics-II', '3320301', 'Theory'),
            (2, 'Electronic Components', '3320302', 'Theory'),
            (2, 'Digital Electronics', '3320303', 'Theory'),
            (2, 'Electronic Circuits', '3320304', 'Theory'),
            (2, 'PCB Design', '3320305', 'Practical'),
            
            # Semester 3
            (3, 'Communication Engineering', '3330301', 'Theory'),
            (3, 'Linear Integrated Circuits', '3330302', 'Theory'),
            (3, 'Microprocessors', '3330303', 'Theory'),
            (3, 'Electronic Measurements', '3330304', 'Theory'),
            (3, 'Electronic Workshop', '3330305', 'Practical'),
            
            # Semester 4
            (4, 'Digital Communication', '3340301', 'Theory'),
            (4, 'Microcontrollers', '3340302', 'Theory'),
            (4, 'Computer Networks', '3340303', 'Theory'),
            (4, 'Electronic Design', '3340304', 'Theory'),
            (4, 'PCB Fabrication', '3340305', 'Practical'),
            
            # Semester 5
            (5, 'Mobile Communication', '3350301', 'Theory'),
            (5, 'Embedded Systems', '3350302', 'Theory'),
            (5, 'Antenna and Wave Propagation', '3350303', 'Theory'),
            (5, 'Industrial Electronics', '3350304', 'Theory'),
            (5, 'Project-1', '3350305', 'Practical'),
            
            # Semester 6
            (6, 'Optical Communication', '3360301', 'Theory'),
            (6, 'VLSI Design', '3360302', 'Theory'),
            (6, 'Project-2', '3360303', 'Practical'),
            (6, 'Industrial Training', '3360304', 'Practical')
        ]

        # Add subjects for EC
        for sem, name, code, category in ec_subjects:
            subject = Subject(
                name=name,
                code=code,
                category=category,
                semester=sem,
                department_id=ec_dept.id
            )
            db.session.add(subject)
        
        db.session.commit()
        print("Added Electronics and Communication Engineering subjects successfully!")

if __name__ == '__main__':
    add_gpp_subjects()
