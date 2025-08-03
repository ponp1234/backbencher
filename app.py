from flask import Flask, render_template, redirect, url_for, flash, request, session, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from datetime import datetime
from datetime import datetime, timedelta
from sqlalchemy import text, exc
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker


app = Flask(__name__)
app.config['SECRET_KEY'] = '12345'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site6.db'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# Separate database for this API
EXECUTE_QUERY_DB_URI = 'sqlite:///dummy.db'  # Replace with API-specific DB URL
execute_query_engine = create_engine(EXECUTE_QUERY_DB_URI, pool_pre_ping=True)
SessionLocal = sessionmaker(bind=execute_query_engine)






class WalletTransaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    transaction_type = db.Column(db.String(50), nullable=False)  # 'Initial', 'Allowance', 'Spending'
    amount = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(200), nullable=True)  # Optional description

    # Relationship
    user = db.relationship('User', backref='wallet_transactions', lazy=True)

class LearningProgress(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    topic_code = db.Column(db.String(50), nullable=False)  # e.g., 'plants', 'animals'
    completed = db.Column(db.Boolean, default=False)
    completed_at = db.Column(db.DateTime, nullable=True)

    user = db.relationship('User', backref='learning_progress', lazy=True)



class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    exam_id = db.Column(db.Integer, db.ForeignKey('exam.id'), nullable=False)
    question_text = db.Column(db.String(500), nullable=False)
    option_a = db.Column(db.String(100), nullable=True)  # For single/multiple-choice questions
    option_b = db.Column(db.String(100), nullable=True)
    option_c = db.Column(db.String(100), nullable=True)
    option_d = db.Column(db.String(100), nullable=True)
    correct_option = db.Column(db.String(1), nullable=True)  # For single-choice questions
    correct_options = db.Column(db.String(100), nullable=True)  # Comma-separated correct answers for multiple-choice or fill-in-the-blank
    blanks = db.Column(db.Integer, nullable=True)  # Number of blanks for fill-in-the-blank questions
    question_type = db.Column(db.String(20), nullable=False, default="single")  # 'single', 'multiple', 'fill_in_the_blank'


class ExamAttempt(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    exam_id = db.Column(db.Integer, db.ForeignKey('exam.id'), nullable=False)
    score = db.Column(db.Integer, nullable=False)
    total_questions = db.Column(db.Integer, nullable=False)
    attempt_date = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    user = db.relationship('User', backref='attempts', lazy=True)
    exam = db.relationship('Exam', backref='attempts', lazy=True)
    
class ToDo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task = db.Column(db.String(200), nullable=False)
    date = db.Column(db.Date, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)


# User Model
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    student_class = db.Column(db.String(50), unique=True, nullable=False)  
    wallet_balance = db.Column(db.Float, default=0.0)  # New field to store total balance

class ExamMapping(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    exam_id = db.Column(db.Integer, db.ForeignKey('exam.id'), nullable=False)
    class_name = db.Column(db.String(50), nullable=False)  # Stores the class name


class Learning(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)  # Title of the learning material
    desc = db.Column(db.Text, nullable=True)           # Description of the learning material
    code = db.Column(db.String(50), nullable=False)    # Code identifier for the learning material


class LearningsMapping(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    learning_id = db.Column(db.Integer, db.ForeignKey('learning.id'), nullable=False)
    class_name = db.Column(db.String(50), nullable=False)  # Maps to the class

class HTMLMapping(db.Model):
    id = db.Column(db.Integer, primary_key=True)     # Primary key
    code = db.Column(db.String(50), nullable=False)  # Unique code identifier
    html = db.Column(db.String(50), nullable=False)        # HTML 


    @app.route('/wallet', methods=['GET', 'POST'])
    @login_required
    def wallet():
        if request.method == 'POST':
            transaction_type = request.form.get('transaction_type')
            amount = float(request.form.get('amount'))
            description = request.form.get('description', '')
            
            if transaction_type == 'Initial':
                # Set initial money
                current_user.wallet_balance = amount
                description = 'Set Initial Money'
            elif transaction_type == 'Allowance':
                # Add daily allowance
                current_user.wallet_balance += amount
                description = 'Added Daily Allowance'
            elif transaction_type == 'Spending':
                # Deduct spending
                if amount > current_user.wallet_balance:
                    flash("Insufficient balance!", "danger")
                    return redirect(url_for('wallet'))
                current_user.wallet_balance -= amount
                description = f"Spent on {description}"
    
            # Save transaction
            transaction = WalletTransaction(
                user_id=current_user.id,
                transaction_type=transaction_type,
                amount=amount,
                description=description
            )
            db.session.add(transaction)
            db.session.commit()
    
            flash(f"Transaction successful! New Balance: ${current_user.wallet_balance:.2f}", "success")
            return redirect(url_for('wallet'))
        
        # Fetch transactions
        transactions = (WalletTransaction.query
                    .filter_by(user_id=current_user.id)
                    .order_by(WalletTransaction.date.desc())
                    .limit(20)
                    .all())
        return render_template('wallet.html', transactions=transactions, balance=current_user.wallet_balance)



# Exam model (must be defined before Question model)
class Exam(db.Model):
    __tablename__ = 'exam'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    questions = db.relationship('Question', backref='exam', lazy=True)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/help")
def help():
    return render_template("help.html")




@app.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        student_class = request.form['student_class']  # Get class information from the form
        
        # Check if username already exists
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash('Username already exists. Please choose a different one.', 'danger')
            return redirect(url_for('register'))
        
        # Hash the password and create new user
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        user = User(username=username, password=hashed_password, student_class=student_class)
        db.session.add(user)
        db.session.commit()
        
        flash('Your account has been created!', 'success')
        return redirect(url_for('register'))
    
    return render_template('register.html')

@app.route('/update_learning_progress', methods=['POST'])
@login_required
def update_learning_progress():
    data = request.get_json()
    topic = data.get('topic')
    if not topic:
        return jsonify({'error': 'No topic provided'}), 400

    progress = LearningProgress.query.filter_by(user_id=current_user.id, topic_code=topic).first()
    if not progress:
        progress = LearningProgress(
            user_id=current_user.id,
            topic_code=topic,
            completed=True,
            completed_at=datetime.utcnow()
        )
        db.session.add(progress)
    else:
        progress.completed = True
        progress.completed_at = datetime.utcnow()
    db.session.commit()
    return jsonify({'success': True})

@app.route('/P4_science')
@login_required
def p4_science():
    # Query the user's progress from the database
    progress = LearningProgress.query.filter_by(user_id=current_user.id).all()
    completed_topics = len([p for p in progress if p.completed])
    total_points = sum([p.points for p in progress])  # If you track points per topic
    return render_template('P4_science.html', completed_topics=completed_topics, total_points=total_points)

@app.route('/countdown')
@login_required
def countdown():
    return render_template('countdown.html')

@app.route('/game')
@login_required
def game():
    return render_template('game.html')


@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/terms')
def terms():
    return render_template('terms.html')

@app.route('/privacy')
def privacy():
    return render_template('privacy.html')


@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = User.query.filter_by(username=request.form['username']).first()
        if user and bcrypt.check_password_hash(user.password, request.form['password']):
            login_user(user)
            return redirect(url_for('dashboard'))  # Redirect to user home page after login
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html')


@app.route("/attempts")
@login_required
def attempts():
    attempts = ExamAttempt.query.filter_by(user_id=current_user.id).order_by(ExamAttempt.attempt_date.desc()).all()
    return render_template("attempts.html", attempts=attempts)


@app.route("/learn/<code>", endpoint="learn")
@login_required
def dynamic_html(code):
    # Fetch the HTML mapping for the given code
    mapping = HTMLMapping.query.filter_by(code=code).first()

    if mapping:
        try:
            # Render the specified HTML file dynamically
            progress = LearningProgress.query.filter_by(user_id=current_user.id).all()
            completed_topics = len([p for p in progress if p.completed])
            # If you want to track points, add a points field to LearningProgress and sum here.
            total_points = 10 * completed_topics  # Example: 10 points per completed topic
            return render_template(mapping.html, completed_topics=completed_topics, total_points=total_points)
        except Exception:
            flash(f"HTML file '{mapping.html}' not found.", "danger")
            return redirect(url_for('home'))
    else:
        # Handle the case where the code is not found
        flash(f"No learning material found for code: {code}", "danger")
        return redirect(url_for('home'))



@app.route("/profile")
@login_required
def profile():
    return render_template("profile.html")

@app.route("/settings")
@login_required
def settings():
    return render_template("settings.html")

@app.route("/result/<int:score>/<int:total>")
@login_required
def result(score, total):
    return render_template("result.html", score=score, total=total)


@app.route("/exam/<int:exam_id>/<int:question_number>", methods=['GET', 'POST'])
@login_required
def exam(exam_id, question_number):
    exam = Exam.query.get_or_404(exam_id)
    questions = Question.query.filter_by(exam_id=exam_id).all()
    question = questions[question_number - 1]

    if request.method == 'POST':
        try:
            # Parse JSON data
            data = request.get_json()
            print("Received JSON Data:", data)  # Debugging - print the received JSON
            
            question_type = question.question_type
            score_increment = 0  # Initialize score increment

            if question_type == 'fill_in_the_blank':
                # Handle fill-in-the-blank answers
                correct_answers = question.correct_options.split(',')
                user_answers = data.get('answers', [])
                if len(user_answers) != question.blanks:
                    return jsonify({'error': 'Number of answers does not match the number of blanks'}), 400
                
                user_correct_count = sum(
                    1 for i, user_answer in enumerate(user_answers)
                    if user_answer.strip().lower() == correct_answers[i].strip().lower()
                )
                if user_correct_count == question.blanks:
                    score_increment = 1

            elif question_type == 'multiple':
                # Handle multiple-answer questions
                user_answers = data.get('answers', [])
                correct_answers = question.correct_options.split(',')
                if set(user_answers) == set(correct_answers):
                    score_increment = 1

            elif question_type == 'single':
                # Handle single-answer questions
                user_answer = data.get('answer')
                if user_answer == question.correct_option:
                    score_increment = 1

            # Update score
            session['score'] = session.get('score', 0) + score_increment
            session.modified = True

            # If it's the last question, show the results
            if question_number == len(questions):
                final_score = session.get('score', 0)

                # Save attempt to the database
                attempt = ExamAttempt(
                    user_id=current_user.id,
                    exam_id=exam_id,
                    score=final_score,
                    total_questions=len(questions),
                    attempt_date=datetime.utcnow()
                )
                db.session.add(attempt)
                db.session.commit()

                session.pop('score', None)
                return jsonify({'message': 'Exam completed', 'score': final_score, 'total_questions': len(questions)})

            # Redirect to the next question
            return jsonify({'message': 'Question processed', 'next_question': question_number + 1})

        except Exception as e:
            print("Error:", str(e))
            return jsonify({'error': 'Invalid JSON data or processing error', 'details': str(e)}), 400

    # GET request - render the question page
    return render_template(
        'exam_question.html',
        exam=exam,
        question=question,
        question_number=question_number,
        total_questions=len(questions)
    )

    return render_template('exam_question.html', exam=exam, question=question, question_number=question_number, total_questions=len(questions))



@app.route("/check-answer", methods=['POST'])
@login_required
def check_answer():
    data = request.json
    exam_id = data.get('examId')
    question_number = int(data.get('questionNumber'))
    
    # Get the question
    questions = Question.query.filter_by(exam_id=exam_id).all()
    question = questions[question_number - 1]
    
    is_correct = False
    explanation = ""
    correct_answer = None
    
    if question.question_type == 'fill_in_the_blank':
        correct_answers = question.correct_options.split(',')
        user_answers = data.get('userAnswers', {})
        correct_count = 0
        
        for i in range(1, question.blanks + 1):
            user_answer = user_answers.get(f"blank{i}", "").strip().lower()
            if user_answer == correct_answers[i - 1].strip().lower():
                correct_count += 1
                
        is_correct = correct_count == question.blanks
        correct_answer = correct_answers
        explanation = f"The correct answer{'s are' if len(correct_answers) > 1 else ' is'}: {', '.join(correct_answers)}"
        
    elif question.question_type == 'multiple':
        user_answers = set(data.get('userAnswers', []))
        correct_answers = set(question.correct_options.split(','))
        is_correct = user_answers == correct_answers
        correct_answer = list(correct_answers)
        explanation = f"The correct answers are: {', '.join(correct_answer)}"
        
    else:  # single choice
        user_answer = data.get('userAnswers')
        is_correct = user_answer == question.correct_option
        correct_answer = question.correct_option
        explanation = f"The correct answer is: {question.correct_option}"
    
    return jsonify({
        'isCorrect': is_correct,
        'correctAnswer': correct_answer,
        'explanation': explanation
    })

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route("/user_home")
@login_required
def user_home():
    # Get all past attempts by the current user
    # Define today's and tomorrow's dates
    today = datetime.now().date()
    tomorrow = today + timedelta(days=1)
    
    # Filter To-Do items by date
    todos = ToDo.query.filter(
        ToDo.user_id == current_user.id,
        ToDo.date.in_([today, tomorrow])  # Filter for today and tomorrow
    ).order_by(ToDo.date.asc()).all()
    
    print(todos)
    # Get the current user's student class
    user_class = current_user.student_class
    print(user_class)
   
    # Fetch exams mapped to the user's student class
    exams = db.session.query(Exam).join(ExamMapping).filter(ExamMapping.class_name == user_class).all()
    
    learnings = db.session.query(Learning).join(LearningsMapping).filter(LearningsMapping.class_name == user_class).all()
    
    return render_template("user_home.html", exams=exams, attempts=attempts, learnings=learnings, todos=todos)


@app.route("/papers")
@login_required
def papers():
    # Get all past attempts by the current user
    # Define today's and tomorrow's dates
    today = datetime.now().date()
    tomorrow = today + timedelta(days=1)
    
    # Filter To-Do items by date
    todos = ToDo.query.filter(
        ToDo.user_id == current_user.id,
        ToDo.date.in_([today, tomorrow])  # Filter for today and tomorrow
    ).order_by(ToDo.date.asc()).all()
    
    print(todos)
    # Get the current user's student class
    user_class = current_user.student_class
    print(user_class)
   
    # Fetch exams mapped to the user's student class
    exams = db.session.query(Exam).join(ExamMapping).filter(ExamMapping.class_name == user_class).all()
    
    learnings = db.session.query(Learning).join(LearningsMapping).filter(LearningsMapping.class_name == user_class).all()
    
    return render_template("papers.html", exams=exams, attempts=attempts, learnings=learnings, todos=todos)

@app.route("/pastpapers")
@login_required
def pastpapers():
    # Get all past attempts by the current user
    # Define today's and tomorrow's dates
    today = datetime.now().date()
    tomorrow = today + timedelta(days=1)
    
    # Filter To-Do items by date
    todos = ToDo.query.filter(
        ToDo.user_id == current_user.id,
        ToDo.date.in_([today, tomorrow])  # Filter for today and tomorrow
    ).order_by(ToDo.date.asc()).all()
    
    print(todos)
    # Get the current user's student class
    user_class = current_user.student_class
    print(user_class)
   
    # Fetch exams mapped to the user's student class
    exams = db.session.query(Exam).join(ExamMapping).filter(ExamMapping.class_name == user_class).all()
    
    learnings = db.session.query(Learning).join(LearningsMapping).filter(LearningsMapping.class_name == user_class).all()
    
    return render_template("pastpapers.html", exams=exams, attempts=attempts, learnings=learnings, todos=todos)


@app.route("/dashboard")
@login_required
def dashboard():
    # Get all past attempts by the current user
    # Define today's and tomorrow's dates
    today = datetime.now().date()
    tomorrow = today + timedelta(days=1)
    
    # Filter To-Do items by date
    todos = ToDo.query.filter(
        ToDo.user_id == current_user.id,
        ToDo.date.in_([today, tomorrow])  # Filter for today and tomorrow
    ).order_by(ToDo.date.asc()).all()
    
    print(todos)
    # Get the current user's student class
    user_class = current_user.student_class
    print(user_class)
   
    # Fetch exams mapped to the user's student class
    exams = db.session.query(Exam).join(ExamMapping).filter(ExamMapping.class_name == user_class).all()
    
    learnings = db.session.query(Learning).join(LearningsMapping).filter(LearningsMapping.class_name == user_class).all()
    
    return render_template("dashboard.html", exams=exams, attempts=attempts, learnings=learnings, todos=todos)


@app.route("/access_home")
@login_required
def access_home():
    # Get all past attempts by the current user
    attempts = ExamAttempt.query.filter_by(user_id=current_user.id).order_by(ExamAttempt.attempt_date.desc()).all()
    exams = Exam.query.all()  # Fetch all available exams
    
    return render_template("access_home.html", exams=exams, attempts=attempts)

import google.generativeai as genai
from flask_cors import CORS

CORS(app)


# Configure the Gemini API
genai.configure(api_key='AIzaSyB265GIXXq5REPMHi_y_X1luKzaDFtgR6E')

# Initialize Gemini model
model = genai.GenerativeModel('gemini-pro')

@app.route('/ask-ai', methods=['POST'])
def ask_gemini():
    try:
        data = request.json
        question = data['messages'][0]['content']
        
        # Add better error handling and logging
        print(f"Received question: {question}")  # Debug log
        
        # Structure the prompt
        prompt = f"""Please help explain this exam question and provide guidance with respect to IGCSC sylabus. 
        Question: {question}
        Please provide:
        1. A clear explanation of the question
        2. Key concepts to consider
        3. Approach to solving it 
        """
        
        try:
            # Generate response using Gemini
            response = model.generate_content(prompt)
            
            # Debug logging
            print("API Response received")
            
            return jsonify({
                'response': response.text if hasattr(response, 'text') else str(response)
            })
            
        except Exception as api_error:
            print(f"Gemini API error: {str(api_error)}")  # Debug log
            return jsonify({
                'error': f"Gemini API error: {str(api_error)}"
            }), 500
    
    except Exception as e:
        print(f"Server error: {str(e)}")  # Debug log
        return jsonify({
            'error': f"Server error: {str(e)}"
        }), 500

@app.route('/check-with-ai', methods=['POST'])
def check_gemini():
    try:
        data = request.json
        exam_id = data['messages'][0]['examId']
        question_number = int(data['messages'][0]['questionNumber'])
        
        # Get the question
        questions = Question.query.filter_by(exam_id=exam_id).all()
        question = questions[question_number - 1]
        
        correct_answer = None
        correct_answers = question.correct_options       

        question_text = data['messages'][0]['content']
        
        # Add better error handling and logging
        print(f"Received question: {question}")  # Debug log
        
        # Structure the prompt
        prompt = f"""
        {question_text}
        expected answer: {correct_answers}
        Please provide:
        1. A clear explanation why the useranswer: is correct or incorrect or partialy correct with a score from 0 to 100 based on the  expected answer
        """
        
        try:
            # Generate response using Gemini
            response = model.generate_content(prompt)
            
            # Debug logging
            print("API Response received")
            
            return jsonify({
                'response': response.text if hasattr(response, 'text') else str(response)
            })
            
        except Exception as api_error:
            print(f"Gemini API error: {str(api_error)}")  # Debug log
            return jsonify({
                'error': f"Gemini API error: {str(api_error)}"
            }), 500
    
    except Exception as e:
        print(f"Server error: {str(e)}")  # Debug log
        return jsonify({
            'error': f"Server error: {str(e)}"
        }), 500


@app.route('/add_todo', methods=['POST'])
@login_required
def add_todo():
    task = request.form['task']
    date_str = request.form['date']  # This is a string
    try:
        date = datetime.strptime(date_str, "%Y-%m-%d").date()  # Convert to datetime.date
    except ValueError:
        flash("Invalid date format. Please use YYYY-MM-DD.", "danger")
        return redirect(url_for('user_home'))

    new_todo = ToDo(task=task, date=date, user_id=current_user.id)
    db.session.add(new_todo)
    db.session.commit()
    return redirect(url_for('task'))

@app.route('/update_todo/<int:todo_id>', methods=['POST'])
@login_required
def update_todo(todo_id):
    todo = ToDo.query.get_or_404(todo_id)
    if todo.user_id != current_user.id:
        abort(403)

    task = request.form['task']
    date_str = request.form.get('date')  # Optional date update
    if date_str:
        try:
            todo.date = datetime.strptime(date_str, "%Y-%m-%d").date()
        except ValueError:
            flash("Invalid date format. Please use YYYY-MM-DD.", "danger")
            return redirect(url_for('user_home'))

    todo.task = task
    db.session.commit()
    return redirect(url_for('task'))

@app.route("/task")
@login_required
def task():
    todos = ToDo.query.filter_by(user_id=current_user.id).order_by(ToDo.date.asc()).all()
    return render_template("task.html", todos=todos)

@app.route('/delete_todo/<int:todo_id>', methods=['POST'])
@login_required
def delete_todo(todo_id):
    todo = ToDo.query.get_or_404(todo_id)
    if todo.user_id != current_user.id:
        abort(403)
    db.session.delete(todo)
    db.session.commit()

    return redirect(url_for('task'))

# Change class route
@app.route('/change_class', methods=['POST'])
@login_required
def change_class():
    new_class = request.form.get('class')
    if new_class:
        current_user.student_class = new_class  # Update the `student_class` field
        db.session.commit()
        flash('Class updated successfully!', 'success')
    else:
        flash('Please select a valid class.', 'error')
    return redirect(url_for('settings'))


@app.route("/calc")
@login_required
def calc():
    return render_template("calc.html")


@app.route('/dbq')
@login_required
def dbq():
    return render_template('dbq.html')



@app.route('/execute_query', methods=['POST'])
@login_required
def execute_query():
    session = SessionLocal()  # Create a new session for this API request
    try:
        data = request.get_json()
        queries = data.get('queries', [])  # Expecting a list of queries

        if not queries or not isinstance(queries, list):
            return jsonify({'error': 'No valid queries provided'})

        # Prevent destructive queries
        for query in queries:
            query_lower = query.lower()
            if any(word in query_lower for word in ['alter']):
                return jsonify({'error': 'Data modification queries are not allowed'})

        print("Executing queries...")

        results = []
        for query in queries:
            result = session.execute(text(query))
            if result.returns_rows:
                rows = [dict(row) for row in result.mappings()]
                results.append({'query': query, 'results': rows})
            else:
                results.append({'query': query, 'message': 'Query executed successfully'})

        session.close()  # Close session after execution
        return jsonify({'queries_results': results})

    except Exception as e:
        session.rollback()  # Rollback in case of failure
        return jsonify({'error': str(e)})

    finally:
        session.close()  # Ensure session is closed
        
if __name__ == '__main__':
    with app.app_context():
        
        db.create_all()  # Creates database tables if they don't exist

    context = (r'/home/bb/exam/ssl/bb.pem', r'/home/bb/exam/ssl/bb.key')
    app.run(host='0.0.0.0', port=443, debug=True, ssl_context=context)
    
    #app.run(host='0.0.0.0', port=443, debug=True)
