from bottle import route, run, template
import os


@route('/hello/<name>')
def index(name):
    return template('<b>Hello {{name}}</b>!', name=name)


if os.environ.get('APP_LOCATION') == 'heroku':
    run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
else:
    run(host='localhost', port=8080, debug=True)
