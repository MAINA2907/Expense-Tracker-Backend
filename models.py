from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.orm import validates
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.ext.associationproxy import association_proxy


metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

db = SQLAlchemy(metadata=metadata)


class User(db.Model, SerializerMixin):
    _tablename_ = 'user'
    
    id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String)
    name = db.Column(db.String)
    password = db.Column(db.String)

    # expenses = db.relationship('Expense', back_populates = "user", cascade = "all,delete-orphan")
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
    
    def _repr_(self):
        return f'<User {self.id}, {self.name}>'
    


    
class Budget(db.Model, SerializerMixin):
        _tablename_ = "budget"
            
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
        
        def _repr_(self):
            return f'<Budget {self.id}, {self.budget_name}, {self.amount}>'
        

    