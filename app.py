from flask import Flask,render_template, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy.orm import query

from werkzeug.utils import redirect

#initialize app to current file
app = Flask(__name__)

#connect to sqlite database db name = "test.db"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

#class to save details as in table in test.db
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    complete = db.Column(db.Integer, default=0)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __rep__(self):
        return '<Task %r>' % self.id

#first decorator displays  the home page
@app.route('/', methods=['POST','GET'])
def index():
    #if a new task is added it will go into this condition
    if request.method == 'POST':
        #takes the task content from the form in html
        task_content = request.form['content']
        #creats a object with given task
        new_task = Todo(content=task_content)
        
        try:
            #adding the task to the database
            db.session.add(new_task)
            db.session.commit()
            #after adding task to db it loads the home page
            return redirect('/')
        except:
            return "There was an issue adding your task"

    #if there are no updates just displays the available tasks
    else:
        tasks = Todo.query.order_by(Todo.date_created).all()
        return render_template('index.html', tasks=tasks)

#decorator to delete the task with id which we get from <int:id>
@app.route('/delete/<int:id>')
def delete(id):
    #check the database for the task with id , id
    task_to_delete = Todo.query.get_or_404(id)

    try:
        #delets the task
        db.session.delete(task_to_delete)
        db.session.commit()
        #goes back to home page to see the updates tasks
        return redirect('/')
    except:
        return 'error in delete'

#decoratir to update content of the task with the given id <int:id>
@app.route("/update/<int:id>", methods=['GET', 'POST'])
def update(id):
    #check for task with id if not present displays error 404
    task = Todo.query.get_or_404(id)
    
    if request.method == 'POST':
        #updates the task with the new content from the form
        task.content = request.form['content']
        try:
            db.session.commit()
            #after updating redirects to home page
            return redirect('/')
        except:
            return 'error in update'
    else:
        #it displays the update page till it gets post from form in the html
        return render_template('update.html',task=task)

#run the app unless the file is imported
if __name__ == "__main__":
    app.run(debug=True)