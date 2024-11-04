from app import db, Exam, Question, app  # Import app and models from your main application

with app.app_context():
    # Delete all questions
    Question.query.delete()
    # Delete all exams
    Exam.query.delete()
    # Commit changes to the database
    db.session.commit()
    print("All exams and associated questions have been deleted.")
