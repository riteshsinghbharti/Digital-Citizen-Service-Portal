from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, current_user, login_required
from app import db
from app.models import User
from app.forms import LoginForm, RegistrationForm

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        if current_user.is_admin():
            return redirect(url_for('admin.dashboard'))
        return redirect(url_for('citizen.dashboard'))

    form = LoginForm()
    if form.validate_on_submit():
        user_identifier = form.email.data.strip().lower()
        
        # Allow login via Email or Mobile number
        user = User.query.filter((User.email == user_identifier) | (User.mobile == user_identifier)).first()

        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')

            flash(f'Welcome back, {user.name}!', 'success')
            
            if next_page:
                return redirect(next_page)
            if user.is_admin():
                return redirect(url_for('admin.dashboard'))
            return redirect(url_for('citizen.dashboard'))
        else:
            flash('Invalid email/mobile number or password. Please try again.', 'danger')

    return render_template('auth/login.html', form=form)


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('citizen.dashboard'))

    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(
            name=form.name.data.strip(),
            email=form.email.data.strip().lower(),
            mobile=form.mobile.data.strip(),
            role='citizen',
            address=form.address.data.strip(),
            state=form.state.data,
            district=form.district.data.strip()
        )
        user.set_password(form.password.data)
        
        db.session.add(user)
        db.session.commit()

        flash('Your Citizen account has been created successfully! You can now log in.', 'success')
        return redirect(url_for('auth.login'))

    return render_template('auth/register.html', form=form)


@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out safely.', 'info')
    return redirect(url_for('main.index'))
