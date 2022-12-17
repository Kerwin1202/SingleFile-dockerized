import subprocess
from flask import Flask, request, Response, jsonify, render_template
import os
from urllib.parse import urljoin

server = Flask(__name__, template_folder='/opt/app')

SINGLEFILE_EXECUTABLE = '/node_modules/single-file/cli/single-file'
BROWSER_PATH = '/opt/google/chrome/google-chrome'
BROWSER_ARGS = '["--no-sandbox"]'

BASE_DIR = './htmls'


def get_html_path(key, name):
    return f'{BASE_DIR}/{key}/{name}.html'


@server.route('/dl/<key>/<name>.html')
def show_html(key, name):
    return render_template(get_html_path(key, name))


@server.route('/', methods=['GET'])
def singlefile():
    print(request.url)
    url = request.args.get('url')
    key = request.args.get('key')
    name = request.args.get('name')
    refresh = request.args.get('refresh', False)
    if key and name and not refresh and os.path.exists(get_html_path(key, name)):
        response = {'url': urljoin(request.base_url, f'/dl/{key}/{name}.html')}
        return jsonify(response)

    if url:
        p = subprocess.Popen([
            SINGLEFILE_EXECUTABLE,
            '--browser-executable-path=' + BROWSER_PATH,
            "--browser-args='%s'" % BROWSER_ARGS,
            url,
            '--dump-content',
        ],
            stdout=subprocess.PIPE)
    else:
        return Response('Error: url parameter not found.',
                        status=500)
    singlefile_html = p.stdout.read()

    key = request.args.get('key')
    name = request.args.get('name')
    if key and name:
        folder_path = f'{BASE_DIR}/{key}'
        if not os.path.exists(folder_path):
            os.mkdir(folder_path)
        with open(get_html_path(key, name), 'wb') as f:
            f.write(singlefile_html)
        response = {'url': urljoin(request.base_url, f'/dl/{key}/{name}.html')}
        return jsonify(response)
    else:
        return Response(
            singlefile_html,
            mimetype="text/html",
        )


if __name__ == '__main__':
    server.run(host='0.0.0.0', port=80)
