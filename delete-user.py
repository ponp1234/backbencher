from app import User, app  # Import app and models from your main application

with app.app_context():
    # Delete all questions
    User.__table__.drop(db.engine)
    db.session.commit()

