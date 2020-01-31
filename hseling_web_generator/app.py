import json
from flask import Flask
from flask import render_template, request
import requests


RPC_HOST = 'http://hse-api-generator/rpc'

app = Flask(__name__)

AUT_LST = ['azarova', 'hexameter', 'modernism', 'vysotsky']


COORD = {'azarova': 'Наталия Азарова',
    'hexameter': 'Русский гекзаметр',
    'modernism': 'Русский модернизм',
    'vysotsky': 'Владимир Высоцкий'
    }

@app.route('/web/')
def index():
    return render_template('index.html')


@app.route('/web/models/<author>')
def generate(author=None):
    if author:
        if author not in AUT_LST:
            author = 'hexameter'
    else:
        author = 'hexameter'
    info = {
        "method": "get_text",
        "params":{"author": "{}".format(author)},
        "jsonrpc": "2.0",
        "id": 0,
        }
    response = requests.post(RPC_HOST, json=info).json()
    name = COORD[author]
    text = response['result']
    text = text.replace('\n', '<br/>')
    text = text.replace('<br/><br/><br/>', '<br/>')
    text = text.replace('<br/><br/><br/>', '<br/>')
    l_number = AUT_LST.index(author)
    l_nember_arr = ['', '', '', '']
    l_nember_arr[l_number] = ' class="active"'
    return render_template('common.html', name=name, text=text, l1=l_nember_arr[0], l2=l_nember_arr[1], l3=l_nember_arr[2], l4=l_nember_arr[3])


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=80)
