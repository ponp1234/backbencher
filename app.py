from flask import Flask, render_template, redirect, url_for, flash, request, session, jsonify, abort
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


import logging



# SIMPLE logging fix - just reduce log level
logging.getLogger('werkzeug').setLevel(logging.WARNING)

# SIMPLE bot blocking - only block obvious attacks
@app.before_request
def simple_bot_filter():
    """Very lightweight bot filtering"""
    path = request.path.lower()
    
    # Only block the most obvious bot patterns
    if any(pattern in path for pattern in ['/owa/', '/.env', '/wp-admin']):
        abort(404)

# Add these simple routes to handle common bot requests silently
@app.route('/robots.txt')
def robots():
    return "User-agent: *\nDisallow: /"

@app.route('/favicon.ico')
def favicon():
    return '', 204

# Separate database for this API
EXECUTE_QUERY_DB_URI = 'sqlite:///dummy.db'  # Replace with API-specific DB URL
execute_query_engine = create_engine(EXECUTE_QUERY_DB_URI, pool_pre_ping=True)
SessionLocal = sessionmaker(bind=execute_query_engine)




# Add these new models to your existing app.py

import uuid
import json
from datetime import datetime

class ExamSession(db.Model):
    __tablename__ = 'exam_sessions'
    
    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.String(255), unique=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    exam_id = db.Column(db.Integer, db.ForeignKey('exam.id'), nullable=False)
    start_time = db.Column(db.DateTime, default=datetime.utcnow)
    end_time = db.Column(db.DateTime)
    current_question = db.Column(db.Integer, default=1)
    total_score = db.Column(db.Integer, default=0)
    is_completed = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    user = db.relationship('User', backref='exam_sessions')
    exam = db.relationship('Exam', backref='exam_sessions')
    question_attempts = db.relationship('QuestionAttempt', backref='exam_session', cascade='all, delete-orphan')

class QuestionAttempt(db.Model):
    __tablename__ = 'question_attempts'
    
    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.String(255), db.ForeignKey('exam_sessions.session_id'), nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'), nullable=False)
    user_answer = db.Column(db.Text)  # JSON string for complex answers
    is_correct = db.Column(db.Boolean, default=False)
    points_earned = db.Column(db.Integer, default=0)
    max_points = db.Column(db.Integer, default=1)
    attempt_time = db.Column(db.DateTime, default=datetime.utcnow)
    ai_help_used = db.Column(db.Boolean, default=False)
    
    # Relationships
    question = db.relationship('Question', backref='attempts')
    
    # Ensure unique attempts per session-question
    __table_args__ = (db.UniqueConstraint('session_id', 'question_id'),)


@app.route("/start_exam/<int:exam_id>")
@login_required
def start_exam(exam_id):
    """Start a new exam session"""
    # Check if user has an active session for this exam
    active_session = ExamSession.query.filter_by(
        user_id=current_user.id,
        exam_id=exam_id,
        is_completed=False
    ).first()
    
    if active_session:
        # Resume existing session
        return redirect(url_for('exam', exam_id=exam_id, question_number=active_session.current_question))
    
    # Create new session
    session_id = str(uuid.uuid4())
    exam_session = ExamSession(
        session_id=session_id,
        user_id=current_user.id,
        exam_id=exam_id,
        start_time=datetime.utcnow()
    )
    db.session.add(exam_session)
    db.session.commit()
    
    # Store session ID in Flask session
    session['exam_session_id'] = session_id
    
    return redirect(url_for('exam', exam_id=exam_id, question_number=1))




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


class ExamAttempts(db.Model):
    __tablename__ = 'exam_attempts'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    exam_id = db.Column(db.Integer, db.ForeignKey('exams.id'), nullable=False)
    start_time = db.Column(db.DateTime, default=datetime.utcnow)
    end_time = db.Column(db.DateTime)
    total_score = db.Column(db.Integer, default=0)
    max_possible_score = db.Column(db.Integer, default=0)
    percentage = db.Column(db.Float, default=0.0)
    time_taken_minutes = db.Column(db.Integer)
    is_completed = db.Column(db.Boolean, default=False)
    answers = db.Column(db.Text)  # JSON object storing all answers
    feedback = db.Column(db.Text)  # Overall feedback for the student
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    # Relationships
    responses = db.relationship('QuestionResponse', backref='attempt', lazy=True)

