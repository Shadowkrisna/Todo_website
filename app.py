from flask import Flask, render_template , request , redirect
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__) 
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///My_database.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False



db = SQLAlchemy(app)

class todo(db.Model):
    Sno = db.Column(db.Integer , primary_key = True)
    Title =  db.Column(db.String(100) , nullable = False)
    Desc =  db.Column(db.String(500) , nullable = False)
  
    def __repr__(self):
        return f"{self.Sno} - {self.Title}"


@app.route("/todo", methods = ["GET","POST"])
def add_user():
    if request.method=="POST":
        title =  request.form["title"]
        desc = request.form["desc"]    
        addd = todo(Title=title, Desc=desc)
        db.session.add(addd)
        db.session.commit()
    get = todo.query.all()
    return render_template('index.html' , get = get )
    # return f'User {user.Sno} added with its todo!'
    
@app.route('/update/<int:Sno>', methods=['GET', 'POST'])
def update(Sno):
    if request.method == 'POST':
        Title = request.form['title']
        Desc = request.form['desc']
        Todo = todo.query.filter_by(Sno=Sno).first()
        Todo.Title = Title   # <- match model field
        Todo.Desc = Desc     # <- match model field
        db.session.commit()
        return redirect("/todo")

    Todo = todo.query.filter_by(Sno=Sno).first()
    return render_template('update.html', Todo=Todo)


    
@app.route("/delete/<int:Sno>")
def delete(Sno):
    del_todo = todo.query.filter_by(Sno=Sno) . first()
    db.session.delete(del_todo)
    db.session.commit()
    return redirect("/todo")

# @app.route("/delete/<int:Sno>")
# def delete(Sno):
#     del_todo = todo.query.filter_by(Sno=Sno).first()
#     if del_todo:
#         db.session.delete(del_todo)
#         db.session.commit()
#     return redirect("/todo")

    
@app.route("/") 
def hi():
    return "hello it is a flask page"
    
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True , port=8000)
