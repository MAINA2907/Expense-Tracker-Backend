from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.orm import validates
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.ext.associationproxy import association_proxy


metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

db = SQLAlchemy(metadata=metadata)

expenses_categories = db.Table(
    'expenses_categories',
    metadata,
    db.Column('expense_id', db.Integer, db.ForeignKey(
        'expense.id'), primary_key=True),
    db.Column('category_id', db.Integer, db.ForeignKey(
        'category.id'), primary_key=True)
)

class User(db.Model, SerializerMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String)
    name = db.Column(db.String)
    password = db.Column(db.String)

    expenses = db.relationship('Expense', back_populates = "user", cascade = "all,delete-orphan")
    budgets = db.relationship('Budget', back_populates = "user", cascade = "all,delete-orphan")

    serialize_rules = ("-expenses", "-budgets",)

    @validates('name')
    def validates_name(self, key, name):
        if not name:
            raise ValueError("Must enter name")
        return name
    
    @validates('email')
    def validates_name(self, key, email):
        if "@" not in email:
            raise ValueError("Invalid email")
        return email
    
    def __repr__(self):
        return f'<User {self.id}, {self.name}>'




class Expense(db.Model, SerializerMixin):
    __tablename__ = 'expense'
    id = db.Column(db.Integer, primary_key = True)
    expense_name = db.Column(db.String)
    expense_amount = db.Column(db.Integer)
    date = db.Column(db.String)
    paymode=db.Column(db.String)
    category=db.Column(db.String)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    user = db.relationship('User', back_populates='expenses')
    categories = db.relationship('Category', secondary='expenses_categories', back_populates="expenses")
    categories = association_proxy('expense_category', 'category')


    serialize_rules = ("-user", "-categories",)


    @validates('expense_amount')
    def validate_amount(self, key, expense_amount):
        if expense_amount is None or expense_amount <= 0:
            raise ValueError("Amount must be a valid numeric value greater than zero")
        return expense_amount
    
    def __repr__(self):
        return f'<Expense {self.id}, {self.expense_name}>'



class Budget(db.Model, SerializerMixin):
    __tablename__ = "budget"
    id = db.Column(db.Integer, primary_key = True)
    amount = db.Column(db.Integer)
    budget_name = db.Column(db.String)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    user = db.relationship('User', back_populates = "budgets")
    serialize_rules = ("-user",)

    @validates('amount')
    def validate_amount(self, key, amount):
        if amount is None or amount <= 0:
            raise ValueError("Amount must be a valid numeric value greater than zero")
        return amount
    
    def __repr__(self):
        return f'<Budget {self.id}, {self.budget_name}, {self.amount}>'




class Category(db.Model, SerializerMixin):
    __tablename__ = "category"
    id = db.Column(db.Integer, primary_key=True)
    category_name = db.Column(db.String)
    expenses = db.relationship('Expense', secondary='expenses_categories', back_populates="categories")
    # expenses = db.relationship('Expense', secondary=categories, backref=db.backref('expenses_categories', lazy='dynamic'))

    
    

    def __repr__(self):
        return f'<Category {self.id}, {self.category_name}>'
    
# class ExpenseCategory(db.Model):
#     __tablename__ = "expensescategoies"
#     expense_id = db.Column('expense_id', db.Integer, db.ForeignKey('expense.id'), primary_key=True)
#     category_id = db.Column('category_id', db.Integer, db.ForeignKey('category.id'), primary_key=True)