class QuestionResponse(db.Model):
    __tablename__ = 'question_responses'
    
    id = db.Column(db.Integer, primary_key=True)
    attempt_id = db.Column(db.Integer, db.ForeignKey('exam_attempts.id'), nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey('exam_questions.id'), nullable=False)
    student_answer = db.Column(db.Text)
    is_correct = db.Column(db.Boolean, default=False)
    marks_awarded = db.Column(db.Integer, default=0)
    time_spent_seconds = db.Column(db.Integer)
    feedback = db.Column(db.Text)  # Specific feedback for this question
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class StudentProgress(db.Model):
    __tablename__ = 'student_progress'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    topic_id = db.Column(db.String(50), nullable=False)
    topic_title = db.Column(db.String(200), nullable=False)
    score = db.Column(db.Integer, default=0)
    total_questions = db.Column(db.Integer, default=0)
    completed = db.Column(db.Boolean, default=False)
    attempts = db.Column(db.Integer, default=0)
    best_score = db.Column(db.Integer, default=0)
    last_attempt = db.Column(db.DateTime, default=datetime.utcnow)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    __table_args__ = (db.UniqueConstraint('user_id', 'topic_id'),)

class ExamAnalytics(db.Model):
    __tablename__ = 'exam_analytics'
    
    id = db.Column(db.Integer, primary_key=True)
    exam_id = db.Column(db.Integer, db.ForeignKey('exams.id'), nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey('exam_questions.id'), nullable=False)
    total_attempts = db.Column(db.Integer, default=0)
    correct_attempts = db.Column(db.Integer, default=0)
    average_time_seconds = db.Column(db.Float, default=0.0)
    difficulty_rating = db.Column(db.Float, default=0.0)  # Calculated based on success rate
    last_updated = db.Column(db.DateTime, default=datetime.utcnow)
    
    __table_args__ = (db.UniqueConstraint('exam_id', 'question_id'),)


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
    student_class = db.Column(db.String(50), nullable=False)  
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

