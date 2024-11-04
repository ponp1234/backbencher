from app import db, Question, Exam, app  # Import app and models from your main application

# Example exam title to delete and recreate
exam_title = "Computer Science Paper "

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
        {
            "question_text": "(ii) Tick (✓) to show whether the MP3 file is a lossy compressed file or a lossless compressed file or not a compressed file.",
            "option_a": "Lossy compressed file",
            "option_b": "Lossless compressed file",
            "option_c": "Not a compressed file",
            "correct_option": "option_a",
            "question_type": "single"
        },
        # Question 2
        {
            "question_text": "A computer is designed using the Von Neumann model for a computer system.\n\n(a) (i) State the name of the primary storage from where data is fetched.",
            "blanks": 1,
            "correct_options": "RAM",
            "question_type": "fill_in_the_blank"
        },
        {
            "question_text": "(ii) The CPU performs a cycle to process data. Fetch is the first stage in this cycle.\n\nState the names of the second and third stages in the cycle.",
            "blanks": 2,
            "correct_options": "Decode,Execute",
            "question_type": "fill_in_the_blank"
        },
        {
            "question_text": "(iii) Identify two components within the CPU that are used in the fetch stage of the cycle.",
            "blanks": 2,
            "correct_options": "Control Unit,Register",
            "question_type": "fill_in_the_blank"
        },
        # Question 3
        {
            "question_text": "Identify one other example of solid-state storage.",
            "blanks": 1,
            "correct_options": "USB Flash Drive",
            "question_type": "fill_in_the_blank"
        },
        {
            "question_text": "Explain how a laser is used to store and read data from a disk.",
            "blanks": 3,
            "correct_options": "Reflective surface,Pits and lands,Light sensor",
            "question_type": "fill_in_the_blank"
        },
        # Question 4
        {
            "question_text": "All data needs to be converted to binary data so that it can be processed by a computer.\n\n(a) Explain why a computer can only process binary data.",
            "blanks": 1,
            "correct_options": "Binary is the language of the CPU",
            "question_type": "fill_in_the_blank"
        },
        {
            "question_text": "(b) The denary values 64, 101 and 242 are converted to 8‑bit binary values.\n\nGive the 8‑bit binary value for each denary value.",
            "blanks": 3,
            "correct_options": "01000000,01100101,11110010",
            "question_type": "fill_in_the_blank"
        },
        # Question 5
        {
            "question_text": "Calculate the file size of an image with 16-bit color, 100 pixels high, and 150 pixels wide in bytes.",
            "blanks": 1,
            "correct_options": "30000",
            "question_type": "fill_in_the_blank"
        },
        # Question 6
        {
            "question_text": "A compiler and an interpreter are two different types of translator.\n\n(a) One similarity between a compiler and an interpreter is that they both translate high‑level language into machine code.\n\n(i) Give one other similarity between a compiler and an interpreter.",
            "blanks": 1,
            "correct_options": "Both check for syntax errors",
            "question_type": "fill_in_the_blank"
        },
        {
            "question_text": "(ii) Explain two differences between a compiler and an interpreter.",
            "blanks": 2,
            "correct_options": "Compiler translates entire code at once,Interpreter translates line by line",
            "question_type": "fill_in_the_blank"
        },
        # Question 7
        {
            "question_text": "State what is meant by a biometric password.",
            "blanks": 1,
            "correct_options": "A password based on biological characteristics",
            "question_type": "fill_in_the_blank"
        },
        {
            "question_text": "Explain how a firewall keeps a device secure.",
            "blanks": 2,
            "correct_options": "Monitors incoming and outgoing traffic,Blocks unauthorized access",
            "question_type": "fill_in_the_blank"
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
        },
        # Question 10
        {
            "question_text": "Identify and describe three ethical issues related to Internet use.",
            "blanks": 3,
            "correct_options": "Privacy concerns,Cyberbullying,Digital piracy",
            "question_type": "fill_in_the_blank"
        },
        # Question 11
        {
            "question_text": "Describe the function of the ALU within the CPU.",
            "blanks": 1,
            "correct_options": "Performs arithmetic and logical operations",
            "question_type": "fill_in_the_blank"
        },
        # Question 12
        {
            "question_text": "Explain why cache memory is faster than RAM.",
            "blanks": 1,
            "correct_options": "Cache is closer to the CPU",
            "question_type": "fill_in_the_blank"
        },
        # Question 13
        {
            "question_text": "List two examples of magnetic storage devices.",
            "blanks": 2,
            "correct_options": "Hard Disk Drive,Magnetic Tape",
            "question_type": "fill_in_the_blank"
        },
        # Question 14
        {
            "question_text": "State one advantage and one disadvantage of using optical storage.",
            "blanks": 2,
            "correct_options": "Portable,Easily scratched",
            "question_type": "fill_in_the_blank"
        },
        # Question 15
        {
            "question_text": "Name two differences between SSDs and HDDs.",
            "blanks": 2,
            "correct_options": "SSD has no moving parts,HDD has a higher failure rate",
            "question_type": "fill_in_the_blank"
        },
        # Question 16
        {
            "question_text": "Convert the denary number 255 into an 8-bit binary number.",
            "blanks": 1,
            "correct_options": "11111111",
            "question_type": "fill_in_the_blank"
        },
        # Question 17
        {
            "question_text": "Convert the hexadecimal number FA into binary.",
            "blanks": 1,
            "correct_options": "11111010",
            "question_type": "fill_in_the_blank"
        },
        # Question 18
        {
            "question_text": "Explain one advantage of hexadecimal notation over binary.",
            "blanks": 1,
            "correct_options": "Hexadecimal is easier to read",
            "question_type": "fill_in_the_blank"
        },
        # Question 19
        {
            "question_text": "Define the term 'protocol' in computer networks.",
            "blanks": 1,
            "correct_options": "A set of rules for communication",
            "question_type": "fill_in_the_blank"
        },
        # Question 20
        {
            "question_text": "State two functions of a network router.",
            "blanks": 2,
            "correct_options": "Directs data packets,Connects multiple networks",
            "question_type": "fill_in_the_blank"
        },
        # Question 21
        {
            "question_text": "Describe how a firewall can help prevent unauthorized access.",
            "blanks": 1,
            "correct_options": "Filters incoming and outgoing traffic",
            "question_type": "fill_in_the_blank"
        },
        # Question 22
        {
            "question_text": "What does 'IP address' stand for, and what is its purpose?",
            "blanks": 2,
            "correct_options": "Internet Protocol,Identifies devices on a network",
            "question_type": "fill_in_the_blank"
        },
        # Question 23
        {
            "question_text": "Identify the purpose of the MAC address in networking.",
            "blanks": 1,
            "correct_options": "Uniquely identifies each network device",
            "question_type": "fill_in_the_blank"
        },
        # Question 24
        {
            "question_text": "Explain why binary is used in digital systems.",
            "blanks": 1,
            "correct_options": "Binary is simple and reliable for circuits",
            "question_type": "fill_in_the_blank"
        },
        # Question 25
        {
            "question_text": "Describe the purpose of an operating system.",
            "blanks": 1,
            "correct_options": "Manages hardware and software resources",
            "question_type": "fill_in_the_blank"
        },
        # Question 26
        {
            "question_text": "Give two functions of the OS in managing files.",
            "blanks": 2,
            "correct_options": "Organizes files,Controls file access",
            "question_type": "fill_in_the_blank"
        },
        # Question 27
        {
            "question_text": "Explain what 'open-source software' means.",
            "blanks": 1,
            "correct_options": "Software with publicly available source code",
            "question_type": "fill_in_the_blank"
        },
        # Question 28
        {
            "question_text": "State one advantage of using open-source software.",
            "blanks": 1,
            "correct_options": "Can be modified and customized",
            "question_type": "fill_in_the_blank"
        },
        # Question 29
        {
            "question_text": "Describe one risk of using open-source software.",
            "blanks": 1,
            "correct_options": "May lack professional support",
            "question_type": "fill_in_the_blank"
        },
        # Question 30
        {
            "question_text": "Identify one difference between proprietary and open-source software.",
            "blanks": 1,
            "correct_options": "Proprietary is closed-source",
            "question_type": "fill_in_the_blank"
        },
        # Question 31
        {
            "question_text": "Explain the term 'algorithm'.",
            "blanks": 1,
            "correct_options": "A set of steps to solve a problem",
            "question_type": "fill_in_the_blank"
        },
        # Question 32
        {
            "question_text": "Write the binary equivalent of decimal number 27.",
            "blanks": 1,
            "correct_options": "00011011",
            "question_type": "fill_in_the_blank"
        },
        # Question 33
        {
            "question_text": "Define 'machine code'.",
            "blanks": 1,
            "correct_options": "Low-level code understood by the CPU",
            "question_type": "fill_in_the_blank"
        },
        # Question 34
        {
            "question_text": "Explain why high-level languages are easier for humans to understand.",
            "blanks": 1,
            "correct_options": "They are closer to human languages",
            "question_type": "fill_in_the_blank"
        },
        # Question 35
        {
            "question_text": "Define the term 'variable' in programming.",
            "blanks": 1,
            "correct_options": "A storage location for data",
            "question_type": "fill_in_the_blank"
        },
        # Question 36
        {
            "question_text": "What is a syntax error?",
            "blanks": 1,
            "correct_options": "An error in the structure of code",
            "question_type": "fill_in_the_blank"
        },
        # Question 37
        {
            "question_text": "Explain what a logic error is.",
            "blanks": 1,
            "correct_options": "An error that produces incorrect results",
            "question_type": "fill_in_the_blank"
        },
        # Question 38
        {
            "question_text": "Describe the purpose of comments in programming.",
            "blanks": 1,
            "correct_options": "To explain code for easier understanding",
            "question_type": "fill_in_the_blank"
        },
        # Question 39
        {
            "question_text": "What is a loop in programming?",
            "blanks": 1,
            "correct_options": "A sequence that repeats until a condition is met",
            "question_type": "fill_in_the_blank"
        },
        # Question 40
        {
            "question_text": "State the purpose of an 'if' statement in programming.",
            "blanks": 1,
            "correct_options": "To make decisions based on conditions",
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
