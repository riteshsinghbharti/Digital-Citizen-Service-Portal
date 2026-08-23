from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import current_user
from app import db
from app.models import Service, Application, Grievance, User
from app.forms import GrievanceForm
from app.utils import generate_grievance_number, get_timeline_steps, save_uploaded_file

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    # Fetch key public statistics
    total_services = Service.query.count()
    total_applications = Application.query.count()
    completed_applications = Application.query.filter_by(status='approved').count()
    total_citizens = User.query.filter_by(role='citizen').count()

    # Featured services for homepage cards
    featured_services = Service.query.limit(6).all()

    return render_template('main/index.html',
                           total_services=total_services,
                           total_applications=total_applications,
                           completed_applications=completed_applications,
                           total_citizens=total_citizens,
                           featured_services=featured_services)


@main_bp.route('/services')
def services():
    query = request.args.get('q', '').strip()
    category = request.args.get('category', '').strip()

    services_query = Service.query

    if query:
        services_query = services_query.filter(
            (Service.name.ilike(f'%{query}%')) |
            (Service.description.ilike(f'%{query}%'))
        )
    if category and category != 'All':
        services_query = services_query.filter_by(category=category)

    services_list = services_query.all()
    categories = ['All', 'Certificates', 'Pensions', 'Revenue', 'Others']

    return render_template('main/services.html',
                           services=services_list,
                           query=query,
                           selected_category=category or 'All',
                           categories=categories)


@main_bp.route('/track', methods=['GET', 'POST'])
def track():
    app_number = request.args.get('app_id', '').strip() or request.form.get('app_id', '').strip()
    searched_app = None
    timeline = None

    if app_number:
        searched_app = Application.query.filter_by(application_number=app_number).first()
        if searched_app:
            timeline = get_timeline_steps(searched_app.status)
        else:
            flash(f'No application found with ID: "{app_number}". Please double check the ID format (e.g. APP-2026-XXXXX).', 'warning')

    return render_template('main/track.html',
                           searched_app=searched_app,
                           app_number=app_number,
                           timeline=timeline)


@main_bp.route('/grievance', methods=['GET', 'POST'])
def grievance():
    form = GrievanceForm()
    
    # Auto-fill for logged-in citizen
    if request.method == 'GET' and current_user.is_authenticated:
        form.citizen_name.data = current_user.name
        form.citizen_email.data = current_user.email
        form.citizen_mobile.data = current_user.mobile

    if form.validate_on_submit():
        attachment_path = None
        if form.attachment.data:
            try:
                res = save_uploaded_file(form.attachment.data)
                if res:
                    attachment_path = res[1]
            except Exception as e:
                flash(f'Error uploading attachment: {str(e)}', 'danger')
                return render_template('main/grievance.html', form=form)

        grv_num = generate_grievance_number()
        new_grievance = Grievance(
            grievance_number=grv_num,
            user_id=current_user.id if current_user.is_authenticated else None,
            citizen_name=form.citizen_name.data.strip(),
            citizen_email=form.citizen_email.data.strip().lower(),
            citizen_mobile=form.citizen_mobile.data.strip(),
            category=form.category.data,
            subject=form.subject.data.strip(),
            description=form.description.data.strip(),
            attachment_path=attachment_path,
            status='open'
        )

        db.session.add(new_grievance)
        db.session.commit()

        flash(f'Your grievance has been submitted successfully! Your Grievance Reference ID is {grv_num}. Keep this for tracking.', 'success')
        return redirect(url_for('main.grievance'))

    return render_template('main/grievance.html', form=form)


@main_bp.route('/certificate/<int:application_id>')
def certificate(application_id):
    app_record = Application.query.get_or_404(application_id)

    # Security check: only applicant or admin can view/download certificate
    if not current_user.is_authenticated:
        flash('Please login to download the official certificate.', 'warning')
        return redirect(url_for('auth.login'))

    if not current_user.is_admin() and app_record.user_id != current_user.id:
        flash('Unauthorized access to application certificate.', 'danger')
        return redirect(url_for('citizen.dashboard'))

    if app_record.status != 'approved':
        flash('Certificate is only available for approved applications.', 'warning')
        return redirect(url_for('citizen.application_detail', application_id=app_record.id))

    return render_template('main/certificate.html', app_record=app_record)