@app.route("/exam/<int:exam_id>/<int:question_number>", methods=['GET', 'POST'])
@login_required
def exam(exam_id, question_number):
    exam = Exam.query.get_or_404(exam_id)
    questions = Question.query.filter_by(exam_id=exam_id).all()
    
    if question_number > len(questions) or question_number < 1:
        flash('Invalid question number', 'error')
        return redirect(url_for('papers'))
    
    question = questions[question_number - 1]
    
    # Get or create exam session
    exam_session_id = session.get('exam_session_id')
    exam_session = None
    
    if exam_session_id:
        exam_session = ExamSession.query.filter_by(session_id=exam_session_id).first()
    
    if not exam_session:
        # Create new session if none exists
        exam_session_id = str(uuid.uuid4())
        exam_session = ExamSession(
            session_id=exam_session_id,
            user_id=current_user.id,
            exam_id=exam_id,
            start_time=datetime.utcnow()
        )
        db.session.add(exam_session)
        db.session.commit()
        session['exam_session_id'] = exam_session_id
    
    # Check if question already attempted
    existing_attempt = QuestionAttempt.query.filter_by(
        session_id=exam_session_id,
        question_id=question.id
    ).first()
    
    if request.method == 'POST':

        
        try:
            data = request.get_json()
            question_type = question.question_type
            is_correct = False
            points_earned = 0
            user_answer_json = json.dumps(data)
            
            # Evaluate answer based on question type
            if question_type == 'fill_in_the_blank':
                correct_answers = [ans.strip().lower() for ans in question.correct_options.split(',')]
                user_answers = [ans.strip().lower() for ans in data.get('answers', [])]
                if user_answers == correct_answers:
                    is_correct = True
                    points_earned = 1
                    
            elif question_type == 'multiple':
                correct_answers = set(question.correct_options.split(','))
                user_answers = set(data.get('answers', []))
                if user_answers == correct_answers:
                    is_correct = True
                    points_earned = 1
                    
            elif question_type == 'single':
                user_answer = data.get('answer')
                if user_answer == question.correct_option:
                    is_correct = True
                    points_earned = 1
            
  
            
            # Update session score and current question
            exam_session.total_score += points_earned
            exam_session.current_question = min(question_number + 1, len(questions))
            
            # Check if exam is completed
            if question_number == len(questions):
                exam_session.is_completed = True
                exam_session.end_time = datetime.utcnow()
                
                # Create final exam attempt record for compatibility
                final_attempt = ExamAttempt(
                    user_id=current_user.id,
                    exam_id=exam_id,
                    score=exam_session.total_score,
                    total_questions=len(questions),
                    attempt_date=datetime.utcnow()
                )
                db.session.add(final_attempt)
                db.session.commit()
                
                # Clear session
                session.pop('exam_session_id', None)
                session.pop('score', None)
                
                return jsonify({
                    'message': 'Exam completed',
                    'session_id': exam_session_id
                })
            
            db.session.commit()
            return jsonify({
                'message': 'Question processed',
                'next_question': question_number + 1,
                'is_correct': is_correct,
                'points_earned': points_earned
            })
            
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 400
    
    # GET request - check if question is already attempted
    question_attempted = existing_attempt is not None
    user_answer = None
    is_correct = None
    
    if existing_attempt:
        user_answer = json.loads(existing_attempt.user_answer) if existing_attempt.user_answer else None
        is_correct = existing_attempt.is_correct
    
    # Get all attempted questions for navigation
    attempted_questions = db.session.query(QuestionAttempt.question_id).filter_by(
        session_id=exam_session_id
    ).all()
    attempted_question_ids = [q[0] for q in attempted_questions]
    
    return render_template(
        'exam_question.html',
        exam=exam,
        question=question,
        question_number=question_number,
        total_questions=len(questions),
        question_attempted=question_attempted,
        user_answer=user_answer,
        is_correct=is_correct,
        attempted_question_ids=attempted_question_ids
    )

@app.route("/exam_summary/<session_id>")
@login_required
def exam_summary(session_id):
    print("Session ID:", session_id)  # Debugging - print session ID
    """Display comprehensive exam summary"""
    exam_session = ExamSession.query.filter_by(session_id=session_id).first_or_404()
    
    # Security check
    if exam_session.user_id != current_user.id:
        flash('Unauthorized access', 'error')
        return redirect(url_for('papers'))
    
    # Get all question attempts for this session
    attempts = db.session.query(QuestionAttempt, Question).join(
        Question, QuestionAttempt.question_id == Question.id
    ).filter(
        QuestionAttempt.session_id == session_id
    ).order_by(Question.id).all()
    
    # Calculate statistics
    total_questions = Question.query.filter_by(exam_id=exam_session.exam_id).count()
    questions_attempted = len(attempts)
    correct_answers = sum(1 for attempt, _ in attempts if attempt.is_correct)
    ai_help_used = sum(1 for attempt, _ in attempts if attempt.ai_help_used)
    
    # Calculate time taken
    time_taken_minutes = 0
    if exam_session.end_time and exam_session.start_time:
        time_taken = exam_session.end_time - exam_session.start_time
        time_taken_minutes = int(time_taken.total_seconds() / 60)
    
    # Calculate percentage
    percentage = (correct_answers / total_questions * 100) if total_questions > 0 else 0
    
    # Determine grade/feedback
    grade = get_grade(percentage)
    feedback = get_feedback(percentage, ai_help_used, questions_attempted, total_questions)
    
    return render_template(
        'exam_summary.html',
        exam_session=exam_session,
        attempts=attempts,
        total_questions=total_questions,
        questions_attempted=questions_attempted,
        correct_answers=correct_answers,
        percentage=round(percentage, 1),
        time_taken_minutes=time_taken_minutes,
        ai_help_used=ai_help_used,
        grade=grade,
        feedback=feedback
    )

