from flask import Flask, request, render_template, redirect, flash, url_for
from models import db, Category, Dish, User
from flask_login import LoginManager, login_user, logout_user, login_required, current_user


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///trattoria.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
with app.app_context():
    db.create_all()


@app.errorhandler(404)
def not_found(error):
    return render_template('error.html'), 404

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view("login")

@login_manager.user_loader
def load_user(userId):
    return db.session.get(User, int(userId))

@app.route('/register', methods=['GET', 'POST'])
def registration():
    if request.method == 'POST':
        username = request.form['username'].strip()
        email = request.form['email'].strip()
        password = request.form['password'].strip()

        exist_user = db.session.scalar(db.select(User).where(User.username == username))

        if exist_user:
            flash("This user existing")
            return redirect(url_for('register'))
        new_user = User(username = username,
                        email = email)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()
        flash("Registration successful")
        return redirect(url_for('login'))
    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email'].strip().lower()
        password = request.form['password'].strip()

        user = db.session.scalar(
            db.select(User).where(User.email == email)
        )
        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('menu'))


    return render_template('login.html')




if __name__ == '__main__':
    app.run(debug=True)
