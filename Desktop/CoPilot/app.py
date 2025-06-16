from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from flask import redirect, url_for

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Define the Todo model
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    completed = db.Column(db.Boolean)

#Route to add a new todo item
@app.route('/add', methods=['POST'])
def add():

    title = request.form.get('title')
    new_todo = Todo(title=title, completed=False)
    db.session.add(new_todo)
    db.session.commit()
    return redirect(url_for('index'))

#Route to update a todo item

@app.route('/update/<int:todo_id>')
def update_todo(todo_id):
    todo = Todo.query.filter_by(id=todo_id).first()
    # title = request.form.get('title')
    todo.completed = not todo.completed  # Toggle completion status
    db.session.commit()
    return redirect(url_for('index'))

#Route to delete a todo item
@app.route('/delete/<int:todo_id>')
def delete_todo(todo_id):

    todo = Todo.query.filter_by(id=todo_id).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/')
def index():
    todo_list = Todo.query.all()
    return render_template('base.html', todo_list=todo_list)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Create database tables
    app.run(debug=True)

