from app import db, Question, Exam, app  # Import app and models from your main application

# Exam title
exam_title = "AS-IGCSE Computer Science - Text, Sound, Image, and Data Storage, Number System"

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

    # Questions for the topic
    questions = [
        # General Questions (25)
        {"question_text": "How many bits are used to represent a single character in ASCII?",
         "option_a": "7", "option_b": "8", "option_c": "16", "option_d": "32", "correct_option": "option_a", "question_type": "single"},
        {"question_text": "What is the binary representation of the ASCII character 'A'?",
         "option_a": "01000001", "option_b": "01000010", "option_c": "01100001", "option_d": "01100010", "correct_option": "option_a", "question_type": "single"},
        {"question_text": "What is the base unit of digital storage?",
         "option_a": "Bit", "option_b": "Byte", "option_c": "Kilobyte", "option_d": "Gigabyte", "correct_option": "option_a", "question_type": "single"},
        {"question_text": "How many bytes are in a kilobyte (KB)?",
         "option_a": "1000", "option_b": "1024", "option_c": "100", "option_d": "2048", "correct_option": "option_b", "question_type": "single"},
        {"question_text": "What is the standard sampling rate for audio CDs?",
         "option_a": "44.1 kHz", "option_b": "48 kHz", "option_c": "96 kHz", "option_d": "22.05 kHz", "correct_option": "option_a", "question_type": "single"},
        {"question_text": "Which unit is used to measure the resolution of an image?",
         "option_a": "Pixels", "option_b": "DPI", "option_c": "PPI", "option_d": "All of the above", "correct_option": "option_d", "question_type": "single"},
        {"question_text": "What is the hexadecimal representation of binary 11111011?",
         "option_a": "FB", "option_b": "7F", "option_c": "FF", "option_d": "BF", "correct_option": "option_a", "question_type": "single"},
        {"question_text": "How many colors can be represented using 8 bits?",
         "option_a": "16", "option_b": "256", "option_c": "1024", "option_d": "65,536", "correct_option": "option_b", "question_type": "single"},
        {"question_text": "What is the purpose of parity bits in data storage?",
         "option_a": "To correct errors", "option_b": "To detect errors", "option_c": "To increase speed", "option_d": "To compress data", "correct_option": "option_b", "question_type": "single"},
        {"question_text": "What is the binary representation of 255?",
         "option_a": "11111110", "option_b": "11111111", "option_c": "10000000", "option_d": "11111011", "correct_option": "option_b", "question_type": "single"},
        {"question_text": "What is the hexadecimal equivalent of binary 11001100?",
         "option_a": "CC", "option_b": "CD", "option_c": "DD", "option_d": "CE", "correct_option": "option_a", "question_type": "single"},
        {"question_text": "Which image file format uses lossy compression?",
         "option_a": "PNG", "option_b": "BMP", "option_c": "JPEG", "option_d": "TIFF", "correct_option": "option_c", "question_type": "single"},
        {"question_text": "How many kilobytes are there in a megabyte?",
         "option_a": "1024", "option_b": "1000", "option_c": "2048", "option_d": "512", "correct_option": "option_a", "question_type": "single"},
        {"question_text": "What is the binary equivalent of the decimal number 19?",
         "option_a": "10010", "option_b": "10011", "option_c": "10100", "option_d": "10101", "correct_option": "option_b", "question_type": "single"},
        {"question_text": "Which of the following uses the most storage space?",
         "option_a": "1-minute uncompressed audio file", "option_b": "1-minute compressed MP3 file", "option_c": "1-page text document", "option_d": "Low-resolution image", "correct_option": "option_a", "question_type": "single"},
        {"question_text": "How is text stored in a computer?",
         "option_a": "As binary numbers", "option_b": "As hexadecimal values", "option_c": "As ASCII codes", "option_d": "All of the above", "correct_option": "option_d", "question_type": "single"},
        {"question_text": "What is the RGB value for white?",
         "option_a": "255, 255, 255", "option_b": "0, 0, 0", "option_c": "255, 0, 0", "option_d": "0, 255, 255", "correct_option": "option_a", "question_type": "single"},
        {"question_text": "Which number system is commonly used for representing color in digital images?",
         "option_a": "Decimal", "option_b": "Binary", "option_c": "Hexadecimal", "option_d": "Octal", "correct_option": "option_c", "question_type": "single"},
        {"question_text": "What is the storage size of a standard character in Unicode?",
         "option_a": "1 byte", "option_b": "2 bytes", "option_c": "4 bytes", "option_d": "8 bytes", "correct_option": "option_b", "question_type": "single"},
        {"question_text": "What is the function of a file header in image files?",
         "option_a": "Stores metadata", "option_b": "Stores pixel data", "option_c": "Compresses data", "option_d": "Detects errors", "correct_option": "option_a", "question_type": "single"},
        {"question_text": "How many distinct characters can ASCII represent?",
         "option_a": "128", "option_b": "256", "option_c": "512", "option_d": "1024", "correct_option": "option_a", "question_type": "single"},
        {"question_text": "What does DPI stand for?",
         "option_a": "Dots per inch", "option_b": "Data per input", "option_c": "Digits per input", "option_d": "Data processing index", "correct_option": "option_a", "question_type": "single"},
        {"question_text": "What is the binary representation of hexadecimal 1F?",
         "option_a": "00011111", "option_b": "11111000", "option_c": "11111100", "option_d": "11001111", "correct_option": "option_a", "question_type": "single"},
        {"question_text": "What is the hexadecimal equivalent of decimal 255?",
         "option_a": "FF", "option_b": "FE", "option_c": "EF", "option_d": "EE", "correct_option": "option_a", "question_type": "single"},
        {"question_text": "What does a sampling rate determine in audio files?",
         "option_a": "Frequency of samples", "option_b": "File size", "option_c": "Audio quality", "option_d": "All of the above", "correct_option": "option_d", "question_type": "single"},
        
        # Hard Questions (25)
        {"question_text": "Convert 1 GB to bits.",
         "option_a": "8 billion bits", "option_b": "10 billion bits", "option_c": "8,589,934,592 bits", "option_d": "10,000,000,000 bits", "correct_option": "option_c", "question_type": "single"},
        {"question_text": "What is the binary representation of the Unicode character '©'?",
         "option_a": "00101100", "option_b": "10101100", "option_c": "11001100", "option_d": "11101100", "correct_option": "option_b", "question_type": "single"},
        {"question_text": "How many bits are required to represent 1,048,576 colors?",
         "option_a": "24", "option_b": "32", "option_c": "20", "option_d": "16", "correct_option": "option_a", "question_type": "single"},
        {"question_text": "What is the hexadecimal representation of 2’s complement binary 11101101?",
         "option_a": "ED", "option_b": "DF", "option_c": "EE", "option_d": "EF", "correct_option": "option_a", "question_type": "single"},
        {"question_text": "What is the result of a binary XOR operation between 1010 and 1100?",
         "option_a": "0110", "option_b": "1010", "option_c": "1111", "option_d": "1100", "correct_option": "option_a", "question_type": "single"},
        {"question_text": "What is the storage requirement for an image with a resolution of 1024x768 and 24-bit color depth?",
         "option_a": "2 MB", "option_b": "3 MB", "option_c": "4 MB", "option_d": "1 MB", "correct_option": "option_b", "question_type": "single"},
        {"question_text": "Perform binary addition: 1110 + 1011.",
         "option_a": "11001", "option_b": "10101", "option_c": "10001", "option_d": "11111", "correct_option": "option_a", "question_type": "single"},
        {"question_text": "What is the decimal equivalent of the 2’s complement binary 11101101?",
         "option_a": "-19", "option_b": "-18", "option_c": "-17", "option_d": "-16", "correct_option": "option_a", "question_type": "single"},
        {"question_text": "What is the binary floating-point representation of 1.75?",
         "option_a": "1.11 x 2^0", "option_b": "1.10 x 2^0", "option_c": "1.01 x 2^1", "option_d": "1.00 x 2^1", "correct_option": "option_a", "question_type": "single"},
        {"question_text": "What is the storage space required for 3 minutes of uncompressed audio with a sampling rate of 44.1 kHz, 16-bit depth, and 2 channels?",
         "option_a": "30 MB", "option_b": "15 MB", "option_c": "10 MB", "option_d": "40 MB", "correct_option": "option_a", "question_type": "single"}
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
