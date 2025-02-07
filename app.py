from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

# यूज़र मॉडल (लॉगिन के लिए)
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(20), nullable=False)  # thana, officer, admin

# होमपेज (लॉगिन पेज)
@app.route('/')
def login():
    return render_template('login.html')

# लॉगिन वेरिफिकेशन
@app.route('/authenticate', methods=['POST'])
def authenticate():
    username = request.form.get('username')
    password = request.form.get('password')
    role = request.form.get('role')

    user = User.query.filter_by(username=username, role=role).first()
    
    if user and check_password_hash(user.password, password):
        session['user_role'] = role
        session['username'] = username

        if role == 'thana':
            return redirect(url_for('thana_dashboard'))
        elif role == 'officer':
            return redirect(url_for('officer_dashboard'))
        elif role == 'admin':
            return redirect(url_for('admin_dashboard'))
    else:
        return render_template('login.html', error="गलत यूज़रनेम या पासवर्ड")

# थाना डैशबोर्ड
@app.route('/thana')
def thana_dashboard():
    if session.get('user_role') != 'thana':
        return redirect('/')
    return render_template('thana_dashboard.html')

# अधिकारी डैशबोर्ड
@app.route('/officer')
def officer_dashboard():
    if session.get('user_role') != 'officer':
        return redirect('/')
    return render_template('officer_dashboard.html')

# एडमिन डैशबोर्ड
@app.route('/admin')
def admin_dashboard():
    if session.get('user_role') != 'admin':
        return redirect('/')
    return render_template('admin_dashboard.html')

# लॉगआउट
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
