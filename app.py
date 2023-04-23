from flask import Flask, render_template, request

# from flask_mysqldb import MySQL
import os
from flask import Flask, render_template, request, url_for, redirect, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask import jsonify, session
import json
from flask_bootstrap import Bootstrap5
from flask_wtf import FlaskForm
from wtforms import StringField, DecimalField, IntegerField, BooleanField, SubmitField
from wtforms.validators import DataRequired


app = Flask(__name__)
bootstrap = Bootstrap5(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:password@localhost:3306/diningschema'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'super secret key'
app.config['SESSION_TYPE'] = 'filesystem'

db = SQLAlchemy(app)


class Customer(db.Model):
    __tablename__ = 'customer'
    cust_ID = Column(Integer, primary_key=True)
    name = Column(String(50))
    email = Column(String(50))
    meal_plan_id = Column(Integer, ForeignKey('mealplans.plan_ID'))
    mobile = Column(Integer)
    mealplans = relationship("MealPlans")


class Dining(db.Model):
    __tablename__ = 'dining'
    dining_ID = Column(Integer, primary_key=True)
    name = Column(String(50))
    location = Column(String(50))
    franchise = Column(String(50))
    working_hours = Column(String(50))


class Inventory(db.Model):
    __tablename__ = 'inventory'
    item_ID = Column(Integer, primary_key=True)
    item_name = Column(String(50))
    quantity = Column(Integer)
    dining_id = Column(Integer, ForeignKey('dining.dining_ID'))
    dining = relationship("Dining")


class GreenchoiceUsers(db.Model):
    __tablename__ = 'greenchoiceusers'
    greenchoice_ID = Column(Integer, primary_key=True)
    cust_id = Column(Integer, ForeignKey('customer.cust_ID'))
    customer = relationship("Customer")


class Orders(db.Model):
    __tablename__ = 'orders'
    order_ID = Column(Integer, primary_key=True)
    order_location = Column(String(50))
    order_total = Column(Integer)
    dining_id = Column(Integer, ForeignKey('dining.dining_ID'))
    dining = relationship("Dining")
    cust_id = Column(Integer, ForeignKey('customer.cust_ID'))
    customer = relationship("Customer")


class DiningCustomer(db.Model):
    __tablename__ = 'diningcustomer'
    cust_id = Column(Integer, ForeignKey('customer.cust_ID'), primary_key=True)
    dining_id = Column(Integer, ForeignKey(
        'dining.dining_ID'), primary_key=True)
    customer = relationship("Customer")
    dining = relationship("Dining")


class Employee(db.Model):
    __tablename__ = 'employee'
    emp_ID = Column(Integer, primary_key=True)
    emp_name = Column(String(50))
    emp_address = Column(String(50))
    emp_email = Column(String(50))
    emp_mobile = Column(Integer)
    emp_password = Column(String(50))
    dining_id = Column(Integer, ForeignKey('dining.dining_ID'))
    dining = relationship("Dining")


class Expenses(db.Model):
    __tablename__ = 'expenses'
    expense_ID = Column(Integer, primary_key=True)
    exp_description = Column(String(50))
    exp_amount = Column(Integer)
    dining_id = Column(Integer, ForeignKey('dining.dining_ID'))
    dining = relationship("Dining")


class MealPlans(db.Model):
    __tablename__ = 'mealplans'
    plan_ID = Column(Integer, primary_key=True)
    price_limit = Column(Integer)
    plan_description = Column(String(50))


class Menu(db.Model):
    __tablename__ = 'menu'
    menu_ID = Column(Integer, primary_key=True)
    item_name = Column(String(50))
    item_price = Column(Integer)
    gluten_free = Column(Integer)
    alergen_free = Column(Integer)
    vegan = Column(Integer)
    dining_id = Column(Integer, ForeignKey('dining.dining_ID'))
    dining = relationship("Dining")


class OrderItem(db.Model):
    __tablename__ = 'orderitem'
    order_id = Column(Integer, ForeignKey('orders.order_ID'), primary_key=True)
    menu_id = Column(Integer, ForeignKey('menu.menu_ID'), primary_key=True)
    menu = relationship("Menu")
    orders = relationship("Orders")


class Assets(db.Model):
    __tablename__ = 'Assets'
    asset_ID = Column(Integer, primary_key=True)
    description = Column(String(50))
    value = Column(Integer)
    dining_id = Column(Integer, ForeignKey('dining.dining_ID'))


class Payment(db.Model):
    __tablename__ = 'Payment'
    payment_ID = Column(Integer, primary_key=True)
    payment_type = Column(String(50))
    payment_amount = Column(Integer)
    order_id = Column(Integer, ForeignKey('orders.order_ID'))
    orders = relationship('Orders')


class Reviews(db.Model):
    __tablename__ = 'reviews'
    review_ID = Column(Integer, primary_key=True)
    review_description = Column(String(50))
    order_id = Column(Integer, ForeignKey('orders.order_ID'))
    orders = relationship('Orders')


@app.route("/",  methods=['GET', 'POST'])
def home():
    if session.__contains__("loggedIn") == False:
        session['emp_id'] = ''
        session['loggedIn'] = False

    food_court = {
        1: "Food Court",
        2: "Eagle Landing",
        3: "Bruce Dining",
        4: "Chic-Fil-A",
        5: "Burger King",
        6: "Fuzzys",
        7: "Clark Bakery",
        8: "Mean Green"
    }
    menu_data = Menu.query.all()
    return render_template('index.html', menu_data=menu_data, fc_dict=food_court)


@app.route('/saveDining', methods=['GET', 'POST'])
def saveDining():
    name = request.form['name']
    location = request.form['location']
    franchise = request.form['franchise']
    working_hours = request.form['working_hours']
    new_dining = Dining(name=name, location=location,
                        franchise=franchise, working_hours=working_hours)
    db.session.add(new_dining)
    db.session.commit()
    food_court = {
        1: "Food Court",
        2: "Eagle Landing",
        3: "Bruce Dining",
        4: "Chic-Fil-A",
        5: "Burger King",
        6: "Fuzzys",
        7: "Clark Bakery",
        8: "Mean Green"
    }
    menu_data = Menu.query.all()
    return render_template('index.html', menu_data=menu_data, fc_dict=food_court)


@app.route('/addDining', methods=['GET', 'POST'])
def addDining():
    return render_template('addDining.html')


@app.route('/addMealPlan', methods=['GET', 'POST'])
def addMealPlan():
    return render_template('addMealPlan.html')


@app.route('/saveMealPlan', methods=['POST'])
def saveMealPlan():
    price_limit = request.form['price_limit']
    plan_description = request.form['plan_description']

    new_mealplan = MealPlans(price_limit=price_limit,
                             plan_description=plan_description)
    db.session.add(new_mealplan)
    db.session.commit()

    food_court = {
        1: "Food Court",
        2: "Eagle Landing",
        3: "Bruce Dining",
        4: "Chic-Fil-A",
        5: "Burger King",
        6: "Fuzzys",
        7: "Clark Bakery",
        8: "Mean Green"
    }
    menu_data = Menu.query.all()
    return render_template('index.html', menu_data=menu_data, fc_dict=food_court)


@app.route('/addExpense', methods=['GET', 'POST'])
def addExpense():
    dining_data = Dining.query.all()
    return render_template('addExpense.html', dining_data=dining_data)


@app.route('/saveExpense', methods=['POST'])
def saveExpense():
    exp_description = request.form['exp_description']
    exp_amount = request.form['exp_amount']
    dining_id = request.form['dining_list']
    new_expense = Expenses(exp_description=exp_description,
                           exp_amount=exp_amount, dining_id=dining_id)
    db.session.add(new_expense)
    db.session.commit()
    food_court = {
        1: "Food Court",
        2: "Eagle Landing",
        3: "Bruce Dining",
        4: "Chic-Fil-A",
        5: "Burger King",
        6: "Fuzzys",
        7: "Clark Bakery",
        8: "Mean Green"
    }
    menu_data = Menu.query.all()
    return render_template('index.html', menu_data=menu_data, fc_dict=food_court)


@app.route('/addMenuItem', methods=['GET', 'POST'])
def addMenuItem():
    dining_data = Dining.query.all()
    return render_template('addMenuItem.html', dining_data=dining_data)


@app.route('/saveMenuItem', methods=['POST'])
def saveMenuItem():
    item_name = request.form['item_name']
    item_price = request.form['item_price']
    gluten_free = 0
    if 'gluten_free' in request.form:
        gluten_free = 1

    alergen_free = 0
    if 'alergen_free' in request.form:
        alergen_free = 1

    vegan = 0
    if 'vegan' in request.form:
        vegan = 1

    dining_id = request.form['dining_list']

    new_item = Menu(item_name=item_name, item_price=item_price,
                    gluten_free=gluten_free, alergen_free=alergen_free, vegan=vegan, dining_id=dining_id)

    db.session.add(new_item)
    db.session.commit()
    food_court = {
        1: "Food Court",
        2: "Eagle Landing",
        3: "Bruce Dining",
        4: "Chic-Fil-A",
        5: "Burger King",
        6: "Fuzzys",
        7: "Clark Bakery",
        8: "Mean Green"
    }
    menu_data = Menu.query.all()
    return render_template('index.html', menu_data=menu_data, fc_dict=food_court)


@app.route('/addInventory', methods=['GET', 'POST'])
def addInventory():
    dining_data = Dining.query.all()
    return render_template('addInventory.html', dining_data=dining_data)


@app.route('/saveInventory', methods=['POST'])
def saveInventory():
    item_name = request.form['item_name']
    quantity = request.form['quantity']
    dining_id = request.form['dining_list']
    new_inventory = Inventory(
        item_name=item_name, quantity=quantity, dining_id=dining_id)
    db.session.add(new_inventory)
    db.session.commit()
    food_court = {
        1: "Food Court",
        2: "Eagle Landing",
        3: "Bruce Dining",
        4: "Chic-Fil-A",
        5: "Burger King",
        6: "Fuzzys",
        7: "Clark Bakery",
        8: "Mean Green"
    }
    menu_data = Menu.query.all()
    return render_template('index.html', menu_data=menu_data, fc_dict=food_court)


@app.route('/addEmployee', methods=['GET', 'POST'])
def addEmployee():
    dining_data = Dining.query.all()
    return render_template('AddEmployee.html', dining_data=dining_data)


@app.route('/saveEmployee', methods=['POST'])
def save_employee():
    emp_name = request.form['emp_name']
    emp_address = request.form['emp_address']
    emp_email = request.form['emp_email']
    emp_mobile = request.form['emp_mobile']
    emp_password = request.form['emp_password']
    dining_id = request.form['dining_list']
    new_employee = Employee(emp_name=emp_name, emp_address=emp_address, emp_email=emp_email,
                            emp_mobile=emp_mobile, emp_password=emp_password, dining_id=dining_id)
    db.session.add(new_employee)
    db.session.commit()
    food_court = {
        1: "Food Court",
        2: "Eagle Landing",
        3: "Bruce Dining",
        4: "Chic-Fil-A",
        5: "Burger King",
        6: "Fuzzys",
        7: "Clark Bakery",
        8: "Mean Green"
    }
    menu_data = Menu.query.all()
    return render_template('index.html', menu_data=menu_data, fc_dict=food_court)


@app.route('/addAsset', methods=['GET', 'POST'])
def addAsset():
    dining_data = Dining.query.all()
    return render_template('addAsset.html', dining_data=dining_data)


@app.route('/saveAsset', methods=['POST'])
def saveAsset():
    description = request.form['description']
    value = request.form['value']
    dining_id = request.form['dining_list']
    new_asset = Assets(description=description,
                       value=value, dining_id=dining_id)
    db.session.add(new_asset)
    db.session.commit()

    food_court = {
        1: "Food Court",
        2: "Eagle Landing",
        3: "Bruce Dining",
        4: "Chic-Fil-A",
        5: "Burger King",
        6: "Fuzzys",
        7: "Clark Bakery",
        8: "Mean Green"
    }
    menu_data = Menu.query.all()
    return render_template('index.html', menu_data=menu_data, fc_dict=food_court)


@app.route('/addOrders', methods=['POST'])
def add_order():
    order_location = request.json['order_location']
    order_total = request.json['order_total']
    dining_id = request.json['dining_id']
    cust_id = request.json['cust_id']
    new_order = Orders(order_location=order_location,
                       order_total=order_total, dining_id=dining_id, cust_id=cust_id)
    db.session.add(new_order)
    db.session.commit()
    return 'Successfully added'


@app.route('/addCustomer', methods=['POST'])
def add_customer():
    name = request.json['name']
    email = request.json['email']
    meal_plan_id = request.json['meal_plan_id']
    mobile = request.json['mobile']
    new_customer = Customer(name=name, email=email,
                            meal_plan_id=meal_plan_id, mobile=mobile)
    db.session.add(new_customer)
    db.session.commit()
    return 'Successfully added'


@app.route('/addPayment', methods=['POST'])
def add_payment():
    if request.method == 'POST':
        payment_type = request.json['payment_type']
        payment_amount = request.json['payment_amount']
        order_id = request.json['order_id']

        payment = Payment(payment_type=payment_type,
                          payment_amount=payment_amount, order_id=order_id)
        db.session.add(payment)
        db.session.commit()

        return 'Successfully added'
    return 'Failed to add'


@app.route('/addReview', methods=['GET', 'POST'])
def addReview():
    return render_template('addReview.html')


@app.route('/saveReview', methods=['POST'])
def saveReview():
    review_description = request.form['review_description']
    order_id = request.form['order_id']
    new_review = Reviews(
        review_description=review_description, order_id=order_id)
    db.session.add(new_review)
    db.session.commit()
    food_court = {
        1: "Food Court",
        2: "Eagle Landing",
        3: "Bruce Dining",
        4: "Chic-Fil-A",
        5: "Burger King",
        6: "Fuzzys",
        7: "Clark Bakery",
        8: "Mean Green"
    }
    menu_data = Menu.query.all()
    return render_template('index.html', menu_data=menu_data, fc_dict=food_court)


@app.route('/addGreenchoiceuser', methods=['POST'])
def add_greenchoice_user():
    cust_id = request.json['cust_id']
    new_greenchoice_user = GreenchoiceUsers(cust_id=cust_id)
    db.session.add(new_greenchoice_user)
    db.session.commit()
    return 'Added Successfully'


@app.route('/addDiningcustomer', methods=['POST'])
def add_dining_customer():
    cust_id = request.json['cust_id']
    dining_id = request.json['dining_id']
    new_dining_customer = DiningCustomer(cust_id=cust_id, dining_id=dining_id)
    db.session.add(new_dining_customer)
    db.session.commit()
    return 'Successfully added'


@app.route('/addOrderitem', methods=['POST'])
def add_orderitem():
    if request.method == 'POST':
        order_id = request.json['order_id']
        menu_id = request.json['menu_id']

        orderitem = OrderItem(order_id=order_id, menu_id=menu_id)
        db.session.add(orderitem)
        db.session.commit()

        return 'Successfully added'
    return 'Failed to add'


# Simulating an order

@app.route('/orderSim')
def orderSim():
    cust_data = Customer.query.all()
    dining_data = Dining.query.all()
    return render_template('OrderSim.html', cust_data=cust_data, dining_data=dining_data)


@app.route('/ContinueOrder',  methods=['POST'])
def ContinueOrder():

    total = 0
    order_limit = 0
    cust_id_ = request.form['cust_list']
    dining_id_ = request.form['dining_list']
# get customer and

    customer_details = Customer.query.get(cust_id_)

#   - also check if greenchoince user add $2
    is_greenuser = db.session.query(GreenchoiceUsers.greenchoice_ID).filter_by(
        cust_id=cust_id_).first() is not None
    if (is_greenuser):
        total += 2

#   - check meal plan and limit under plan total
    if (customer_details.meal_plan_id != None):
        order_limit = MealPlans.query.get(
            customer_details.meal_plan_id).price_limit

    # get dining location
    # get menu
    menu_details = db.session.query(Menu).filter_by(dining_id=1).all()

    return render_template('FinishOrder.html', menu_details=menu_details,
                           order_limit=order_limit, total=total, cust_id_=cust_id_,
                           dining_id_=dining_id_, is_greenuser=is_greenuser)

# select items and calculate order total and list of menu items
# insert into orders, order item, payment, dining customer


@app.route('/FinishOrder', methods=['POST'])
def FinishOrder():

    food_court = {
        1: "Food Court",
        2: "Eagle Landing",
        3: "Bruce Dining",
        4: "Chic-Fil-A",
        5: "Burger King",
        6: "Fuzzys",
        7: "Clark Bakery",
        8: "Mean Green"
    }

    chkbox_values = request.form.getlist('chkbox')
    order_limit = int(request.form.get('order_limit'))
    total = int(request.form.get('total'))
    cust_id_ = int(request.form.get('cust_id_'))
    dining_id_ = int(request.form.get('dining_id_'))
    order_location = food_court.get(dining_id_)
    payment_value = request.form.get('payment')

    for m_id in chkbox_values:
        total += int(Menu.query.get(m_id).item_price)

    if (total < order_limit):
        total = 0
    elif (order_limit > 0):
        total = 0 if total < order_limit else total - order_limit

# inserting values
    # orders
    new_order = Orders(order_location=order_location,
                       order_total=total, dining_id=dining_id_, cust_id=cust_id_)
    db.session.add(new_order)
    db.session.commit()

    # order item
    for m_id in chkbox_values:
        order_id = new_order.order_ID
        menu_id = m_id
        orderitem = OrderItem(order_id=order_id, menu_id=menu_id)
        db.session.add(orderitem)
        db.session.commit()

    # payment
    payment_type = payment_value
    payment_amount = total
    order_id = new_order.order_ID
    payment = Payment(payment_type=payment_type,
                      payment_amount=payment_amount, order_id=order_id)
    db.session.add(payment)
    db.session.commit()

    # dining customer
    exists = db.session.query(DiningCustomer.cust_id).filter_by(
        cust_id=cust_id_, dining_id=dining_id_).first() is not None
    if (not exists):
        new_dining_customer = DiningCustomer(
            cust_id=cust_id_, dining_id=dining_id_)
        db.session.add(new_dining_customer)
        db.session.commit()
    print(exists)
    return 'Successfully added'


# employee login and actions
@app.route('/login', methods=['GET', 'POST'])
def login():
    if session['loggedIn'] == True:
        return 'Already logged in'
    return render_template('login.html')


@app.route('/validate', methods=['POST'])
def validate():
    emp_ID = request.form['emp_ID']
    emp_password = request.form['emp_password']
    employee = Employee.query.filter_by(
        emp_email=emp_ID, emp_password=emp_password).first()

    if employee is not None:
        session['emp_id'] = employee.emp_ID
        session['loggedIn'] = True
        return redirect(url_for('home'))
    else:
        return redirect(url_for('login'))


@app.route('/signout', methods=['GET', 'POST'])
def signout():
    session['loggedIn'] = False
    session['emp_id'] = ''
    return render_template('login.html')


# ------------------------------------------------------------------

# class MenuForm(FlaskForm):
#     item_name = StringField('Item Name', validators=[DataRequired()])
#     item_price = DecimalField('Item Price', validators=[DataRequired()])
#     dining_id = IntegerField('Location', validators=[DataRequired()])
#     gluten_free = BooleanField('Gluten Free')
#     alergen_free = BooleanField('Alergen Free')
#     vegan = BooleanField('Vegan')
#     submit = SubmitField('Submit')


# @app.route('/add_menu', methods=['GET', 'POST'])
# def add_menu():
#     form = MenuForm()
#     if form.validate_on_submit():
#         # Save the new menu item to the database
#         new_menu_item = Menu(
#             item_name=form.item_name.data,
#             item_price=form.item_price.data,
#             dining_id=form.dining_location.data.id,
#             gluten_free=form.gluten_free.data,
#             alergen_free=form.alergen_free.data,
#             vegan=form.vegan.data
#         )
#         db.session.add(new_menu_item)
#         db.session.commit()

#         flash('New menu item added!')
#         return redirect(url_for('menu'))

#     return render_template('add_menu.html', form=form)


# @app.route('/update_menu/<int:menu_id>', methods=['GET', 'POST'])
# def update_menu(menu_id):
#     menu_item = Menu.query.get_or_404(menu_id)
#     form = MenuForm(obj=menu_item)
#     if form.validate_on_submit():
#         # Update the existing menu item in the database
#         menu_item.item_name = form.item_name.data
#         menu_item.item_price = form.item_price.data
#         menu_item.dining_id = form.dining_location.data.id
#         menu_item.gluten_free = form.gluten_free.data
#         menu_item.alergen_free = form.alergen_free.data
#         menu_item.vegan = form.vegan.data
#         db.session.commit()

#         flash('Menu item updated!')
#         return redirect(url_for('menu'))

#     return render_template('update_menu.html', form=form, menu_item=menu_item)


if __name__ == '__main__':

    session.init_app(app)

    app.debug = True
    app.run()
