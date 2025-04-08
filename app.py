from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///blog.db"
db = SQLAlchemy(app)


class Person(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)


class Exercise(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    exercise_name = db.Column(db.String(100), unique=True)


class Mark(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_person = db.Column(db.ForeignKey("person.id"))
    id_exercise = db.Column(db.ForeignKey("exercise.id"))
    score = db.Column(db.Integer, nullable=False)


@app.route("/")
@app.route("/marks")
def read_marks_page():
    marks_all = Mark.query.all()
    persons_all = [Person.query.get(mark.id_person) for mark in marks_all]
    exercises_all = [Exercise.query.get(mark.id_exercise) for mark in marks_all]
    res = zip(marks_all, persons_all, exercises_all)
    return render_template("marks.html", marks=res)


@app.route("/marks/<int:id>")
def read_mark_detail_page(id):
    mark = Mark.query.get(id)
    person = Person.query.get(mark.id_person)
    exercise = Exercise.query.get(mark.id_exercise)
    return render_template("detail_mark.html", mark=mark, person=person, exercise=exercise)


@app.route("/marks/<int:id>/delete_mark", methods=["POST", "GET"])
def delete_mark_page(id):
    mark = Mark.query.get_or_404(id)
    try:
        db.session.delete(mark)
        db.session.commit()
        return redirect("/marks")
    except:
        return "При удалении оценки произошла ошибка"


@app.route("/create_mark", methods=["POST", "GET"])
def create_mark_page():
    persons_poll = Person.query.all()
    exercises_poll = Exercise.query.all()
    if request.method == "POST":
        id_person = request.form["id_person"]
        id_exercise = request.form["id_exercise"]
        score_value = request.form["score"]
        new_mark = Mark(score=score_value, id_person=id_person, id_exercise=id_exercise)
        try:
            db.session.add(new_mark)
            db.session.commit()
            return redirect("/marks")
        except:
            return "При добавлении статьи произошла ошибка"
    else:
        return render_template(
            "create_mark.html", persons=persons_poll, exercises=exercises_poll
        )


@app.route("/marks/<int:id>/update_mark", methods=["POST", "GET"])
def update_mark_page():
    pass


if __name__ == "__main__":
    app.run(debug=True)
    with app.app_context():
        db.create_all()
