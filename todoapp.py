from flask import Flask, url_for, render_template, redirect, request,flash
from flask_sqlalchemy import SQLAlchemy
 
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db=SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(100))
    email = db.Column(db.String(100))
    priority = db.Column(db.String(100))
    complete = db.Column(db.Boolean)


@app.route('/')
def homepage():
    todo_list = Todo.query.all()
    return render_template("index.html", todo_list=todo_list)

@app.route("/submit", methods=["POST", "GET]"])
def submit():
    description = request.form.get("description")
    email = request.form.get("email")
    priority = request.form.get("priority")
    new_todo = Todo(
    description=description,
    email=email,
    priority=priority
        )
    db.session.add(new_todo)
    db.session.commit()
    fo= open("task.txt", "a") 
    fo.writelines(description + "\r\n") 
    fo.writelines(email + "\r\n")
    fo.writelines(priority + "\r\n" + "\r\n")
    # fo.close()
    return redirect(url_for("homepage"))


@app.route('/clear/<int:id>')
def clear(id):
    todo = Todo.query.filter_by(id=id).first()
    db.session.delete(todo)
    db.session.commit()
    
    return redirect(url_for("homepage"))

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)