
from datetime import datetime
from shop import login_manager,db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

# class Company(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     company_name = db.Column(db.String(20),nullable=False)
#     bikes = db.relationship('Bike', backref='company', lazy=True)

#     def __repr__(self):
#         return f"Company('{self.company_name}')"

# class Bike(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     title = db.Column(db.String(50),nullable=False)
#     description = db.Column(db.String(120), nullable=False)
#     price = db.Column(db.Numeric(10,2), nullable=False)
#     image_file = db.Column(db.String(30), nullable=False, default='default.jpg')
#     stock_level = db.Column(db.Integer, nullable=False)
#     company_id = db.Column(db.Integer, db.ForeignKey('company.id'), nullable=False)

#     def __repr__(self):
#         return f"Bike('{self.title}', '{self.description}', '{self.price}', '{self.stock_level}')"

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(20), nullable=False)
    last_name = db.Column(db.String(20), nullable=False)
    username = db.Column(db.String(15), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    password = db.Column(db.String(60), nullable=False)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

# class Checkout(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     first_name = db.Column(db.String(50),nullable=False)
#     last_name = db.Column(db.String(120), nullable=False)
#     card_number = db.Column(db.Numeric(20), nullable=False)
#     valid_until = db.Column(db.String(30), nullable=False)
#     security_code = db.Column(db.Numeric(5), nullable=False)

#     def __repr__(self):
#         return f"Checkout('{self.card_number}', '{self.valid_unitl}', '{self.security_code}')"

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

db.create_all()
db.session.commit()