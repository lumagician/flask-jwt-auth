from config import db, ma

class User(db.Model):
    id = db.Column(db.String, primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    password_hash = db.Column(db.String(128), nullable=False)
    salt = db.Column(db.String, nullable=False)

    def __init__(self, id, username, password_hash, salt):
        self.id = id
        self.username = username
        self.password_hash = password_hash
        self.salt = salt


    
class UserSchema(ma.Schema):
    class Meta:
        fields = ("id", "username", "password_hash", "salt")

user_schema = UserSchema()

users_schema = UserSchema(many=True)