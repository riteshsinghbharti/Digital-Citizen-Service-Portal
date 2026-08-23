from datetime import datetime
import json
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import db

class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    mobile = db.Column(db.String(15), nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    role = db.Column(db.String(20), nullable=False, default='citizen') # 'citizen' or 'admin'
    address = db.Column(db.Text, nullable=True)
    state = db.Column(db.String(80), nullable=True)
    district = db.Column(db.String(80), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    applications = db.relationship('Application', backref='user', lazy=True, cascade="all, delete-orphan")
    grievances = db.relationship('Grievance', backref='user', lazy=True)
    notifications = db.relationship('Notification', backref='user', lazy=True, cascade="all, delete-orphan")

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def is_admin(self):
        return self.role == 'admin'

    def __repr__(self):
        return f'<User {self.email} ({self.role})>'


class Service(db.Model):
    __tablename__ = 'services'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text, nullable=False)
    required_documents = db.Column(db.Text, nullable=False) # Store comma-separated or formatted list
    processing_time = db.Column(db.String(50), nullable=False) # e.g. "7 Working Days"
    category = db.Column(db.String(80), nullable=False, default='Certificates') # e.g., Certificates, Pensions, Revenue, Others
    icon = db.Column(db.String(50), default='fa-file-medical')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    applications = db.relationship('Application', backref='service', lazy=True)

    def __repr__(self):
        return f'<Service {self.name}>'


class Application(db.Model):
    __tablename__ = 'applications'

    id = db.Column(db.Integer, primary_key=True)
    application_number = db.Column(db.String(50), unique=True, nullable=False, index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    service_id = db.Column(db.Integer, db.ForeignKey('services.id'), nullable=False)
    
    # Store dynamic form fields as JSON strings for flexibility
    personal_info = db.Column(db.Text, nullable=True) # JSON string
    address_info = db.Column(db.Text, nullable=True)  # JSON string
    
    purpose = db.Column(db.String(255), nullable=False)
    additional_info = db.Column(db.Text, nullable=True)
    
    # Statuses: 'submitted', 'under_review', 'documents_verified', 'approved', 'rejected', 'correction_requested'
    status = db.Column(db.String(40), nullable=False, default='submitted')
    current_remarks = db.Column(db.Text, nullable=True)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    documents = db.relationship('Document', backref='application', lazy=True, cascade="all, delete-orphan")

    def get_personal_info(self):
        if self.personal_info:
            try:
                return json.loads(self.personal_info)
            except Exception:
                return {}
        return {}

    def get_address_info(self):
        if self.address_info:
            try:
                return json.loads(self.address_info)
            except Exception:
                return {}
        return {}

    def __repr__(self):
        return f'<Application {self.application_number} ({self.status})>'


class Document(db.Model):
    __tablename__ = 'documents'

    id = db.Column(db.Integer, primary_key=True)
    application_id = db.Column(db.Integer, db.ForeignKey('applications.id'), nullable=False)
    document_type = db.Column(db.String(100), nullable=False) # e.g. "Identity Proof", "Address Proof", "Income Document"
    original_filename = db.Column(db.String(255), nullable=False)
    stored_filename = db.Column(db.String(255), nullable=False)
    file_path = db.Column(db.String(500), nullable=False)
    file_type = db.Column(db.String(50), nullable=False)
    file_size = db.Column(db.Integer, nullable=False) # bytes
    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Document {self.original_filename} for App {self.application_id}>'


class Grievance(db.Model):
    __tablename__ = 'grievances'

    id = db.Column(db.Integer, primary_key=True)
    grievance_number = db.Column(db.String(50), unique=True, nullable=False, index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    citizen_name = db.Column(db.String(120), nullable=False)
    citizen_email = db.Column(db.String(120), nullable=False)
    citizen_mobile = db.Column(db.String(15), nullable=False)
    category = db.Column(db.String(100), nullable=False)
    subject = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    attachment_path = db.Column(db.String(500), nullable=True)
    
    # Statuses: 'open', 'in_progress', 'resolved'
    status = db.Column(db.String(30), nullable=False, default='open')
    remarks = db.Column(db.Text, nullable=True)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<Grievance {self.grievance_number} ({self.status})>'


class Notification(db.Model):
    __tablename__ = 'notifications'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    title = db.Column(db.String(150), nullable=False)
    message = db.Column(db.Text, nullable=False)
    type = db.Column(db.String(50), default='application') # application, grievance, system
    is_read = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Notification {self.title} for User {self.user_id}>'
