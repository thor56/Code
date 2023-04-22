from flask import Flask, render_template, request

# from flask_mysqldb import MySQL
import os
from flask import Flask, render_template, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask import jsonify
import json


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:password@localhost:3306/diningschema'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

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


@app.route("/")
def hello_world():
    # meal_plan = MealPlans(price_limit=200,
    #                       plan_description='Standard')
    # db.session.add(meal_plan)
    # db.session.commit()

    new_customer = Customer(name=name, email=email,
                            meal_plan_id=1, mobile=mobile)
    db.session.add(new_customer)
    db.session.commit()
    return "<p>Hello, World!</p>"


@app.route('/addDining', methods=['POST'])
def add_dining():
    name = request.json['name']
    location = request.json['location']
    franchise = request.json['franchise']
    working_hours = request.json['working_hours']
    new_dining = Dining(name=name, location=location,
                        franchise=franchise, working_hours=working_hours)
    db.session.add(new_dining)
    db.session.commit()
    return 'Successfully added'


@app.route('/addMealplan', methods=['POST'])
def add_mealplan():
    p_limit = request.json['price_limit']
    p_desc = request.json['plan_description']

    mealplan = MealPlans(price_limit=p_limit,
                         plan_description=p_desc)
    db.session.add(mealplan)
    db.session.commit()

    return 'Successfully added'


@app.route('/addExpenses', methods=['POST'])
def add_expense():
    exp_description = request.json['exp_description']
    exp_amount = request.json['exp_amount']
    dining_id = request.json['dining_id']
    new_expense = Expenses(exp_description=exp_description,
                           exp_amount=exp_amount, dining_id=dining_id)
    db.session.add(new_expense)
    db.session.commit()
    return 'Successfully Added'


@app.route('/addMenu', methods=['POST'])
def add_menu():
    if request.method == 'POST':
        item_name = request.json['item_name']
        item_price = request.json['item_price']
        gluten_free = request.json['gluten_free']
        alergen_free = request.json['alergen_free']
        vegan = request.json['vegan']
        dining_id = request.json['dining_id']

        menu = Menu(item_name=item_name, item_price=item_price, gluten_free=gluten_free,
                    alergen_free=alergen_free, vegan=vegan, dining_id=dining_id)
        db.session.add(menu)
        db.session.commit()

        return 'Successfully Added'
    return 'Failed to add'


@app.route('/addInventory', methods=['POST'])
def add_inventory():
    item_name = request.json['item_name']
    quantity = request.json['quantity']
    dining_id = request.json['dining_id']
    new_inventory = Inventory(
        item_name=item_name, quantity=quantity, dining_id=dining_id)
    db.session.add(new_inventory)
    db.session.commit()
    return 'Successfully added'


@app.route('/addEmployee', methods=['POST'])
def add_employee():
    emp_name = request.json['emp_name']
    emp_address = request.json['emp_address']
    emp_email = request.json['emp_email']
    emp_mobile = request.json['emp_mobile']
    emp_password = request.json['emp_password']
    dining_id = request.json['dining_id']
    new_employee = Employee(emp_name=emp_name, emp_address=emp_address, emp_email=emp_email,
                            emp_mobile=emp_mobile, emp_password=emp_password, dining_id=dining_id)
    db.session.add(new_employee)
    db.session.commit()
    return 'Successfully Added'


@app.route('/addAsset', methods=['POST'])
def add_asset():
    if request.method == 'POST':
        description = request.json['description']
        value = request.json['value']
        dining_id = request.json['dining_id']
        asset = Assets(description=description,
                       value=value, dining_id=dining_id)
        db.session.add(asset)
        db.session.commit()

        return 'Successfully Added'
    return 'Failed to add'


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


@app.route('/addReview', methods=['POST'])
def add_review():
    if request.method == 'POST':
        review_description = request.json['review_description']
        order_id = request.json['order_id']

        review = Reviews(
            review_description=review_description, order_id=order_id)
        db.session.add(review)
        db.session.commit()

        return 'Successfully added'
    return 'Failed to add'


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


if __name__ == '__main__':
    app.run()
