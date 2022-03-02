import datetime, json
from flask import Flask, abort, jsonify, request

app = Flask(__name__)

tasks = [
    {
        "id": 1,
        "name": "Tomar la clase",
        "check": False,
        "creado": datetime.datetime.now(),
    },
    {
        "id": 2,
        "name": "Hacer la tarea",
        "check": False,
        "creado": datetime.datetime.now(),
    },
]


@app.route("/")
def hello_world():
    return "Hello, World!"


uri = "/api/tasks/"


@app.route(uri, methods=["GET"])
def get_tasks():
    return jsonify({"tasks": tasks})


@app.route(uri + "<int:id>", methods=["GET"])
def get_task(id):
    this_task = [task for task in tasks if task["id"] == id]
    return (
        jsonify({"task": this_task[0]})
        if this_task
        else jsonify({"status": "ID Inexistente"})
    )


@app.route(uri, methods=["POST"])
def create_task():
    if not request.json:
        abort(404)
    task = {
        "id": len(tasks) + 1,
        "name": request.json["name"],
        "check": False,
        "creado": datetime.datetime.now(),
    }
    tasks.append(task)
    return jsonify({"tasks": tasks}), 201


@app.route(uri + "<int:task_id>", methods=["PUT"])
def update_task(task_id):
    if not request.json:
        abort(400)

    this_task = [task for task in tasks if task["id"] == task_id]

    if not this_task:
        abort(404)

    if "name" in request.json and type(request.json.get("name")) is not str:
        abort(400)

    if "check" in request.json and type(request.json.get("check")) is not bool:
        abort(400)

    this_task[0]["name"] = request.json.get("name", this_task[0]["name"])
    this_task[0]["check"] = request.json.get("check", this_task[0]["check"])

    this_task[0].update({"modificado": datetime.datetime.now()})

    return jsonify({"task": this_task[0]}), 201


@app.route(uri + "<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
    this_task = [task for task in tasks if task["id"] == task_id]

    if not this_task:
        abort(404)

    tasks.remove(this_task[0])
    return jsonify({"result": True})


with open("json_data.json", "w") as outfile:
    json.dump(tasks, outfile, indent=4, sort_keys=True, default=str)

if __name__ == "__main__":
    app.run(debug=True)
