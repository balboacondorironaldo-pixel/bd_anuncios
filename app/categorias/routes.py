from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
from app.models import Category
from app import db

categorias_bp = Blueprint('categorias', __name__, template_folder='../templates')

@categorias_bp.route('/')
@login_required
def index():
    categorias = Category.query.all()
    return render_template('categorias/index.html', categorias=categorias)

@categorias_bp.route('/create', methods=['POST'])
@login_required
def create():
    nombre = request.form.get('nombre')
    descripcion = request.form.get('descripcion')
    
    if Category.query.filter_by(nombre=nombre).first():
        flash('La categoría ya existe.', 'warning')
        return redirect(url_for('categorias.index'))
        
    nueva_cat = Category(nombre=nombre, descripcion=descripcion)
    db.session.add(nueva_cat)
    db.session.commit()
    flash('Categoría creada con éxito.', 'success')
    return redirect(url_for('categorias.index'))

@categorias_bp.route('/delete/<int:id>')
@login_required
def delete(id):
    cat = Category.query.get_or_404(id)
    db.session.delete(cat)
    db.session.commit()
    flash('Categoría eliminada.', 'success')
    return redirect(url_for('categorias.index'))