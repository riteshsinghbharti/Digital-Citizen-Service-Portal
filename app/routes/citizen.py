import json
from flask import Blueprint, render_template, redirect, url_for, flash, request, session
from flask_login import login_required, current_user
from app import db
from app.models import Service, Application, Document, Notification
from app.forms import ApplicationForm, ProfileForm, ChangePasswordForm
from app.utils import generate_app_number, get_timeline_steps, save_uploaded_file

citizen_bp = Blueprint('citizen', __name__)

@citizen_bp.route('/dashboard')
@login_required
def dashboard():
    if current_user.is_admin():
        return redirect(url_for('admin.dashboard'))

    # Citizen statistics
    applications = Application.query.filter_by(user_id=current_user.id).order_by(Application.created_at.desc()).all()
    
    total_apps = len(applications)
    pending_apps = sum(1 for a in applications if a.status == 'submitted')
    review_apps = sum(1 for a in applications if a.status in ('under_review', 'documents_verified'))
    approved_apps = sum(1 for a in applications if a.status == 'approved')
    rejected_apps = sum(1 for a in applications if a.status == 'rejected')
    
    recent_notifications = Notification.query.filter_by(user_id=current_user.id, is_read=False).order_by(Notification.created_at.desc()).limit(5).all()

    return render_template('citizen/dashboard.html',
                           applications=applications,
                           total_apps=total_apps,
                           pending_apps=pending_apps,
                           review_apps=review_apps,
                           approved_apps=approved_apps,
                           rejected_apps=rejected_apps,
                           unread_notifications=recent_notifications)


@citizen_bp.route('/apply/<int:service_id>', methods=['GET', 'POST'])
@login_required
def apply(service_id):
    service = Service.query.get_or_404(service_id)
    form = ApplicationForm()

    # Pre-fill user details on GET
    if request.method == 'GET':
        form.full_name.data = current_user.name
        form.email.data = current_user.email
        form.mobile.data = current_user.mobile
        form.street_address.data = current_user.address or ''
        form.state.data = current_user.state or ''
        form.district.data = current_user.district or ''
        form.purpose.data = f"Application for {service.name}"

    if form.validate_on_submit():
        # Process Document Uploads
        uploaded_docs = []
        doc_fields = [
            (form.id_proof.data, 'Identity Proof'),
            (form.address_proof.data, 'Address Proof'),
            (form.supporting_doc.data, 'Supporting Document')
        ]

        saved_files_metadata = []
        for file_data, doc_label in doc_fields:
            if file_data:
                try:
                    res = save_uploaded_file(file_data)
                    if res:
                        stored_name, rel_path, file_size, ext = res
                        saved_files_metadata.append({
                            'doc_type': doc_label,
                            'orig_name': file_data.filename,
                            'stored_name': stored_name,
                            'file_path': rel_path,
                            'file_type': ext,
                            'file_size': file_size
                        })
                except Exception as e:
                    flash(f'Error uploading {doc_label}: {str(e)}', 'danger')
                    return render_template('citizen/apply.html', service=service, form=form)

        # Build application draft payload in session for Review stage
        session['draft_app'] = {
            'service_id': service.id,
            'personal_info': {
                'full_name': form.full_name.data.strip(),
                'dob': form.dob.data.strip(),
                'gender': form.gender.data,
                'mobile': form.mobile.data.strip(),
                'email': form.email.data.strip()
            },
            'address_info': {
                'street_address': form.street_address.data.strip(),
                'city': form.city.data.strip(),
                'district': form.district.data.strip(),
                'state': form.state.data.strip(),
                'pincode': form.pincode.data.strip()
            },
            'purpose': form.purpose.data.strip(),
            'additional_info': form.additional_info.data.strip() if form.additional_info.data else '',
            'documents': saved_files_metadata
        }

        return redirect(url_for('citizen.apply_review', service_id=service.id))

    return render_template('citizen/apply.html', service=service, form=form)


