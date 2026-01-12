from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy_serializer import SerializerMixin
from datetime import datetime

metadata= MetaData()
db=SQLAlchemy(metadata=metadata)


class User(db.Model, SerializerMixin):
    __tablename__="users"
    
    id=db.Column(db.Integer, primary_key=True)
    first_name=db.Column(db.String,nullable=False)
    last_name=db.Column(db.String,nullable=False)
    email=db.Column(db.String,unique=True, nullable=False)
    password=db.Column(db.String, nullable=False)
    role=db.Column(db.String, default="Admin", nullable=False)
    
    appointments=db.relationship("Appointment",back_populates="user", cascade="all, delete-orphan")
    reports=db.relationship("Report",back_populates='user')
    
    serialize_rules = ("-appointments.user",)
    
class Patient(db.Model, SerializerMixin):
    __tablename__="patients"
    id=db.Column(db.Integer, primary_key=True)
    first_name=db.Column(db.String, nullable=False)
    last_name=db.Column(db.String, nullable=False)
    phone_number=db.Column(db.String, unique=True, nullable=False)  
    status=db.Column(db.String, default="Admitted", nullable=False)
    doctor_summary=db.Column(db.String, nullable=False)
    diagnosis=db.Column(db.String, nullable=False)
    admitted_at=db.Column(db.DateTime, nullable=True)
    discharged_at=db.Column(db.DateTime, nullable=True)
    
    appointments=db.relationship("Appointment", back_populates="patient", cascade="all, delete-orphan")
    reports=db.relationship('Report', back_populates='patient', cascade='all, delete-orphan')
    
    serialize_rules = ("-appointments.patient",)
    
    
class Appointment(db.Model, SerializerMixin):
    __tablename__="appointments"
    
    id=db.Column(db.Integer,primary_key=True)
    appointment_datetime=db.Column(db.DateTime, nullable=False)
    status=db.Column(db.String, nullable=False)
    reason=db.Column(db.String, nullable=False)
    
    patient_id=db.Column(db.Integer, db.ForeignKey('patients.id'), nullable=False)
    user_id=db.Column(db.Integer, db.ForeignKey('users.id'),nullable=False)
    
    patient=db.relationship("Patient",back_populates="appointments")
    user=db.relationship("User", back_populates="appointments")
    
    serialize_rules = ("-user.appointments", "-patient.appointments")
    
class Report(db.Model,SerializerMixin):
    __tablename__='reports'
    
    id=db.Column(db.Integer, primary_key=True)
    patient_id=db.Column(db.Integer, db.ForeignKey('patients.id'), nullable=False)
    user_id=db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    diagnosis=db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    patient=db.relationship("Patient", back_populates='reports')
    user=db.relationship("User", back_populates='reports')
    
    
        
              