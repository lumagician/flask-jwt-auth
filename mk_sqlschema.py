from config import app, db
# create the database
app.app_context().push()
db.create_all()

# create the tables
from models import User
db.create_all()