@citizen_bp.route('/apply/<int:service_id>/review', methods=['GET', 'POST'])
@login_required
def apply_review(service_id):
    service = Service.query.get_or_404(service_id)
    draft = session.get('draft_app')

    if not draft or draft.get('service_id') != service.id:
        flash('Session expired or no draft application found. Please fill out the application form again.', 'warning')
        return redirect(url_for('citizen.apply', service_id=service.id))

    if request.method == 'POST':
        app_num = generate_app_number()

        new_app = Application(
            application_number=app_num,
            user_id=current_user.id,
            service_id=service.id,
            personal_info=json.dumps(draft['personal_info']),
            address_info=json.dumps(draft['address_info']),
            purpose=draft['purpose'],
            additional_info=draft['additional_info'],
            status='submitted',
            current_remarks='Application dossier submitted online by applicant.'
        )

        db.session.add(new_app)
        db.session.flush() # get new_app.id

        # Save Document database records
        for doc_meta in draft.get('documents', []):
            doc = Document(
                application_id=new_app.id,
                document_type=doc_meta['doc_type'],
                original_filename=doc_meta['orig_name'],
                stored_filename=doc_meta['stored_name'],
                file_path=doc_meta['file_path'],
                file_type=doc_meta['file_type'],
                file_size=doc_meta['file_size']
            )
            db.session.add(doc)

        # Generate Notification
        notif = Notification(
            user_id=current_user.id,
            title='Application Submitted',
            message=f'Your application for {service.name} (ID: {app_num}) has been successfully submitted.',
            type='application'
        )
        db.session.add(notif)

        db.session.commit()

        # Clear session draft
        session.pop('draft_app', None)

        flash(f'Application submitted successfully! Your Application ID is {app_num}.', 'success')
        return redirect(url_for('citizen.application_detail', application_id=new_app.id))

    return render_template('citizen/review.html', service=service, draft=draft)


@citizen_bp.route('/application/<int:application_id>')
@login_required
def application_detail(application_id):
    app_record = Application.query.get_or_404(application_id)

    # Security check: applicant or admin
    if not current_user.is_admin() and app_record.user_id != current_user.id:
        flash('Unauthorized access to application dossier.', 'danger')
        return redirect(url_for('citizen.dashboard'))

    timeline = get_timeline_steps(app_record.status)
    documents = app_record.documents

    return render_template('citizen/application_detail.html',
                           app_record=app_record,
                           timeline=timeline,
                           documents=documents)


@citizen_bp.route('/notifications', methods=['GET', 'POST'])
@login_required
def notifications():
    if request.method == 'POST':
        # Mark all as read
        Notification.query.filter_by(user_id=current_user.id).update({'is_read': True})
        db.session.commit()
        flash('All notifications marked as read.', 'info')
        return redirect(url_for('citizen.notifications'))

    user_notifs = Notification.query.filter_by(user_id=current_user.id).order_by(Notification.created_at.desc()).all()
    return render_template('citizen/notifications.html', notifications=user_notifs)


@citizen_bp.route('/notification/read/<int:notif_id>')
@login_required
def mark_notification_read(notif_id):
    notif = Notification.query.get_or_404(notif_id)
    if notif.user_id == current_user.id:
        notif.is_read = True
        db.session.commit()
    return redirect(url_for('citizen.notifications'))


@citizen_bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    profile_form = ProfileForm()
    password_form = ChangePasswordForm()

    if 'update_profile' in request.form and profile_form.validate_on_submit():
        current_user.name = profile_form.name.data.strip()
        current_user.mobile = profile_form.mobile.data.strip()
        current_user.address = profile_form.address.data.strip()
        current_user.state = profile_form.state.data.strip()
        current_user.district = profile_form.district.data.strip()
        db.session.commit()
        flash('Profile details updated successfully!', 'success')
        return redirect(url_for('citizen.profile'))

    if 'change_password' in request.form and password_form.validate_on_submit():
        if not current_user.check_password(password_form.current_password.data):
            flash('Current password is incorrect.', 'danger')
        else:
            current_user.set_password(password_form.new_password.data)
            db.session.commit()
            flash('Password changed successfully!', 'success')
            return redirect(url_for('citizen.profile'))

    if request.method == 'GET':
        profile_form.name.data = current_user.name
        profile_form.mobile.data = current_user.mobile
        profile_form.address.data = current_user.address
        profile_form.state.data = current_user.state
        profile_form.district.data = current_user.district

    return render_template('citizen/profile.html', profile_form=profile_form, password_form=password_form)
