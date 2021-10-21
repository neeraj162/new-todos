from flask import Blueprint, render_template, request, flash, jsonify, redirect
from flask_login import login_required, current_user
from .models import Todo
from . import db
import json

views = Blueprint('views', __name__)

@views.route("/", methods=['GET','POST'])
@login_required
def hello_world():
    if(request.method=="POST"):
        title = request.form.get("title")
        desc = request.form.get("desc")
        todo  = Todo(title=title,desc=desc,user_id=current_user.id)
        db.session.add(todo)
        db.session.commit()
    return render_template('index.html', user=current_user)
    # return "<p>Hello, World!</p>"

@views.route("/about")
@login_required
def about():
    return render_template('about.html')

@views.route("/update/<int:id>", methods=['GET','POST'])
@login_required
def update(id):
    if request.method=='POST':
        title = request.form.get("title")
        desc = request.form.get("desc")
        todo = Todo.query.filter_by(id=id).first()
        todo.title = title
        todo.desc = desc
        db.session.add(todo)
        db.session.commit()  
        return redirect('/') 
    todo = Todo.query.filter_by(id=id).first()
    return render_template('update.html', todo=todo)

@views.route("/delete/<int:id>")
@login_required
def delete(id):
    todo = Todo.query.filter_by(id=id).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect('/')