from flask import Flask, jsonify, request
from functools import wraps
from models import Task

app = Flask(__name__)

API_KEY = 'live_oGxvWh0u3mWmMNetq6hSWWWpuxke5PIRehczw2PUWasyi2lKrJV84JbN5XPCu947'

tasks = [
    Task(1, 'Task 1', 'Description 1', False),
    Task(2, 'Task 2', 'Description 2', True)
]

def authenticate(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        provided_key = request.headers.get('Authorization')
        if provided_key == API_KEY:
            return func(*args, **kwargs)
        else:
            return jsonify({'error': 'Unauthorized'}), 401
    return wrapper

@app.route('/tasks', methods=['GET'])
@authenticate
def get_tasks():
    return jsonify([vars(task) for task in tasks])

@app.route('/tasks/<int:task_id>', methods=['GET'])
@authenticate
def get_task(task_id):
    task = next((task for task in tasks if task.id == task_id), None)
    if task:
        return jsonify(vars(task))
    else:
        return jsonify({'error': 'Task not found'}), 404

@app.route('/tasks', methods=['POST'])
@authenticate
def create_task():
    data = request.get_json()
    new_task = Task(len(tasks) + 1, data['title'], data['description'], False)
    tasks.append(new_task)
    return jsonify(vars(new_task)), 201

@app.route('/tasks/<int:task_id>', methods=['PUT'])
@authenticate
def update_task(task_id):
    task = next((task for task in tasks if task.id == task_id), None)
    if task:
        data = request.get_json()
        task.title = data['title']
        task.description = data['description']
        task.completed = data['completed']
        return jsonify(vars(task))
    else:
        return jsonify({'error': 'Task not found'}), 404

@app.route('/tasks/<int:task_id>', methods=['DELETE'])
@authenticate
def delete_task(task_id):
    global tasks
    tasks = [task for task in tasks if task.id != task_id]
    return jsonify({'message': 'Task deleted successfully'})

if __name__ == '__main__':
    app.run(debug=True)
