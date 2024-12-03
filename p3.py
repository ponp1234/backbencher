from app import db, Question, Exam, app  # Import app and models from your main application
# Example exam title to delete and recreate
exam_title = "P3 science"

with app.app_context():
    # Check if the exam already exists and delete it along with its questions
    exam = Exam.query.filter_by(title=exam_title).first()
    if exam:
        # Delete associated questions
        Question.query.filter_by(exam_id=exam.id).delete()
        # Delete the exam itself
        db.session.delete(exam)
        db.session.commit()  # Commit the deletion

    # Recreate the exam
    new_exam = Exam(title=exam_title)
    db.session.add(new_exam)
    db.session.commit()  # Commit to get the new exam ID

    # List of real questions from the document
    questions = [
        # Question
        {
            "question_text": "The diagram shows the positions of 3 ring magnets when they are put through a wooden rod.\nWhich one of the following correctly shows the poles of A and B?",
            "option_a": "A: North, B: North",
            "option_b": "A: North, B: South",
            "option_c": "A: South, B: North",
            "option_d": "A: South, B: South",
            "correct_option": "option_a",  # Replace this with the correct answer based on the context
            "question_type": "single"
        }
    ]

    # Add questions to the database with the new exam ID
    for q in questions:
        question = Question(
            exam_id=new_exam.id,  # Set the new exam ID for the question
            question_text=q["question_text"],
            option_a=q.get("option_a"),
            option_b=q.get("option_b"),
            option_c=q.get("option_c"),
            option_d=q.get("option_d"),
            correct_option=q.get("correct_option"),
            question_type=q["question_type"]
        )
        db.session.add(question)

    db.session.commit()
    print("Exam and questions added successfully.")
