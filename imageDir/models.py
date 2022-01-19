from enum import unique
from imageDir import db

class User(db.Model):
    
    id = db.Column(db.Integer, primary_key =True)
    username= db.Column (db.String(20), unique = True, nullable = False)
    email= db.Column (db.String(120), unique = True, nullable = False)
    password= db.Column (db.String(60), nullable = False)
    
    def __repr__(self):
        return f"User('{self.username}', '{self.email}',)"
    
    
class imgDetails(db.Model):
    
    id = db.Column(db.Integer, primary_key = True)
    file = db.Column(db.Text, nullable= False)
    name  = db.Column(db.String(20))
    price = db.Column(db.Integer)
    discount = db.Column(db.Integer)
    discounted_price = db.Column(db.Integer)
    category = db.Column(db.String(20))
    private_user_id = db.Column(db.Integer, db.ForeignKey('user.id'))