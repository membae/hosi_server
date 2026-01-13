from models import db, User, Patient, Appointment, Report
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
            new_patient=Patient(first_name=data.get("first_name"),last_name=data.get("last_name"),phone_number=data.get("phone_number"),doctor_summary=data.get("doctor_summary"),status=data.get("status"),admitted_at = datetime.fromisoformat(data["admitted_at"]),discharged_at = datetime.fromisoformat(data["discharged_at"]), diagnosis =data.get("diagnosis"))
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
        patient=Patient.query.filter_by(id=id).first()
        if patient:
            data=request.get_json()
            for attr in data:
                if attr in['first_name','last_name','phone_number','diagnosis','doctor_summary','admitted_at','discharged_at','status']:
                    setattr(patient,attr,data.get(attr))
            if "admitted_at" in data :
                patient.admitted_at = datetime.fromisoformat(data["admitted_at"])
            if "discharged_at" in data :
                patient.discharged_at = datetime.fromisoformat(data["discharged_at"])  
            
            db.session.add(patient)
            db.session.commit()
            return make_response(patient.to_dict(),200)            
        return make_response ({"msg":"patient not found"})
    
    def delete(self,id):
        patient=Patient.query.filter_by(id=id).first()
        if patient:
            db.session.delete(patient)
            db.session.commit()
            return make_response({"msg":"patient deleted successfully"},200)
        return make_response({"msg":"patient not found"})
    
api.add_resource(Patient_by_Id,'/patient/<int:id>')

class Get_appointments(Resource):
    def get(self):
        appointments=Appointment.query.all()
        return make_response([appointment.to_dict() for appointment in appointments],200)
        # return make_response({"msg":"No appointment records found"},404)
    
    def post(self):
        data=request.get_json()
        if not data:
            return make_response({"msg":"no data provided"})
        
        if 'appointment_datetime' in data and 'status' in data and 'reason' in data and 'patient_id' in data and 'user_id' in data :
            patient=Patient.query.get(data['patient_id'])
            user=User.query.get(data['user_id'])
            if not patient:
                return make_response({"msg":"patient does not exist"},404)
            if not user:
                return make_response({"msg":"user does not exist"},404)
            new_appointment=Appointment(appointment_datetime=datetime.fromisoformat(
                data["appointment_datetime"]), status=data.get('status'), reason=data.get('reason'), patient_id=data.get('patient_id'), user_id=data.get('user_id'))
            
            db.session.add(new_appointment)
            db.session.commit()
            return make_response(new_appointment.to_dict(),201)
        return make_response({"msg":"field missing"},400)
    
api.add_resource(Get_appointments,'/appointment')

class Appointment_byId(Resource):
    def get(self,id):
        appointments = Appointment.query.all()
        if not appointments:
            return make_response({"msg": "No appointment records found"}, 404)

        result = []
        for appointment in appointments:
            data = appointment.to_dict()  # keep IDs
            data["patient_name"] = (
                f"{appointment.patient.first_name} {appointment.patient.last_name}"
                if appointment.patient else None
            )
            data["doctor_name"] = (
                f"{appointment.user.first_name} {appointment.user.last_name}"
                if appointment.user else None
            )
            result.append(data)

        return make_response(result, 200)

    
    
    def patch(self,id):
        appointment=Appointment.query.filter_by(id=id).first()
        if appointment:
            data=request.get_json()
            
            if "appointment_datetime" in data:
                appointment.appointment_datetime = datetime.fromisoformat(
            data["appointment_datetime"].replace("Z", "")
        )
            for attr in data:
                if attr in ['status','reason']:
                    setattr(appointment,attr,data.get(attr))
                if attr == "patient_id":
                    patient = db.session.get(Patient, data[attr])
                    if not patient:
                        return make_response({"msg": "patient does not exist"}, 404)

                if attr == "user_id":
                    user = db.session.get(User, data[attr])
                    if not user:
                        return make_response({"msg": "user does not exist"}, 404)
            db.session.add(appointment)
            db.session.commit()
            return make_response(appointment.to_dict(),200)
        return make_response({"msg":"appointment not found"},404)

    def delete(self,id):
        appointment=Appointment.query.filter_by(id=id).first()
        if appointment:
            db.session.delete(appointment)
            db.session.commit()
            return make_response({"msg":"appointment deleted successfully"},200)
        return make_response({"msg":"appointment not found"})
    
api.add_resource(Appointment_byId,'/appointment/<int:id>')

class GetReports(Resource):
    def get(self):
        reports=Report.query.all()
        return make_response([report.to_dict() for report in reports],200)
    
    def post(self):
        data=request.get_json()
        if not data:
            return make_response({"msg":"no data provided"},400)
        if "patient_id" in data and "user_id" in data and "diagnosis" in data:
            patient=Patient.query.get(data['patient_id'])
            user=User.query.get(data['user_id'])
            if not patient:
                return make_response({"msg":"patient does not exist"},404)
            if not user:
                return make_response({"msg":"user does not exist"},404)
            new_report=Report(patient_id=data.get("patient_id"), user_id=data.get("user_id"),diagnosis=data.get("diagnosis"))
            db.session.add(new_report)
            db.session.commit()
            return make_response(new_report.to_dict(),201)
        return make_response({"msg":"Missing field"},400)
    
    
    
api.add_resource( GetReports, "/reports")
        
        
class Report_byId(Resource):
    def get(self,id):
        report=Report.query.filter_by(id=id).first()
        if report:
            return make_response(report.to_dict(),200)
        return make_response({"msg":"report with that id does not exist"},404)
    
    
    def patch(self,id):
        report=Report.query.filter_by(id=id).first()
        if report:
            data=request.get_json()
            for attr in data:
                if attr in ['diagnosis','patient_id','user_id']:
                    setattr(report,attr,data.get(attr))
            db.session.add(report)
            db.session.commit()
            return make_response(report.to_dict(),200)
        return make_response({"msg":"report not found"},404)
    
    
    def delete(self,id):
        report=Report.query.filter_by(id=id).first()
        if report:
            db.session.delete(report)
            db.session.commit()
            return make_response({"msg":"report deleted succesfully"},200)
        return make_response({"msg":"report does not exist"},404)
api.add_resource(Report_byId,'/reports/<int:id>')


if __name__=="__main__":
    app.run(debug=True)