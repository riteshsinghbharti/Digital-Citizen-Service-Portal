from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField, TextAreaField, DateField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, Optional
from app.models import User

class LoginForm(FlaskForm):
    email = StringField('Email Address or Mobile Number', validators=[DataRequired(), Length(min=3, max=120)])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class RegistrationForm(FlaskForm):
    name = StringField('Full Name', validators=[DataRequired(), Length(min=2, max=120)])
    email = StringField('Email Address', validators=[DataRequired(), Email(), Length(max=120)])
    mobile = StringField('Mobile Number', validators=[DataRequired(), Length(min=10, max=15)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6, max=50)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password', message='Passwords must match.')])
    address = TextAreaField('Residential Address', validators=[DataRequired(), Length(min=5, max=500)])
    state = SelectField('State', choices=[
        ('', 'Select State'),
        ('Maharashtra', 'Maharashtra'),
        ('Delhi', 'Delhi'),
        ('Karnataka', 'Karnataka'),
        ('Uttar Pradesh', 'Uttar Pradesh'),
        ('Tamil Nadu', 'Tamil Nadu'),
        ('West Bengal', 'West Bengal'),
        ('Gujarat', 'Gujarat'),
        ('Other', 'Other')
    ], validators=[DataRequired()])
    district = StringField('District / City', validators=[DataRequired(), Length(min=2, max=80)])
    agree_terms = BooleanField('I agree to the Terms of Service and Privacy Policy', validators=[DataRequired(message="You must accept terms.")])
    submit = SubmitField('Create Citizen Account')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data.strip().lower()).first()
        if user:
            raise ValidationError('This email address is already registered. Please login.')


class ApplicationForm(FlaskForm):
    # Step 1: Personal Info
    full_name = StringField('Applicant Full Name', validators=[DataRequired(), Length(min=2, max=120)])
    dob = StringField('Date of Birth (YYYY-MM-DD)', validators=[DataRequired()])
    gender = SelectField('Gender', choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')], validators=[DataRequired()])
    mobile = StringField('Mobile Number', validators=[DataRequired(), Length(min=10, max=15)])
    email = StringField('Email Address', validators=[DataRequired(), Email()])

    # Step 2: Address Info
    street_address = StringField('House / Street Address', validators=[DataRequired()])
    city = StringField('City / Village', validators=[DataRequired()])
    district = StringField('District', validators=[DataRequired()])
    state = StringField('State', validators=[DataRequired()])
    pincode = StringField('PIN Code', validators=[DataRequired(), Length(min=6, max=6)])

    # Step 3: Application Details
    purpose = StringField('Purpose of Application', validators=[DataRequired(), Length(min=3, max=255)])
    additional_info = TextAreaField('Additional Remarks / Info', validators=[Optional()])

    # Step 4: Documents
    id_proof = FileField('Identity Proof (Aadhaar / Voter ID / Passport) [PDF/JPG/PNG]', validators=[
        FileAllowed(['pdf', 'jpg', 'jpeg', 'png'], 'Only PDF, JPG, and PNG files are allowed!')
    ])
    address_proof = FileField('Address Proof (Ration Card / Electricity Bill / Rent Agreement) [PDF/JPG/PNG]', validators=[
        FileAllowed(['pdf', 'jpg', 'jpeg', 'png'], 'Only PDF, JPG, and PNG files are allowed!')
    ])
    supporting_doc = FileField('Supporting Document (Income Certificate / Caste Proof / Pension File) [PDF/JPG/PNG]', validators=[
        FileAllowed(['pdf', 'jpg', 'jpeg', 'png'], 'Only PDF, JPG, and PNG files are allowed!')
    ])

    submit = SubmitField('Submit Application Dossier')


class GrievanceForm(FlaskForm):
    citizen_name = StringField('Full Name', validators=[DataRequired(), Length(min=2, max=120)])
    citizen_email = StringField('Email Address', validators=[DataRequired(), Email()])
    citizen_mobile = StringField('Mobile Number', validators=[DataRequired(), Length(min=10, max=15)])
    category = SelectField('Grievance Category', choices=[
        ('Delay in Service Delivery', 'Delay in Service Delivery'),
        ('Document Rejection Dispute', 'Document Rejection Dispute'),
        ('Technical / Portal Issue', 'Technical / Portal Issue'),
        ('Staff Misbehavior / Corruption', 'Staff Misbehavior / Corruption'),
        ('General Inquiry / Feedback', 'General Inquiry / Feedback')
    ], validators=[DataRequired()])
    subject = StringField('Subject / Application Reference ID', validators=[DataRequired(), Length(min=5, max=200)])
    description = TextAreaField('Detailed Complaint / Grievance Description', validators=[DataRequired(), Length(min=15, max=2000)])
    attachment = FileField('Optional Supporting Document (PDF / Image)', validators=[
        Optional(),
        FileAllowed(['pdf', 'jpg', 'jpeg', 'png'], 'Only PDF, JPG, and PNG files are allowed!')
    ])
    submit = SubmitField('File Grievance')


class ServiceForm(FlaskForm):
    name = StringField('Service Title', validators=[DataRequired(), Length(min=3, max=150)])
    description = TextAreaField('Service Description', validators=[DataRequired()])
    required_documents = TextAreaField('Required Documents (Comma-separated or bulleted)', validators=[DataRequired()])
    processing_time = StringField('Expected Processing Time', validators=[DataRequired(), Length(max=50)])
    category = SelectField('Category', choices=[
        ('Certificates', 'Certificates'),
        ('Pensions', 'Pensions'),
        ('Revenue', 'Revenue'),
        ('Others', 'Others')
    ], validators=[DataRequired()])
    icon = StringField('FontAwesome Icon Class (e.g. fa-file-invoice)', validators=[DataRequired()])
    submit = SubmitField('Save Service')


class StatusUpdateForm(FlaskForm):
    status = SelectField('Update Application Status', choices=[
        ('submitted', 'Submitted'),
        ('under_review', 'Under Review'),
        ('documents_verified', 'Documents Verified'),
        ('correction_requested', 'Correction Requested'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected')
    ], validators=[DataRequired()])
    remarks = TextAreaField('Administrative Remarks / Reason / Correction Details', validators=[DataRequired(), Length(min=3, max=1000)])
    submit = SubmitField('Update Application Status')


class GrievanceStatusForm(FlaskForm):
    status = SelectField('Status', choices=[
        ('open', 'Open'),
        ('in_progress', 'In Progress'),
        ('resolved', 'Resolved')
    ], validators=[DataRequired()])
    remarks = TextAreaField('Administrative Action Taken / Response', validators=[DataRequired(), Length(min=3, max=1000)])
    submit = SubmitField('Update Grievance Status')


class ProfileForm(FlaskForm):
    name = StringField('Full Name', validators=[DataRequired(), Length(min=2, max=120)])
    mobile = StringField('Mobile Number', validators=[DataRequired(), Length(min=10, max=15)])
    address = TextAreaField('Residential Address', validators=[DataRequired(), Length(min=5, max=500)])
    state = StringField('State', validators=[DataRequired()])
    district = StringField('District', validators=[DataRequired()])
    submit = SubmitField('Update Profile')


class ChangePasswordForm(FlaskForm):
    current_password = PasswordField('Current Password', validators=[DataRequired()])
    new_password = PasswordField('New Password', validators=[DataRequired(), Length(min=6, max=50)])
    confirm_new_password = PasswordField('Confirm New Password', validators=[DataRequired(), EqualTo('new_password', message='Passwords must match.')])
    submit = SubmitField('Change Password')
