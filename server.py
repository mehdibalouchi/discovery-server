from flask import Flask, render_template, jsonify
from flask_socketio import SocketIO, emit
from bert_serving.client import BertClient
import numpy as np
import re
from functools import reduce
import time
import asyncio

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

bert_client = BertClient()


def pre_process(tfx):
    return [(cmd_name, cmd['template']) for cmd_name, cmd in tfx['commands'].items()]


def rank(templates, query):
    names = []
    temps = []
    for temp in templates:
        temps.append(temp[1])
        names.append(temp[0])

    temps.append(query)

    embeddings = bert_client.encode(temps)
    query_embedding = embeddings[-1]
    template_embeddings = embeddings[:-1]
    # distances = list(map(lambda tmp: (tmp[0], tmp[1], tmp[2], np.inner(tmp[2], query_embedding)), template_embeddings))
    distances = list(map(lambda p: np.linalg.norm(p - query_embedding), template_embeddings))
    ranked_templates = list(
        map(lambda x: (x[0], x[1]), list(sorted(list(zip(names, temps[:-1], distances)), key=lambda x: x[2], reverse=False ))))

    return ranked_templates


def apply_threshold(ranked_commands):
    return ranked_commands[0]


def extract_args(command, query, tfx):
    command_name = command[0]

    command_args = []
    command_tfx = tfx['commands'][command_name]
    for arg in command_tfx['arguments']:
        print(arg)
        new_command = {}
        command_args.append(new_command)
        regexp_list = tfx['terms'][arg]['regexp']
        for regexp in regexp_list:
            reg = re.compile(regexp)
            match = re.search(reg, query)
            if match:
                for key, value in match.groupdict().items():
                    new_command[key] = value
                continue

    return [command, command_args]


def discover(tfx, query, callback):
    templates = pre_process(tfx)
    ranked_commands = rank(templates, query)
    # print(list(ranked_commands))
    command, args = extract_args(apply_threshold(ranked_commands), query, tfx)
    callback({'command': command, 'params': args})


def generate_result(tfx, query):
    return {
        'command': 'sr',
        'args': {
            'selection': {'name': 'A', 'element': 'column'},
            'order': 'ascending'
        }
    }


@app.route('/')
def index():
    return jsonify({'data': 'Server is up'})


@socketio.on('test connection')
def test_message(message):
    print("Test connection request arrived")
    emit('test ack', {'data': 'ack'})


@socketio.on('discover request')
def discover_request(data):
    print('Discover request arrived')

    # time.sleep(1)

    def callback(result):
        emit('discover response', result)
        print('emmited', result)

    discover(data['tfx'], data['query'], callback)


if __name__ == '__main__':
    socketio.run(app)
