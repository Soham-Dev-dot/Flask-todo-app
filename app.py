from flask import Flask, render_template, request, redirect,flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


app = Flask(__name__)
app.secret_key = 'your-secret-key'  # required for flash messages
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    details = db.Column(db.String(500), nullable=True)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"{self.id} - {self.title}"

@app.route('/', methods=['GET', 'POST'])
def hello_world():
    if request.method == 'POST':
        title = request.form.get('title')
        details = request.form.get('desc')
        todo = Todo(title=title, details=details)
        db.session.add(todo)
        db.session.commit()
        flash('Your todo was added successfully!', 'success')
        return redirect('/')
    allTodos = Todo.query.all()
    return render_template('text.html', allTodo=allTodos)
    # return 'Hello, World!'


@app.route('/product')
def product():
    allTodos = Todo.query.all()
    print(allTodos)
    return 'Product'

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    if request.method == 'POST':
        title = request.form['title']
        details = request.form['desc']
        todo =Todo.query.filter_by(id=id).first()
        todo.title = title
        todo.details = details
        db.session.add(todo)
        db.session.commit()
        return redirect('/')
    
    todo = Todo.query.filter_by(id=id).first()
    return render_template('update.html', todo=todo)
    

@app.route('/delete/<int:id>')
def delete(id):
    todo = Todo.query.filter_by(id=id).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect('/')


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
