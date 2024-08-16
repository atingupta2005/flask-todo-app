from flask import Flask, request, redirect, url_for, render_template, flash
from models import db, TodoItem
import config

app = Flask(__name__)
app.config.from_object(config.Config)
db.init_app(app)

@app.route('/')
def index():
    todo_items = TodoItem.query.all()
    return render_template('index.html', todo_items=todo_items)

@app.route('/add', methods=['POST'])
def add():
    task = request.form.get('task')
    if task:
        new_item = TodoItem(task=task)
        db.session.add(new_item)
        db.session.commit()
        flash('Task added successfully!')
    return redirect(url_for('index'))

@app.route('/toggle/<int:id>')
def toggle(id):
    item = TodoItem.query.get_or_404(id)
    item.done = not item.done
    db.session.commit()
    flash('Task updated!')
    return redirect(url_for('index'))

@app.route('/delete/<int:id>')
def delete(id):
    item = TodoItem.query.get_or_404(id)
    db.session.delete(item)
    db.session.commit()
    flash('Task deleted!')
    return redirect(url_for('index'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
