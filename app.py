from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Configure SQLite Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Admin credentials
admin_credentials = {'admin': 'admin123'}

# Define the User Model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50))
    email = db.Column(db.String(120))

# Create the database
with app.app_context():
    db.create_all()

@app.route('/')
def home():
    return render_template('login_type.html')

@app.route('/user-login', methods=['GET', 'POST'])
def user_login():
    if request.method == 'POST':
        username = request.form['username']
        user = User.query.filter((User.username == username) | (User.email == username)).first()
        if user:
            return "Login Successful!"
        return redirect('/register')
    return render_template('user_login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        new_user = User(username=username, email=email)
        db.session.add(new_user)
        db.session.commit()
        return redirect('/')
    return render_template('registration.html')

@app.route('/admin-login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        admin_id = request.form['admin_id']
        admin_password = request.form['admin_password']
        if admin_credentials.get(admin_id) == admin_password:
            all_users = User.query.all()
            return render_template('admin_dashboard.html', users=all_users)
    return render_template('admin_login.html')

if __name__ == '__main__':
    app.run(debug=True)
