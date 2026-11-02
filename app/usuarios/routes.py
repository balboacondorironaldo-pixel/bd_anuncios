from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
from werkzeug.security import generate_password_hash
from app.models import User
from app import db

usuarios_bp = Blueprint('usuarios', __name__, template_folder='../templates')

@usuarios_bp.route('/')
@login_required
def index():
    usuarios = User.query.all()
    return render_template('usuarios/index.html', usuarios=usuarios)

@usuarios_bp.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    usuario = User.query.get_or_404(id)
    if request.method == 'POST':
        usuario.username = request.form.get('username')
        usuario.email = request.form.get('email')
        password = request.form.get('password')
        if password:
            usuario.password_hash = generate_password_hash(password)
        db.session.commit()
        flash('Usuario actualizado correctamente.', 'success')
        return redirect(url_for('usuarios.index'))
    return render_template('usuarios/edit.html', usuario=usuario)

@usuarios_bp.route('/delete/<int:id>')
@login_required
def delete(id):
    usuario = User.query.get_or_404(id)
    db.session.delete(usuario)
    db.session.commit()
    flash('Usuario eliminado exitosamente.', 'success')
    return redirect(url_for('usuarios.index'))