from models import db, User
from flask_migrate import Migrate
from flask import Flask, request, make_response, jsonify
from flask_restful import Api, Resource
from flask_jwt_extended import JWTManager, create_access_token, create_refresh_token, jwt_required, get_jwt_identity
from flask_cors import CORS
from werkzeug.security import check_password_hash,generate_password_hash
import os


BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.environ.get(
    "DB_URI", f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}")
app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
migrate = Migrate(app, db)

db.init_app(app)
api=Api(app)
jwt=JWTManager(app)

class Home(Resource):
    def get(self):
        return make_response({"msg":"homepage here"},200)
    
api.add_resource(Home,'/')


class Signup(Resource):
    def post(self):
        data=request.get_json()
        email=data.get("email")
        first_name=data.get("first_name")
        last_name=data.get("last_name")
        password=generate_password_hash(data.get("password"))
        role=data.get("role")
        if "@" in email and first_name and first_name!=" " and last_name and last_name!=" " and role and role!=" " and data.get("password") and data.get("password")!=" ":
            user= User.query.filter_by(email=email).first()
            if user:
                return make_response({"msg":f"{email} is already registered"},400)
            new_user=User(first_name=first_name, last_name=last_name, password=password, role=role, email=email)
            db.session.add(new_user)
            db.session.commit()
            return make_response(new_user.to_dict(),201)
        return make_response({"msg":"invalid entires"},400)
api.add_resource(Signup,'/signup')












if __name__=="__main__":
    app.run(debug=True)