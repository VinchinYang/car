#hints: It can work in python2 and python3

from bottle import run, route, static_file

@route('/')
def index():
    return static_file('template.html', './')

@route('/resource/<filename>')
def staticFile(filename):
    return static_file(filename, './resource')

run(host='192.168.0.107', port='8888')
