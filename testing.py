from app import db, Question, Exam, app  # Import app and models from your main application

# Example exam title to delete and recreate
exam_title = "Testing"

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
        # Question 1
        {
            "question_text": "Jack has an MP3 file stored on his computer.\n\n(a) (i) Tick (✓) to show which type of data is stored in an MP3 file.",
            "option_a": "Video",
            "option_b": "Sound",
            "option_c": "Image",
            "correct_option": "option_b",
            "question_type": "single"
        },
        # Question 2
        {
            "question_text": "A computer is designed using the Von Neumann model for a computer system.\n\n(a) (i) State the name of the primary storage from where data is fetched.",
            "blanks": 1,
            "correct_options": "RAM",
            "question_type": "textbox"
        },
        {
            "question_text": "dentify and describe three ethical issues that could be a concern when using the Internet.",
            "blanks": 2,
            "correct_options": "Plagiarism – The copying of other people's work without their permission – Claiming someone else's work as your own. Hacking – Unauthorised access to a computer/data. Malware – Malicious software designed to damage a computer system or stored data. Spyware – Keylogger used to record keypresses and sends them to third party. Ransomware – Holding hostage a user's data, often for a release fee. Intellectual property theft – Stealing other people work. Breaching copyright – Breaking the law by copying someone's work. Piracy – Using piracy websites to gain content for free that should have been paid for. Privacy – A person's data could be leaked. Phishing – Sending an email to lure users to a fake site to obtain their personal details.",
            "question_type": "textbox"
        },
       
        # Question 8
        {
            "question_text": "Draw a logic circuit to represent the following logic statement:\n\nX = (((A AND NOT B) OR (NOT (B NOR C))) AND C)",
            "blanks": 1,
            "correct_options": "Diagram Required",
            "question_type": "drawing"
        },
        # Question 9
        {
            "question_text": "Give three features of a MAC address.",
            "blanks": 3,
            "correct_options": "Unique identifier,Static for each device,48-bits long",
            "question_type": "fill_in_the_blank"
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
            correct_options=q.get("correct_options"),
            blanks=q.get("blanks"),
            question_type=q["question_type"]
        )
        db.session.add(question)

    db.session.commit()
    print("Exam and questions added successfully.")
