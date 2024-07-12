from app import app
from models import db, User,  Budget


with app.app_context():
    print ('Deleting data...')
    
    
    
    User.query.delete()
    Budget.query.delete()
    db.session.commit()


    print("Creating data..")

    u1 = User(email = "dan@gmail.com", name= "dan", password= '12345678')
    u2 = User(email = 'example@gmail.com', name = 'example', password = "12345")

    
    b1 = Budget(budget_name = "stima", amount= 300)
    b2 = Budget(budget_name = "rent", amount= 3000)

    
    
    users = [u1,u2]
    budgets = [b1, b2]
    

    db.session.add_all(users)
    db.session.add_all(budgets)   
    db.session.commit()

    print("seeding done")