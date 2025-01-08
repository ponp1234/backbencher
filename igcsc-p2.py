from app import db, Question, Exam, app  # Import app and models from your main application

# Example exam title to delete and recreate
exam_title = "Paper 2 002"

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

    # Add the two questions from the image
    questions = [
        {
            "question_text": """
                <div>
                    <p><strong>Question 1:</strong> Tick (✓) one box to show which operator means less than or equal to.</p>
                </div>
            """,
            "option_a": "OR",
            "option_b": "<",
            "option_c": "<=",
            "option_d": ">=",
            "correct_option": "option_c",
            "question_type": "single"
        },
        {
            "question_text": """
                <div>
                    <p><strong>Question 2:</strong> Tick (✓) one box to show how a value can be passed to a procedure.</p>
                </div>
            """,
            "option_a": "function",
            "option_b": "parameter",
            "option_c": "return",
            "option_d": "subroutine",
            "correct_option": "option_b",
            "question_type": "single"
        },
        {
            "question_text": """
                <div>
                    <p><strong>Question 3:</strong> Four descriptions of data and five data types are shown.</p>
                    <p>Draw one line to link each description to the most appropriate data type. Not all data types will be used.</p>
                    <table style="width: 100%; border-collapse: collapse;">
                        <tr>
                            <th style="text-align: left; padding: 10px;">Description</th>
                            <th style="text-align: left; padding: 10px;">Data type</th>
                        </tr>
                        <tr>
                            <td style="padding: 10px;">A whole number</td>
                            <td style="padding: 10px;">INTEGER</td>
                        </tr>
                        <tr>
                            <td style="padding: 10px;">A single letter</td>
                            <td style="padding: 10px;">CHAR</td>
                        </tr>
                        <tr>
                            <td style="padding: 10px;">A word or phrase</td>
                            <td style="padding: 10px;">STRING</td>
                        </tr>
                        <tr>
                            <td style="padding: 10px;">A number with two decimal places</td>
                            <td style="padding: 10px;">REAL</td>
                        </tr>
                    </table>
                </div>
            """,
            "option_a": "INTEGER",
            "option_b": "CHAR",
            "option_c": "STRING",
            "option_d": "REAL",
            "correct_option": "Matching required as described above",
            "question_type": "matching"
        },
        {
            "question_text": """
                <div>
                    <p><strong>Question 4:</strong> Circle the <strong>three words</strong> representing places where data may be stored.</p>
                    <ul>
                        <li>array</li>
                        <li>constant</li>
                        <li>dimension</li>
                        <li>input</li>
                        <li>output</li>
                        <li>procedure</li>
                        <li>variable</li>
                    </ul>
                </div>
            """,
            "blanks": 3,
            "correct_options": "array, constant, variable",
            "question_type": "fill_in_the_blank"
        },
        {
            "question_text": """
                <div>
                    <p><strong>Question 5(a):</strong> Describe what is meant by abstraction.</p>
                </div>
            """,
            "blanks": 1,
            "correct_options": "Abstraction is the process of removing unnecessary details to focus on essential aspects.",
            "question_type": "fill_in_the_blank"
        },
        {
            "question_text": """
                <div>
                    <p><strong>Question 5(b):</strong> Identify <strong>three</strong> of the component parts when a problem has been decomposed at the analysis stage.</p>
                    <ol>
                        <li>....................................................................</li>
                        <li>....................................................................</li>
                        <li>....................................................................</li>
                    </ol>
                </div>
            """,
            "blanks": 3,
            "correct_options": "Inputs, Processes, Outputs",
            "question_type": "fill_in_the_blank"
        },
        {
            "question_text": """
                <div>
                    <p><strong>Question 5(c):</strong> Identify and describe one other stage of the program development life cycle.</p>
                </div>
            """,
            "blanks": 1,
            "correct_options": "Testing: Ensures the program works as expected and meets requirements.",
            "question_type": "fill_in_the_blank"
        },
        {
            "question_text": """
                <div>
                    <p><strong>Question 6(a):</strong> State the purpose of this pseudocode algorithm.</p>
                    <pre>
01 DECLARE A[1:10] : STRING
02 DECLARE T : STRING
03 DECLARE C, L : INTEGER
...
21 NEXT C
                    </pre>
                </div>
            """,
            "blanks": 1,
            "correct_options": "The algorithm sorts an array of names in ascending order.",
            "question_type": "fill_in_the_blank"
        },
        {
            "question_text": """
                <div>
                    <p><strong>Question 6(b):</strong> State four processes in this algorithm.</p>
                </div>
            """,
            "blanks": 4,
            "correct_options": "Data input, Comparison, Swapping elements, Output results",
            "question_type": "fill_in_the_blank"
        },
        {
            "question_text": """
                <div>
                    <p><strong>Question 6(c):</strong> Suggest suitable meaningful identifiers for the following variables:</p>
                    <ul>
                        <li>A</li>
                        <li>T</li>
                        <li>C</li>
                        <li>L</li>
                    </ul>
                </div>
            """,
            "blanks": 4,
            "correct_options": "NamesArray, TempName, Counter, Length",
            "question_type": "fill_in_the_blank"
        },
        {
            "question_text": """
                <div>
                    <p><strong>Question 6(d):</strong> State two other ways the algorithm can be made easier to understand and maintain.</p>
                </div>
            """,
            "blanks": 2,
            "correct_options": "Add comments, Use meaningful variable names",
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
