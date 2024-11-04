from app import db, Question, Exam, app  # Import app and models from your main application

# Example exam ID to delete and recreate
exam_title = "IGCSE Computer Science"

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

    # List of questions to add with various types
    questions = [
        # Single-choice question example
        {
            "question_text": "What is the primary function of the CPU?",
            "option_a": "Storage",
            "option_b": "Input",
            "option_c": "Processing",
            "option_d": "Output",
            "correct_option": "option_c",
            "question_type": "single"
        },
        {
            "question_text": "Jack has an MP3 file stored on his computer. which type of data is stored in an MP3 file.",
            "option_a": "Video",
            "option_b": "Sound",
            "option_c": "Image",
            "correct_option": "option_b",
            "question_type": "single"
        },        
        # Another single-choice question
        {
            "question_text": "What does RAM stand for?",
            "option_a": "Random Access Memory",
            "option_b": "Read Access Memory",
            "option_c": "Read And Manage",
            "option_d": "Random Active Memory",
            "correct_option": "option_a",
            "question_type": "single"
        },
        # Multiple-choice question example
        {
            "question_text": "Select all programming languages.",
            "option_a": "Python",
            "option_b": "HTML",
            "option_c": "CSS",
            "option_d": "Java",
            "correct_options": "option_a,option_d",  # Correct options for multiple-choice
            "question_type": "multiple"
        },
        # Fill-in-the-blank question example
        {
            "question_text": "Complete the paragraph with the correct terms for an inkjet printer.",
            "blanks": 3,
            "correct_options": "buffer,head,nozzles",  # Correct answers for each blank
            "question_type": "fill_in_the_blank"
        }
        # Add more questions as needed following these structures
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
            correct_options=q.get("correct_options"),
            blanks=q.get("blanks"),
            question_type=q["question_type"]
        )
        db.session.add(question)

    db.session.commit()
    print("Exam and questions added successfully.")
