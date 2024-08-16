from flask import Flask, request, redirect, url_for, render_template, flash
from models import db, TodoItem
import config
import argparse

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

def main():
    # Set up argument parsing
    parser = argparse.ArgumentParser(description='Run the Flask application.')
    parser.add_argument('--port', type=int, default=5000, help='Port number to run the Flask application on.')
    
    # Parse the arguments
    args = parser.parse_args()

    # Create all database tables (if applicable)
    with app.app_context():
        db.create_all()

    # Run the Flask application
    app.run(debug=True, host='0.0.0.0', port=args.port)

if __name__ == '__main__':
    main()
