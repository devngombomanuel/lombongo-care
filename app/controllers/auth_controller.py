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
        
        valida, mensagem = AuthService.validar_forca_senha(password)
        if not valida:
            flash(mensagem, 'danger')
            return render_template('register.html')
            
        user, message = AuthService.register_user(nome, email, password)
        if user:
            flash(message, 'success')
            return redirect(url_for('auth.login'))
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

@auth_bp.route('/recuperar-senha', methods=['GET', 'POST'])
def recuperar_senha():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard.index'))
    if request.method == 'POST':
        email = request.form.get('email')
        AuthService.enviar_link_recuperacao(email)
        flash('Se o e-mail inserido constar no nosso sistema, receberá um link de recuperação.', 'success')
        return redirect(url_for('auth.recuperar_senha'))
    return render_template('recuperar_senha.html')

@auth_bp.route('/redefinir-senha/<token>', methods=['GET', 'POST'])
def redefinir_senha(token):
    if current_user.is_authenticated:
        return redirect(url_for('dashboard.index'))
        
    email = AuthService.verificar_token_recuperacao(token)
    if not email:
        flash('O link de recuperação é inválido ou expirou.', 'danger')
        return redirect(url_for('auth.recuperar_senha'))
        
    if request.method == 'POST':
        nova_senha = request.form.get('nova_senha')
        confirmar_senha = request.form.get('confirmar_senha')
        
        if nova_senha != confirmar_senha:
            flash('As passwords não coincidem.', 'danger')
            return render_template('redefinir_senha.html', token=token)
            
        valida, mensagem = AuthService.validar_forca_senha(nova_senha)
        if not valida:
            flash(mensagem, 'danger')
            return render_template('redefinir_senha.html', token=token)
            
        if AuthService.atualizar_senha_por_email(email, nova_senha):
            flash('Palavra-passe redefinida com sucesso! Já pode iniciar sessão.', 'success')
            return redirect(url_for('auth.login'))
        flash('Ocorreu um erro ao atualizar a palavra-passe.', 'danger')
        
    return render_template('redefinir_senha.html', token=token)