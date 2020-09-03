from flask import Flask, render_template, request, redirect
import os

app = Flask(__name__)

methods_counter = {'GET': 0,
                   'POST': 0,
                   'PUT': 0,
                   'DELETE': 0}

current_dir = os.path.dirname(os.path.realpath(__file__))
txt_file = os.path.join(current_dir, "request_counts.txt")


def load_file_to_dict():
    if os.path.isfile(txt_file):
        with open(txt_file, 'r') as line_txt:
            methods = line_txt.read()
            method = methods.strip().split(' ')
            for data in method:
                data_split = data.strip().split(':')
                key, value = data_split
                methods_counter[key] = int(value)


load_file_to_dict()


def reset_methods_counter_dict():
    global methods_counter
    methods_counter = dict.fromkeys(methods_counter.keys(), 0)


def increase_by_1_get():
    methods_counter['GET'] += 1


def increase_by_1_post():
    methods_counter['POST'] += 1


def increase_by_1_put():
    methods_counter['PUT'] += 1


def increase_by_1_delete():
    methods_counter['DELETE'] += 1


def execute_put():
    os.system("curl -X PUT http://localhost:5000/request-counter")


def execute_delete():
    os.system("curl -X DELETE http://localhost:5000/request-counter")


def save_file():
    data_line = ""
    for key, value in methods_counter.items():
        data_line += f'{key}:{value} '
    with open(txt_file, 'w') as line_txt:
        line_txt.write(data_line.strip())


@app.route('/')
def main_page():
    return render_template('index.html', count_get=methods_counter['GET'], count_post=methods_counter['POST'],
                           count_put=methods_counter['PUT'], count_delete=methods_counter['DELETE'])


@app.route('/put')
def put():
    execute_put()
    return render_template('index.html', count_get=methods_counter['GET'], count_post=methods_counter['POST'],
                           count_put=methods_counter['PUT'], count_delete=methods_counter['DELETE'])


@app.route('/delete')
def delete():
    execute_delete()
    return render_template('index.html', count_get=methods_counter['GET'], count_post=methods_counter['POST'],
                           count_put=methods_counter['PUT'], count_delete=methods_counter['DELETE'])


@app.route('/request-counter', methods=['GET', 'POST', 'PUT', 'DELETE'])
def request_counter():
    if request.method == 'GET':
        increase_by_1_get()
        save_file()
        return redirect('/')
    elif request.method == 'POST':
        increase_by_1_post()
        save_file()
        return redirect('/')
    elif request.method == 'PUT':
        increase_by_1_put()
        save_file()
        return redirect('/')
    elif request.method == 'DELETE':
        increase_by_1_delete()
        save_file()
        return redirect('/')
    else:
        info = "There is no such request!!!"
        return render_template('request-counter.html', error=info)


@app.route('/statistics')
def statistics():
    return render_template('statistics.html', methods_dict=methods_counter)


@app.route('/reset_data')
def reset_data():
    if os.path.isfile(txt_file):
        os.remove(txt_file)
        reset_methods_counter_dict()
        return redirect('/')
    else:
        info = "There is no data to reset!!!"
        return render_template('request-counter.html', error=info)


if __name__ == '__main__':
    app.run()