def get_grade(percentage):
    """Convert percentage to grade"""
    if percentage >= 90:
        return 'A*'
    elif percentage >= 80:
        return 'A'
    elif percentage >= 70:
        return 'B'
    elif percentage >= 60:
        return 'C'
    elif percentage >= 50:
        return 'D'
    elif percentage >= 40:
        return 'E'
    else:
        return 'U'

def get_feedback(percentage, ai_help_used, attempted, total):
    """Generate personalized feedback"""
    feedback = []
    
    if percentage >= 90:
        feedback.append("🎉 Excellent work! You have a strong understanding of this topic.")
    elif percentage >= 70:
        feedback.append("👍 Good job! You're on the right track.")
    elif percentage >= 50:
        feedback.append("📚 You're making progress, but there's room for improvement.")
    else:
        feedback.append("💪 Keep studying! Practice makes perfect.")
    
    if attempted < total:
        feedback.append(f"⚠️ You attempted {attempted} out of {total} questions. Try to complete all questions next time.")
    
    if ai_help_used > 0:
        feedback.append(f"🤖 You used AI help on {ai_help_used} question(s). Use this as a learning tool!")
    
    return " ".join(feedback)

# Update the result route to redirect to summary
@app.route("/result/<int:score>/<int:total>")
@login_required  
def result(score, total):
    # If there's an active exam session, redirect to summary
    exam_session_id = session.get('exam_session_id')
    if exam_session_id:
        exam_session = ExamSession.query.filter_by(session_id=exam_session_id).first()
        if exam_session and exam_session.is_completed:
            return redirect(url_for('exam_summary', session_id=exam_session_id))
    
    # Fallback to original result page
    return render_template("result.html", score=score, total=total)

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


@app.route('/t4')
def practise():
    return render_template('p4st31.html')

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
def resultt(score, total):
    return render_template("result.html", score=score, total=total)




