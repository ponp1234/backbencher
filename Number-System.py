from app import db, Question, Exam, app  # Import app and models from your main application

exam_title = "AS-IGCSE Computer Science - Number System"

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

    # List of questions on the Number System topic
    questions = [
        # General Questions (30 questions)
        {"question_text": "What is the binary representation of the decimal number 25?",
         "option_a": "11001", "option_b": "10110", "option_c": "10011", "option_d": "11100", "correct_option": "option_a", "question_type": "single"},
        {"question_text": "What is the decimal equivalent of the binary number 10110?",
         "option_a": "20", "option_b": "21", "option_c": "22", "option_d": "23", "correct_option": "option_d", "question_type": "single"},
        {"question_text": "What is the base of a hexadecimal number system?",
         "option_a": "10", "option_b": "12", "option_c": "16", "option_d": "8", "correct_option": "option_c", "question_type": "single"},
        {"question_text": "What is the octal representation of the decimal number 64?",
         "option_a": "80", "option_b": "74", "option_c": "100", "option_d": "200", "correct_option": "option_c", "question_type": "single"},
        {"question_text": "Convert 1A in hexadecimal to decimal.",
         "option_a": "24", "option_b": "26", "option_c": "28", "option_d": "30", "correct_option": "option_b", "question_type": "single"},
        {"question_text": "What is the binary equivalent of the hexadecimal number F?",
         "option_a": "1111", "option_b": "1010", "option_c": "1100", "option_d": "1001", "correct_option": "option_a", "question_type": "single"},
        {"question_text": "How many bits are in a byte?",
         "option_a": "4", "option_b": "8", "option_c": "16", "option_d": "32", "correct_option": "option_b", "question_type": "single"},
        {"question_text": "What is the range of decimal numbers represented by an 8-bit unsigned binary number?",
         "option_a": "0-127", "option_b": "0-255", "option_c": "1-255", "option_d": "1-256", "correct_option": "option_b", "question_type": "single"},
        {"question_text": "What is the hexadecimal representation of binary 11110000?",
         "option_a": "F0", "option_b": "1E", "option_c": "FE", "option_d": "F1", "correct_option": "option_a", "question_type": "single"},
        {"question_text": "What is the decimal equivalent of binary 11001101?",
         "option_a": "204", "option_b": "205", "option_c": "206", "option_d": "207", "correct_option": "option_b", "question_type": "single"},
        {"question_text": "What is the result of binary AND operation between 1011 and 1101?",
         "option_a": "1010", "option_b": "1001", "option_c": "1101", "option_d": "1111", "correct_option": "option_b", "question_type": "single"},
        {"question_text": "Which number system uses base 2?",
         "option_a": "Binary", "option_b": "Decimal", "option_c": "Hexadecimal", "option_d": "Octal", "correct_option": "option_a", "question_type": "single"},
        {"question_text": "What is the largest hexadecimal digit?",
         "option_a": "E", "option_b": "F", "option_c": "10", "option_d": "G", "correct_option": "option_b", "question_type": "single"},
        {"question_text": "What is the binary representation of decimal 255?",
         "option_a": "11111011", "option_b": "11111111", "option_c": "10000000", "option_d": "10101010", "correct_option": "option_b", "question_type": "single"},
        {"question_text": "Which of the following is a positional number system?",
         "option_a": "Roman numerals", "option_b": "Decimal", "option_c": "Binary", "option_d": "Both B and C", "correct_option": "option_d", "question_type": "single"},
        {"question_text": "Convert the binary number 10101 to decimal.",
         "option_a": "19", "option_b": "20", "option_c": "21", "option_d": "22", "correct_option": "option_c", "question_type": "single"},
        {"question_text": "What is the binary representation of hexadecimal A?",
         "option_a": "1010", "option_b": "1011", "option_c": "1100", "option_d": "1101", "correct_option": "option_a", "question_type": "single"},
        {"question_text": "What is the main advantage of using hexadecimal over binary?",
         "option_a": "Easier to read", "option_b": "Uses more digits", "option_c": "More accurate", "option_d": "No advantage", "correct_option": "option_a", "question_type": "single"},
        {"question_text": "What is the result of binary OR operation between 1010 and 0110?",
         "option_a": "1100", "option_b": "1010", "option_c": "1110", "option_d": "0101", "correct_option": "option_c", "question_type": "single"},
        {"question_text": "Convert octal 77 to binary.",
         "option_a": "110111", "option_b": "111111", "option_c": "100111", "option_d": "101010", "correct_option": "option_b", "question_type": "single"},
        {"question_text": "What is the base of the decimal number system?",
         "option_a": "10", "option_b": "2", "option_c": "8", "option_d": "16", "correct_option": "option_a", "question_type": "single"},
        {"question_text": "Convert binary 101011 to hexadecimal.",
         "option_a": "2B", "option_b": "2F", "option_c": "3B", "option_d": "4B", "correct_option": "option_a", "question_type": "single"},
        {"question_text": "What is the binary equivalent of decimal 64?",
         "option_a": "1100000", "option_b": "1010101", "option_c": "1111111", "option_d": "1110000", "correct_option": "option_a", "question_type": "single"},
        {"question_text": "What is the decimal equivalent of the binary number 101001?",
         "option_a": "38", "option_b": "39", "option_c": "40", "option_d": "41", "correct_option": "option_d", "question_type": "single"},
        {"question_text": "What is the 2’s complement of 1101 (4-bit representation)?",
         "option_a": "0011", "option_b": "1011", "option_c": "1111", "option_d": "0101", "correct_option": "option_b", "question_type": "single"},
        {"question_text": "What is the hexadecimal equivalent of binary 11111111?",
         "option_a": "FF", "option_b": "FE", "option_c": "EF", "option_d": "EE", "correct_option": "option_a", "question_type": "single"},
        {"question_text": "Which is not a valid binary number?",
         "option_a": "1101", "option_b": "2020", "option_c": "1111", "option_d": "1010", "correct_option": "option_b", "question_type": "single"},
        {"question_text": "What is the decimal representation of hexadecimal 1A?",
         "option_a": "26", "option_b": "27", "option_c": "28", "option_d": "29", "correct_option": "option_a", "question_type": "single"},
        {"question_text": "What is the binary equivalent of the octal number 7?",
         "option_a": "111", "option_b": "101", "option_c": "110", "option_d": "100", "correct_option": "option_a", "question_type": "single"},

        # Hard Questions (10 questions)
        {"question_text": "What is the two’s complement representation of -19 in an 8-bit system?",
         "option_a": "11101101", "option_b": "11101100", "option_c": "11101011", "option_d": "11101010", "correct_option": "option_c", "question_type": "single"},
        {"question_text": "Perform binary addition: 1101 + 1011.",
         "option_a": "10100", "option_b": "11000", "option_c": "10000", "option_d": "11110", "correct_option": "option_a", "question_type": "single"},
        {"question_text": "Convert the binary floating-point number 1.101 × 2³ to decimal.",
         "option_a": "11.5", "option_b": "13.5", "option_c": "14.5", "option_d": "15.5", "correct_option": "option_b", "question_type": "single"},
        {"question_text": "What is the result of dividing 1100 (binary) by 11 (binary)?",
         "option_a": "100", "option_b": "101", "option_c": "110", "option_d": "111", "correct_option": "option_a", "question_type": "single"},
        {"question_text": "Simplify binary 10101 × 101 using AND gates.",
         "option_a": "101", "option_b": "1101", "option_c": "111", "option_d": "1000", "correct_option": "option_b", "question_type": "single"},
        {"question_text": "What is the 8-bit signed representation of -128?",
         "option_a": "10000000", "option_b": "11111111", "option_c": "01111111", "option_d": "11000000", "correct_option": "option_a", "question_type": "single"},
        {"question_text": "If the MSB in a signed binary number is 1, what does it indicate?",
         "option_a": "Positive", "option_b": "Negative", "option_c": "Zero", "option_d": "Overflow", "correct_option": "option_b", "question_type": "single"},
        {"question_text": "Convert the hexadecimal number 2F to binary.",
         "option_a": "101111", "option_b": "111011", "option_c": "100111", "option_d": "110101", "correct_option": "option_a", "question_type": "single"},
        {"question_text": "What is the binary representation of the decimal number 1024?",
         "option_a": "10000000000", "option_b": "1111111111", "option_c": "1010101010", "option_d": "1101101101", "correct_option": "option_a", "question_type": "single"},
        {"question_text": "Perform subtraction: 1101 - 1011 (binary).",
         "option_a": "010", "option_b": "100", "option_c": "101", "option_d": "110", "correct_option": "option_b", "question_type": "single"}
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
