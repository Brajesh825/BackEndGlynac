import uuid
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Organization(db.Model):
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    phone = db.Column(db.String(50))
    address = db.Column(db.Text)
    website = db.Column(db.String(255), nullable=True)
    logo_url = db.Column(db.String(255), nullable=True)
    industry = db.Column(db.String(255))
    size = db.Column(db.Integer)
    owner_id = db.Column(db.String(36), nullable=False)  # Reference to a User model (not implemented here)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)

    def __repr__(self):
        return f"<Organisation {self.name}>"

class Department(db.Model):
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    organisation_id = db.Column(db.String(36), db.ForeignKey("organisation.id"), nullable=False)
    name = db.Column(db.String(255), nullable=False, unique=True)
    description = db.Column(db.Text, nullable=True)
    parent_department_id = db.Column(db.String(36), db.ForeignKey("department.id"), nullable=True)
    head_id = db.Column(db.String(36), db.ForeignKey("employee.id"), nullable=True)
    office_location = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f"<Department {self.name}>"

class Employee(db.Model):
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    organisation_id = db.Column(db.String(36), db.ForeignKey("organisation.id"), nullable=False)
    full_name = db.Column(db.String(255), nullable=False)
    work_email = db.Column(db.String(255), unique=True, nullable=False)
    phone = db.Column(db.String(50), nullable=True)
    job_title = db.Column(db.String(255), nullable=False)
    department_id = db.Column(db.String(36), db.ForeignKey("department.id"), nullable=True)
    manager_id = db.Column(db.String(36), db.ForeignKey("employee.id"), nullable=True)
    employee_code = db.Column(db.String(100), unique=True, nullable=False)
    employment_type = db.Column(db.String(100), nullable=False)
    hired_at = db.Column(db.DateTime, nullable=False)
    terminated_at = db.Column(db.DateTime, nullable=True)
    salary = db.Column(db.Float, nullable=True)
    is_active = db.Column(db.Boolean, default=True)
    office_location = db.Column(db.String(100), nullable=True)
    work_schedule = db.Column(db.JSON, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f"<Employee {self.full_name}>"

class Meeting(db.Model):
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    employee_id = db.Column(db.String(36), db.ForeignKey("employee.id"), nullable=False)
    scheduled_at = db.Column(db.DateTime, nullable=False)
    duration_minutes = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"<Meeting at {self.scheduled_at}>"
