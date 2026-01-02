from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy_serializer import SerializerMixin

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
              