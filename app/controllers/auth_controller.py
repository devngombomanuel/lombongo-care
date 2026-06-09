from flask import Blueprint, render_template, redirect, url_for, request, flash
from app.services.auth_service import AuthService
from flask_login import current_user

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard.index'))
    if request.method == 'POST':
        nome = request.form.get('nome')
        email = request.form.get('email')
        password = request.form.get('password')
        
        user, message = AuthService.register_user(nome, email, password)
        if user:
            flash(message, 'success')
            return redirect(url_for('auth.login'))  # <-- LINHA 19 CORRIGIDA AQUI
        flash(message, 'danger')
    return render_template('register.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard.index')) 
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        if AuthService.login_user(email, password):
            return redirect(url_for('dashboard.index')) 
        flash('Credenciais inválidas. Verifique o email e a palavra-passe.', 'danger')
    return render_template('login.html')

@auth_bp.route('/logout')
def logout():
    AuthService.logout_user()
    return redirect(url_for('auth.login'))