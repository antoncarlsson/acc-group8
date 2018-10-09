from flask import Flask, request, abort

app = Flask(__name__)

@app.route('/qtlaas/start')
def start():
    return 'TODO: Start QLTaaS'

@app.route('/qtlaas/stop')
def stop():
    return 'TODO: Stop QTLaaS'

@app.route('/qtlaas/workers')
def number_of_workers():
    return 'TODO: Return number of workers'

@app.route('/qtlaas/workers/<int:no_workers>', methods=['POST', 'DELETE'])
def add_workers(no_workers):
    if no_workers < 1:
        abort(400, 'Too few workers to be added/removed.')
    else: 
        if request.method == 'POST':
            return 'TODO: Add workers'
        else: # DELETE
            return 'TODO: Remove workers'


if __name__=='__main__':
    app.run(host='0.0.0.0', debug=True)