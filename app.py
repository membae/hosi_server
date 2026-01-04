from models import db, User, Patient
from flask_migrate import Migrate
from flask import Flask, request, make_response, jsonify
from flask_restful import Api, Resource
from flask_jwt_extended import JWTManager, create_access_token, create_refresh_token, jwt_required, get_jwt_identity
from flask_cors import CORS
from werkzeug.security import check_password_hash,generate_password_hash
import os,secrets, datetime
from datetime import timedelta, datetime


BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.environ.get(
    "DB_URI", f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}")
app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] =secrets.token_hex(32)
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(minutes=30)
app.config['JWT_REFRESH_TOKEN_EXPIRES'] = timedelta(days=30)

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



class Login(Resource):
    def post(self):
        data=request.get_json()
        email=data.get("email")
        password=data.get("password")
        if "@" in email and password:
            user=User.query.filter_by(email=email).first()
            if user:
                if check_password_hash(user.password,password):
                    access_token=create_access_token(identity=user.id)
                    refresh_token=create_refresh_token(identity=user.id)
                    return make_response({"user":user.to_dict(),"access_token":access_token,"refresh_token":refresh_token},200)
                return make_response({"msg":"Incorrect password"},400)
            return make_response({"msg":"email not registered"},404)
        return make_response({"msg":"Invalid data"})

api.add_resource(Login,"/login")

# query all users, specific user, crud patients

class Get_users(Resource):
    def get(self):
        users=User.query.all()
        return make_response([user.to_dict() for user in users],200)
api.add_resource(Get_users,"/users")

class Get_user(Resource):
    def get(self,id):
        user=User.query.filter_by(id=id).first()
        if user:
            return make_response(user.to_dict(),200)
        return make_response({"msg":"user not found"},404)
    
    def patch(self,id):
        user=User.query.filter_by(id=id).first()
        if user:
            data=request.get_json()
            for attr in data:
                if attr in ['first_name','last_name','email','role']:
                    setattr(user,attr,data.get(attr))
                    
                if "password" in data:
                    user.password=generate_password_hash(data['password'])
                db.session.add(user)
                db.session.commit()
            return make_response(user.to_dict(),200)
        return make_response({"msg":"user not found"})
    
    
    def delete(self,id):
        user=User.query.filter_by(id=id).first()
        if user:
            db.session.delete(user)
            db.session.commit()
            return make_response({"msg":f"user{user} deleted successfully"})
        return make_response({"msg":f"user {user} not found"})
    
api.add_resource(Get_user,'/user/<int:id>')


class Get_patients(Resource):
    def get(self):
        patients=Patient.query.all()
        if patients:
            return make_response([patient.to_dict() for patient in patients])
        return make_response({"msg":"No patient records found"})
    
    def post(self):
        data=request.get_json()
        if "first_name" in data and "last_name" in data and "phone_number" in data and "doctor_summary" in data and "status" in data and "admitted_at" in data or "discharged_at" in data and "diagnosis" in data:
            new_patient=Patient(first_name=data.get("first_name"),last_name=data.get("last_name"),phone_number=data.get("phone_number"),doctor_summary=data.get("doctor_summary"),status=data.get("status"),admitted_at = datetime.fromisoformat(data["admitted_at"]),discharged_at=data.get("discharged_at"), diagnosis =data.get("diagnosis"))
            db.session.add(new_patient)
            db.session.commit()
            return make_response(new_patient.to_dict(),201)
        return make_response({"msg":"Missing data"},400)
    
api.add_resource(Get_patients,'/patients')

class Patient_by_Id(Resource):
    def get(self,id):
        patient=Patient.query.filter_by(id=id).first()
        if patient:
            return make_response(patient.to_dict(),200)
        return make_response({"msg":"patient not found"},404)
    
    def patch(self,id):
        pass
        




if __name__=="__main__":
    app.run(debug=True)