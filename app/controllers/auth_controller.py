from app.vers import *
from app.models import handlers
from flask import render_template, flash, request, redirect, url_for, session, abort
from app.services import auth_service
from app.forms import LoginForm, RegisterForm, ChangePasswordForm



def check_authentication():
    session_data = session.get('username', None)
    if session_data is None:
        return False
    else:
        return True
        

@auth_bp.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if not check_authentication():
        logger.debug("Receive an 403 - Forbidden")
        return abort(403)
    else:
        username = session.get('username', None)
        status, domains = handlers.loadJson(f"{outputDir}/{username}{domainsjsonfile}")
        return render_template('dashboard.html', domains=domains, username=username)


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if check_authentication():
        return redirect(url_for('auth.dashboard'))
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        status, msg = auth_service.login_user(username=username, password=password)
        if status:
            session['username'] = username
            return redirect(url_for('auth.dashboard'))
        return render_template('login.html', form=form, error=msg, Mode=False)
    else:
        return render_template('login.html', form=form, error="", Mode=False)


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        status, msg = auth_service.register_user(username=username, password=password)
        if status:
            return redirect(url_for('auth.login'))
        return render_template('register.html', form=form, error=msg, Mode=False)
    return render_template('register.html', form=form, error="", Mode=False)


@auth_bp.route('/logout', methods=['GET', 'POST'])
def logout():
    session.pop('username', None)
    return redirect(url_for('auth.login'))


@auth_bp.route('/profile', methods=['GET', 'POST'])
def profile():
    if not check_authentication():
        logger.debug("Receive an 403 - Forbidden")
        return abort(403)
    else:
        form = ChangePasswordForm()
        username = session.get('username', None)
        if request.method == 'POST':
            if form.validate_on_submit():  
                current_password = form.current_password.data
                new_password = form.new_password.data
                status, msg, mode = auth_service.replace_password(username, current_password, new_password)
                if status:
                    flash(msg, mode)
                    return redirect(url_for('auth.profile'))
                else:
                    flash(msg, mode)
            return render_template('profile.html', form=form, username=username, mode='danger')
        else:
            return render_template('profile.html', form=form, username=username)
