import datetime, json
from flask import Flask, abort, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

app = Flask(__name__)
# Database configuration
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///tasks.db"
db = SQLAlchemy(app)
ma = Marshmallow(app)


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    check = db.Column(db.Boolean)

    def __init__(self, name, check):
        self.name = name
        self.check = check

    def __repr__(self):
        return "<Task %i: %s>" % (self.id, self.name)

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


# db.create_all()

task = [
    {
        "lmao": "lmao",
    }
]


class TaskSchema(ma.Schema):
    class Meta:
        fields = ("id", "name", "check")


task_schema = TaskSchema()
task_schema = TaskSchema(many=True)


all_tasks = Task.query.all()
print(all_tasks)


@app.route("/")
def hello_world():
    return "Hello, World!"


uri = "/api/tasks/"


@app.route(uri, methods=["GET"])
def get_tasks():
    return jsonify({"tasks": Task.as_dict(all_tasks)})


@app.route(uri + "<int:id>", methods=["GET"])
def get_task(id):
    task = Task.query.get_or_404(id)
    return jsonify({"task": Task.as_dict(task)})


@app.route(uri, methods=["POST"])
def create_task():
    if not request.json:
        abort(404)
    new_task = Task(name=request.json["name"], check=False)
    db.session.add(new_task)
    db.session.commit()
    return jsonify({"tasks": Task.as_dict(new_task)}), 201


@app.route(uri + "<int:task_id>", methods=["PUT"])
def update_task(task_id):
    if not request.json:
        abort(400)

    task = Task.query.get_or_404(task_id)

    task.name = request.json["name"]
    db.session.commit()
    task.check = request.json["check"]
    db.session.commit()

    if "name" in request.json and type(request.json.get("name")) is not str:
        abort(400)

    if "check" in request.json and type(request.json.get("check")) is not bool:
        abort(400)

    return jsonify({"task": Task.as_dict(task)}), 201


@app.route(uri + "<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)
    db.session.delete(task)
    db.session.commit()
    return jsonify({"result": True})


if __name__ == "__main__":
    app.run(debug=True)
