from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app import db
from app.models import Service, Application, Grievance, User, Document, Notification
from app.forms import ServiceForm, StatusUpdateForm, GrievanceStatusForm
from app.utils import admin_required, get_timeline_steps

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/dashboard')
@login_required
@admin_required
def dashboard():
    status_filter = request.args.get('status', '').strip()
    search_query = request.args.get('q', '').strip()

    # Admin Metrics
    total_citizens = User.query.filter_by(role='citizen').count()
    total_applications = Application.query.count()
    pending_apps = Application.query.filter_by(status='submitted').count()
    approved_apps = Application.query.filter_by(status='approved').count()
    rejected_apps = Application.query.filter_by(status='rejected').count()
    open_grievances = Grievance.query.filter(Grievance.status.in_(['open', 'in_progress'])).count()

    # Applications list query
    apps_query = Application.query.join(User).join(Service)

    if status_filter:
        apps_query = apps_query.filter(Application.status == status_filter)

    if search_query:
        apps_query = apps_query.filter(
            (Application.application_number.ilike(f'%{search_query}%')) |
            (User.name.ilike(f'%{search_query}%')) |
            (Service.name.ilike(f'%{search_query}%'))
        )

    applications_list = apps_query.order_by(Application.updated_at.desc()).all()

    return render_template('admin/dashboard.html',
                           total_citizens=total_citizens,
                           total_applications=total_applications,
                           pending_apps=pending_apps,
                           approved_apps=approved_apps,
                           rejected_apps=rejected_apps,
                           open_grievances=open_grievances,
                           applications=applications_list,
                           status_filter=status_filter,
                           search_query=search_query)


@admin_bp.route('/application/<int:application_id>', methods=['GET', 'POST'])
@login_required
@admin_required
def application_detail(application_id):
    app_record = Application.query.get_or_404(application_id)
    form = StatusUpdateForm()

    if request.method == 'GET':
        form.status.data = app_record.status
        form.remarks.data = app_record.current_remarks or ''

    if form.validate_on_submit():
        old_status = app_record.status
        new_status = form.status.data
        new_remarks = form.remarks.data.strip()

        app_record.status = new_status
        app_record.current_remarks = new_remarks

        # Trigger notification to applicant
        status_labels = {
            'submitted': 'Submitted',
            'under_review': 'Under Officer Review',
            'documents_verified': 'Documents Verified',
            'correction_requested': 'Correction Requested',
            'approved': 'Approved - Certificate Issued',
            'rejected': 'Application Rejected'
        }
        status_str = status_labels.get(new_status, new_status.title())

        notif = Notification(
            user_id=app_record.user_id,
            title=f'Application Status Updated: {status_str}',
            message=f'Your application ({app_record.application_number}) status has been updated to "{status_str}". Remarks: {new_remarks}',
            type='application'
        )
        db.session.add(notif)
        db.session.commit()

        flash(f'Application {app_record.application_number} status updated to "{status_str}". Applicant notified.', 'success')
        return redirect(url_for('admin.application_detail', application_id=app_record.id))

    timeline = get_timeline_steps(app_record.status)
    documents = app_record.documents

    return render_template('admin/application_detail.html',
                           app_record=app_record,
                           form=form,
                           timeline=timeline,
                           documents=documents)


@admin_bp.route('/grievances')
@login_required
@admin_required
def grievances():
    status_filter = request.args.get('status', '').strip()
    grievances_query = Grievance.query

    if status_filter:
        grievances_query = grievances_query.filter_by(status=status_filter)

    grievances_list = grievances_query.order_by(Grievance.created_at.desc()).all()

    return render_template('admin/grievances.html',
                           grievances=grievances_list,
                           status_filter=status_filter)


@admin_bp.route('/grievance/<int:grievance_id>', methods=['GET', 'POST'])
@login_required
@admin_required
def grievance_detail(grievance_id):
    grv = Grievance.query.get_or_404(grievance_id)
    form = GrievanceStatusForm()

    if request.method == 'GET':
        form.status.data = grv.status
        form.remarks.data = grv.remarks or ''

    if form.validate_on_submit():
        grv.status = form.status.data
        grv.remarks = form.remarks.data.strip()

        # Send notification to user if linked
        if grv.user_id:
            notif = Notification(
                user_id=grv.user_id,
                title=f'Grievance Status Update ({grv.grievance_number})',
                message=f'Your grievance status has been updated to "{grv.status.title()}". Officer response: {grv.remarks}',
                type='grievance'
            )
            db.session.add(notif)

        db.session.commit()

        flash(f'Grievance {grv.grievance_number} updated to "{grv.status.title()}".', 'success')
        return redirect(url_for('admin.grievance_detail', grievance_id=grv.id))

    return render_template('admin/grievance_detail.html', grievance=grv, form=form)


@admin_bp.route('/services')
@login_required
@admin_required
def services():
    services_list = Service.query.order_by(Service.category, Service.name).all()
    return render_template('admin/services.html', services=services_list)


@admin_bp.route('/service/add', methods=['GET', 'POST'])
@login_required
@admin_required
def add_service():
    form = ServiceForm()
    if form.validate_on_submit():
        new_service = Service(
            name=form.name.data.strip(),
            description=form.description.data.strip(),
            required_documents=form.required_documents.data.strip(),
            processing_time=form.processing_time.data.strip(),
            category=form.category.data,
            icon=form.icon.data.strip()
        )
        db.session.add(new_service)
        db.session.commit()
        flash(f'Service "{new_service.name}" added successfully!', 'success')
        return redirect(url_for('admin.services'))

    return render_template('admin/service_form.html', form=form, title='Add New Government Service')


@admin_bp.route('/service/edit/<int:service_id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_service(service_id):
    service = Service.query.get_or_404(service_id)
    form = ServiceForm()

    if request.method == 'GET':
        form.name.data = service.name
        form.description.data = service.description
        form.required_documents.data = service.required_documents
        form.processing_time.data = service.processing_time
        form.category.data = service.category
        form.icon.data = service.icon

    if form.validate_on_submit():
        service.name = form.name.data.strip()
        service.description = form.description.data.strip()
        service.required_documents = form.required_documents.data.strip()
        service.processing_time = form.processing_time.data.strip()
        service.category = form.category.data
        service.icon = form.icon.data.strip()

        db.session.commit()
        flash(f'Service "{service.name}" updated successfully!', 'success')
        return redirect(url_for('admin.services'))

    return render_template('admin/service_form.html', form=form, title=f'Edit Service: {service.name}')


@admin_bp.route('/service/delete/<int:service_id>', methods=['POST'])
@login_required
@admin_required
def delete_service(service_id):
    service = Service.query.get_or_404(service_id)
    name = service.name
    db.session.delete(service)
    db.session.commit()
    flash(f'Service "{name}" deleted successfully.', 'info')
    return redirect(url_for('admin.services'))


@admin_bp.route('/users')
@login_required
@admin_required
def users():
    citizens = User.query.filter_by(role='citizen').order_by(User.created_at.desc()).all()
    return render_template('admin/users.html', citizens=citizens)
