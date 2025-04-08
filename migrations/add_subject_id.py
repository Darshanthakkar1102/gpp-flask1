from app import create_app
from app.extensions import db
from sqlalchemy import text

app = create_app()

def add_subject_id_column():
    with app.app_context():
        # Add subject_id column to study_materials table
        with db.engine.connect() as conn:
            conn.execute(text('ALTER TABLE study_materials ADD COLUMN subject_id INTEGER REFERENCES subjects(id)'))
            conn.commit()
        print("Added subject_id column to study_materials table")

if __name__ == '__main__':
    add_subject_id_column()
