from flask import Flask
from login import login_app
from backend import backend_app
from database import db
from flask_migrate import Migrate

app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='postgresql://neondb_owner:npg_CuwEal8X7hHN@ep-fancy-heart-a1kffa36-pooler.ap-southeast-1.aws.neon.tech/neondb?sslmode=require'#for creating the database
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']= False #for turning modification tracking off
db.init_app(app)
migrate= Migrate(app,db)

app.register_blueprint(backend_app)
app.register_blueprint(login_app)
with app.test_request_context():
    print(app.url_map)
if __name__ == "__main__":
    app.run(debug=True)
