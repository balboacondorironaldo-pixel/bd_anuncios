from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app.models import Announcement, Category
from app import db

anuncios_bp = Blueprint('anuncios', __name__, template_folder='../templates')

@anuncios_bp.route('/')
def index():
    anuncios = Announcement.query.order_by(Announcement.fecha_creacion.desc()).all()
    categorias = Category.query.all()
    return render_template('anuncios/index.html', anuncios=anuncios, categorias=categorias)

@anuncios_bp.route('/create', methods=['POST'])
@login_required
def create():
    titulo = request.form.get('titulo')
    contenido = request.form.get('contenido')
    categoria_id = request.form.get('categoria_id')
    
    nuevo_anuncio = Announcement(
        titulo=titulo,
        contenido=contenido,
        categoria_id=categoria_id,
        usuario_id=current_user.id
    )
    db.session.add(nuevo_anuncio)
    db.session.commit()
    flash('Anuncio publicado correctamente.', 'success')
    return redirect(url_for('anuncios.index'))

@anuncios_bp.route('/delete/<int:id>')
@login_required
def delete(id):
    anuncio = Announcement.query.get_or_404(id)
    if anuncio.usuario_id == current_user.id:
        db.session.delete(anuncio)
        db.session.commit()
        flash('Anuncio eliminado.', 'success')
    else:
        flash('No tienes permisos para eliminar este anuncio.', 'danger')
    return redirect(url_for('anuncios.index'))