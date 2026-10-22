from flask import Flask, request, render_template, redirect, flash, url_for
from models import db, Category, Dish, User, Order
from flask_login import LoginManager, login_user, logout_user, login_required, current_user

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///trattoria.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db.init_app(app)
with app.app_context():
    db.create_all()

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"



@app.route('/')
def index():
    return redirect(url_for('register'))

@app.route('/menu')
@app.route('/menu/<slug>')
def menu(slug=None):
    categories = Category.query.order_by(Category.name).all()
    current = None
    query = Dish.query.filter_by(is_avaliable=True)
    if slug:
        current = Category.query.filter_by(slug=slug).first_or_404()
        query = query.filter_by(category_id=current.id)

    q = request.args.get('q', "").strip()

    if q:
        query = query.filter(Dish.name.ilike(f"%{q}%"))

    dishes = query.order_by(Dish.category_id, Dish.name).all()
    return render_template('menu.html', categories=categories, current=current, dishes=dishes, q=q)

@app.route('/dish/<int:dish_id>')
def dish(dish_id):
    dish = db.get_or_404(Dish, dish_id)
    return render_template('dish.html', dish=dish)

@app.errorhandler(404)
def not_found(error):
    return render_template('error.html'), 404

@login_manager.user_loader
def load_user(userId):
    return db.session.get(User, int(userId))

@app.route('/register', methods=['GET', 'POST'])
def register():
    print(6)
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


@app.route('/order/<int:dish_id>', methods=['POST'])
def order(dish_id):
    dish = db.get_or_404(Dish, dish_id)

    new_order = Order(
        dish_id=dish.id,
    )
    db.session.add(new_order)
    db.session.commit()

    return redirect(url_for('orders'))


@app.route('/orders')
def orders():
    orders = Order.query.all()
    return render_template('orders.html', orders=orders)


if __name__ == '__main__':
    app.run(debug=True)
