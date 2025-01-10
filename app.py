from flask import Flask, render_template, request, redirect, url_for, flash, Response, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import io
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///expense_data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'your_secret_key'

# Initialize SQLAlchemy
db = SQLAlchemy(app)

# Flask-Login configuration
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"  # Redirect to login if not authenticated

# Models
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    expenses = db.relationship('Expense', backref='user', lazy=True)

class Expense(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    category = db.Column(db.String(50), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(200))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

# Flask-Login user loader
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Routes
@app.route('/home')
def home():
    return render_template('home.html')  # Create a public homepage

@app.route('/')
@login_required
def index():
    expenses = Expense.query.filter_by(user_id=current_user.id).all()
    return render_template('index.html', expenses=expenses)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256', salt_length=8)

        if User.query.filter_by(username=username).first():
            flash("Username already exists")
            return redirect(url_for('register'))

        new_user = User(username=username, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        flash("Registration successful! Please log in.")
        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('index'))
        else:
            flash("Invalid username or password")
            return redirect(url_for('login'))

    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("You have been logged out.")
    return redirect(url_for('login'))

@app.route('/add', methods=['GET', 'POST'])
@login_required
def add_expense():
    if request.method == 'POST':
        date = datetime.strptime(request.form['date'], '%Y-%m-%d')
        category = request.form['category']
        amount = float(request.form['amount'])
        description = request.form['description']

        new_expense = Expense(date=date, category=category, amount=amount, description=description, user_id=current_user.id)
        db.session.add(new_expense)
        db.session.commit()
        return redirect(url_for('index'))

    return render_template('add_expense.html')

@app.route('/report', methods=['GET'])
@login_required
def report():
    expenses = Expense.query.filter_by(user_id=current_user.id).all()

    if not expenses:
        return render_template('report.html', summary=[], total_expense=0)

    data = [
        {"Date": expense.date, "Category": expense.category, "Amount": expense.amount}
        for expense in expenses
    ]
    df = pd.DataFrame(data)
    summary = df.groupby("Category")["Amount"].sum().reset_index()
    total_expense = df["Amount"].sum()

    return render_template('report.html', summary=summary.to_dict(orient='records'), total_expense=total_expense)

@app.route('/report/plot.png')
@login_required
def plot_png():
    expenses = Expense.query.filter_by(user_id=current_user.id).all()

    data = [
        {"Date": expense.date, "Category": expense.category, "Amount": expense.amount}
        for expense in expenses
    ]
    df = pd.DataFrame(data)

    plt.figure(figsize=(6, 6))
    category_summary = df.groupby("Category")["Amount"].sum()
    category_summary.plot.pie(autopct='%1.1f%%', startangle=140, colors=plt.cm.Paired.colors)
    plt.title("Expenses by Category")
    plt.ylabel("")

    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    return Response(img.getvalue(), mimetype='image/png')

# Run the app
if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Ensure database tables are created
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
