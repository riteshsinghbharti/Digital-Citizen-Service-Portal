import os
import uuid
from functools import wraps
from flask import flash, redirect, url_for, current_app
from flask_login import current_user
from werkzeug.utils import secure_filename

def save_uploaded_file(file_obj, subfolder='documents'):
    """
    Saves an uploaded file safely using a generated UUID prefix.
    Returns tuple: (stored_filename, relative_file_path, file_size, file_type)
    """
    if not file_obj or not file_obj.filename:
        return None

    filename = secure_filename(file_obj.filename)
    if not filename:
        return None

    ext = filename.rsplit('.', 1)[-1].lower() if '.' in filename else ''
    allowed = current_app.config.get('ALLOWED_EXTENSIONS', {'pdf', 'jpg', 'jpeg', 'png'})
    if ext not in allowed:
        raise ValueError(f"File extension '.{ext}' is not allowed. Supported formats: {', '.join(allowed)}")

    unique_filename = f"{uuid.uuid4().hex[:12]}_{filename}"
    upload_dir = current_app.config['UPLOAD_FOLDER']
    os.makedirs(upload_dir, exist_ok=True)
    full_path = os.path.join(upload_dir, unique_filename)

    file_obj.save(full_path)
    file_size = os.path.getsize(full_path)
    
    # Enforce 5MB limit on saved file
    if file_size > current_app.config.get('MAX_CONTENT_LENGTH', 5 * 1024 * 1024):
        os.remove(full_path)
        raise ValueError("File size exceeds maximum allowed size (5 MB).")

    rel_path = f"uploads/documents/{unique_filename}"
    return (unique_filename, rel_path, file_size, ext)


def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            flash('Please log in with administrative credentials.', 'warning')
            return redirect(url_for('auth.login'))
        if not current_user.is_admin():
            flash('Access Denied. Administrative privileges required.', 'danger')
            return redirect(url_for('citizen.dashboard'))
        return f(*args, **kwargs)
    return decorated_function


def generate_app_number():
    return f"APP-2026-{uuid.uuid4().hex[:6].upper()}"


def generate_grievance_number():
    return f"GRV-2026-{uuid.uuid4().hex[:6].upper()}"


def get_status_badge(status):
    status_map = {
        'submitted': ('bg-info text-dark', 'Submitted'),
        'under_review': ('bg-warning text-dark', 'Under Review'),
        'documents_verified': ('bg-primary', 'Documents Verified'),
        'correction_requested': ('bg-secondary', 'Correction Required'),
        'approved': ('bg-success', 'Approved'),
        'rejected': ('bg-danger', 'Rejected'),
        'open': ('bg-danger', 'Open'),
        'in_progress': ('bg-warning text-dark', 'In Progress'),
        'resolved': ('bg-success', 'Resolved')
    }
    badge_class, label = status_map.get(status, ('bg-secondary', status.replace('_', ' ').title()))
    return f'<span class="badge {badge_class} fs-6 px-3 py-2">{label}</span>'


def get_timeline_steps(status):
    """
    Returns step status states for visual timeline progress bar.
    Stages: 1. Submitted, 2. Under Review, 3. Documents Verified, 4. Final (Approved/Rejected/Correction)
    """
    stages = [
        {'title': 'Application Submitted', 'active': False, 'completed': False, 'date': ''},
        {'title': 'Under Review', 'active': False, 'completed': False, 'date': ''},
        {'title': 'Document Verification', 'active': False, 'completed': False, 'date': ''},
        {'title': 'Final Approval & Certificate', 'active': False, 'completed': False, 'date': ''}
    ]

    if status == 'submitted':
        stages[0]['completed'] = True
        stages[1]['active'] = True
    elif status == 'under_review':
        stages[0]['completed'] = True
        stages[1]['completed'] = True
        stages[2]['active'] = True
    elif status == 'documents_verified':
        stages[0]['completed'] = True
        stages[1]['completed'] = True
        stages[2]['completed'] = True
        stages[3]['active'] = True
    elif status in ('approved', 'rejected', 'correction_requested'):
        stages[0]['completed'] = True
        stages[1]['completed'] = True
        stages[2]['completed'] = True
        stages[3]['completed'] = True
        if status == 'approved':
            stages[3]['title'] = 'Approved & Certificate Issued'
        elif status == 'rejected':
            stages[3]['title'] = 'Application Rejected'
        elif status == 'correction_requested':
            stages[3]['title'] = 'Correction Requested'

    return stages