@app.route("/exam2/<int:exam_id>/<int:question_number>", methods=['GET', 'POST'])
@login_required
def exam2(exam_id, question_number):
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
    
    # Get or create exam session
    exam_session_id = session.get('exam_session_id')
    exam_session = None
    
    if exam_session_id:
        exam_session = ExamSession.query.filter_by(session_id=exam_session_id).first()
    
    if not exam_session:
        # Create new session if none exists
        exam_session_id = str(uuid.uuid4())
        exam_session = ExamSession(
            session_id=exam_session_id,
            user_id=current_user.id,
            exam_id=exam_id,
            start_time=datetime.utcnow()
        )
        db.session.add(exam_session)
        db.session.commit()
        session['exam_session_id'] = exam_session_id
    
    # Check if question already attempted
    existing_attempt = QuestionAttempt.query.filter_by(
        session_id=exam_session_id,
        question_id=question.id
    ).first()
    
    if existing_attempt:
        return jsonify({'error': 'Question already attempted'}), 400
    
    is_correct = False
    explanation = ""
    correct_answer = None
    points_earned = 0
    user_answer_json = json.dumps(data.get('userAnswers'))
    
    try:
        if question.question_type == 'fill_in_the_blank':
            correct_answers = question.correct_options.split(',')
            user_answers = data.get('userAnswers', {})
            correct_count = 0
            
            for i in range(1, question.blanks + 1):
                user_answer = user_answers.get(f"blank{i}", "").strip().lower()
                if user_answer == correct_answers[i - 1].strip().lower():
                    correct_count += 1
                    
            is_correct = correct_count == question.blanks
            if is_correct:
                points_earned = 1
            correct_answer = correct_answers
            explanation = f"The correct answer{'s are' if len(correct_answers) > 1 else ' is'}: {', '.join(correct_answers)}"
            
        elif question.question_type == 'multiple':
            user_answers = set(data.get('userAnswers', []))
            correct_answers = set(question.correct_options.split(','))
            is_correct = user_answers == correct_answers
            if is_correct:
                points_earned = 1
            correct_answer = list(correct_answers)
            explanation = f"The correct answers are: {', '.join(correct_answer)}"
            
        else:  # single choice
            user_answer = data.get('userAnswers')
            is_correct = user_answer == question.correct_option
            if is_correct:
                points_earned = 1
            correct_answer = question.correct_option
            explanation = f"The correct answer is: {question.correct_option}"
        
        # Record the attempt
        attempt = QuestionAttempt(
            session_id=exam_session_id,
            question_id=question.id,
            user_answer=user_answer_json,
            is_correct=is_correct,
            points_earned=points_earned,
            attempt_time=datetime.utcnow(),
            ai_help_used=session.get(f'ai_help_used_{question.id}', False)
        )
        db.session.add(attempt)
        
        # Update session score
        exam_session.total_score += points_earned
        exam_session.current_question = max(exam_session.current_question or 0, question_number)
        
        db.session.commit()
        
        return jsonify({
            'isCorrect': is_correct,
            'correctAnswer': correct_answer,
            'explanation': explanation,
            'pointsEarned': points_earned
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route("/user_home")
@login_required
def user_home():
    # Get duedate from query params, default to 7 days from today
    duedate_str = request.args.get('duedate')
    today = datetime.now().date()
    if duedate_str:
        try:
            duedate = datetime.strptime(duedate_str, "%Y-%m-%d").date()
        except ValueError:
            duedate = today + timedelta(days=70)
    else:
        duedate = today + timedelta(days=70)
    
    print(duedate)

    # Filter To-Do items by date <= duedate
    todos = ToDo.query.filter(
        ToDo.user_id == current_user.id,
        ToDo.date <= duedate
    ).order_by(ToDo.date.asc()).all()

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
    duedate_str = request.args.get('duedate')
    today = datetime.now().date()
    if duedate_str:
        try:
            duedate = datetime.strptime(duedate_str, "%Y-%m-%d").date()
        except ValueError:
            duedate = today + timedelta(days=70)
    else:
        duedate = today + timedelta(days=70)
    
    print(duedate)

    # Filter To-Do items by date <= duedate
    todos = ToDo.query.filter(
        ToDo.user_id == current_user.id,
        ToDo.date <= duedate
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



import requests
import json

import requests
import json

import requests
import json

@app.route('/ask-ai', methods=['POST'])
def ask_groq():
    try:
        data = request.json
        question = data['messages'][0]['content']
        
        # Add better error handling and logging
        print(f"Received question: {question}")  # Debug log
        
        # Structure the prompt
        prompt = f"""Please help explain this exam question and provide guidance with respect to IGCSE syllabus. 
        Question: {question}
        Please provide:
        1. A clear explanation of the question
        2. Key concepts to consider
        3. Approach to solving it 
        """
        
        try:
            # Groq API configuration
            groq_api_key = "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"
            groq_url = "https://api.groq.com/openai/v1/chat/completions"
            
            # Test with minimal payload first
            headers = {
                "Authorization": f"Bearer {groq_api_key}",
                "Content-Type": "application/json"
            }
            
            # Simplified payload to test
            payload = {
                "model": "llama-3.3-70b-versatile",  # Using llama-3.3-70b-versatile
                "messages": [
                    {
                        "role": "user",
                        "content": "Hello, can you help me?"  # Simple test message
                    }
                ]
            }
            
            print(f"Testing with simple payload: {json.dumps(payload, indent=2)}")
            
            # Make API request to Groq
            response = requests.post(groq_url, headers=headers, json=payload, timeout=30)
            
            print(f"Response status code: {response.status_code}")
            print(f"Response headers: {dict(response.headers)}")
            print(f"Response text: {response.text}")
            
            if response.status_code == 401:
                return jsonify({
                    'error': "Authentication failed - please check your API key"
                }), 401
            elif response.status_code == 429:
                return jsonify({
                    'error': "Rate limit exceeded - please try again later"
                }), 429
            elif response.status_code != 200:
                return jsonify({
                    'error': f"API returned status {response.status_code}: {response.text}"
                }), response.status_code
            
            response_data = response.json()
            
            # If the test works, now try with the actual prompt
            if response.status_code == 200:
                payload["messages"][0]["content"] = prompt
                payload["max_tokens"] = 1024
                payload["temperature"] = 0.7
                
                print("Test successful, now sending actual prompt...")
                response = requests.post(groq_url, headers=headers, json=payload, timeout=30)
                
                if response.status_code == 200:
                    response_data = response.json()
                    ai_response = response_data['choices'][0]['message']['content']
                    
                    return jsonify({
                        'response': ai_response
                    })
                else:
                    print(f"Actual request failed: {response.status_code} - {response.text}")
                    return jsonify({
                        'error': f"Request failed: {response.status_code} - {response.text}"
                    }), response.status_code
            
        except requests.exceptions.Timeout:
            print("Request timeout")
            return jsonify({
                'error': "Request timeout - please try again"
            }), 408
            
        except requests.exceptions.ConnectionError:
            print("Connection error")
            return jsonify({
                'error': "Connection error - please check your internet connection"
            }), 503
            
        except requests.exceptions.RequestException as api_error:
            print(f"Groq API request error: {str(api_error)}")
            return jsonify({
                'error': f"Groq API request error: {str(api_error)}"
            }), 500
            
        except KeyError as key_error:
            print(f"Groq API response format error: {str(key_error)}")
            return jsonify({
                'error': f"Groq API response format error: {str(key_error)}"
            }), 500
            
        except Exception as api_error:
            print(f"Groq API error: {str(api_error)}")
            return jsonify({
                'error': f"Groq API error: {str(api_error)}"
            }), 500
    
    except Exception as e:
        print(f"Server error: {str(e)}")
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


@app.route('/complete-exam', methods=['POST'])
def complete_exam():
    """Complete the exam and save final results"""
    try:
        if 'user_id' not in session:
            return jsonify({'error': 'Not authenticated'}), 401
        
        data = request.get_json()
        exam_id = data.get('examId')
        total_score = data.get('totalScore')
        max_score = data.get('maxScore')
        percentage = data.get('percentage')
        time_taken = data.get('timeTaken')
        
        user_id = session['user_id']
        
        # Get the exam attempt
        attempt = ExamAttempt.query.filter_by(
            user_id=user_id,
            exam_id=exam_id,
            is_completed=False
        ).first()
        
        if not attempt:
            return jsonify({'error': 'No active exam attempt found'}), 404
        
        # Complete the attempt
        attempt.end_time = datetime.utcnow()
        attempt.total_score = total_score
        attempt.percentage = percentage
        attempt.time_taken_minutes = time_taken
        attempt.is_completed = True
        
        # Update student progress
        from app.models import StudentProgress
        progress = StudentProgress.query.filter_by(
            user_id=user_id,
            topic_id=f"exam_{exam_id}"
        ).first()
        
        if progress:
            progress.score = max(progress.score, total_score)
            progress.best_score = max(progress.best_score, total_score)
            progress.attempts += 1
            progress.completed = percentage >= 50  # Pass mark
        else:
            progress = StudentProgress(
                user_id=user_id,
                topic_id=f"exam_{exam_id}",
                topic_title=f"Exam: {attempt.exam.title}",
                score=total_score,
                total_questions=len(attempt.exam.questions),
                completed=percentage >= 50,
                attempts=1,
                best_score=total_score
            )
            db.session.add(progress)
        
        db.session.commit()
        
        return jsonify({'success': True})
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/exam-results/<int:exam_id>')
def exam_results(exam_id):
    """Display exam results"""
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    
    user_id = session['user_id']
    
    # Get the most recent completed attempt
    attempt = ExamAttempt.query.filter_by(
        user_id=user_id,
        exam_id=exam_id,
        is_completed=True
    ).order_by(ExamAttempt.end_time.desc()).first()
    
    if not attempt:
        return redirect(url_for('exam.start_exam', exam_id=exam_id))
    
    return render_template('exam_results.html', attempt=attempt)


if __name__ == '__main__':
    with app.app_context():
        
        db.create_all()  # Creates database tables if they don't exist

    context = (r'/home/bb/exam/ssl/bb.pem', r'/home/bb/exam/ssl/bb.key')
    app.run(host='0.0.0.0', port=443, debug=True, ssl_context=context)
    
    #app.run(host='0.0.0.0', port=443, debug=True)
