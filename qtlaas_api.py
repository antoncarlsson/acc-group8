from flask import Flask, request, abort, jsonify, redirect
from keystoneauth1.identity import v3
from keystoneauth1 import session
import heatclient
from heatclient import client as heat_client
from heatclient.common import template_utils
import sys
from getpass import getpass

keystone_settings = {
	'auth_url': 'https://uppmax.cloud.snic.se:5000/v3',
#	'region_name': 'UPPMAX',
	'project_id': '2344cddf33a1412b846290a9fb90b762',
	'project_name': 'SNIC 2018/10-30',
	'user_domain_name': 'snic',
	'username': sys.argv[1],
	'password': getpass('Password: ')
}

keystone_auth = v3.Password(**keystone_settings)
keystone_session = session.Session(auth=keystone_auth)
auth_url = 'https://uppmax.cloud.snic.se:5000/v3'
kwargs = {
    'auth_url': auth_url,
    'session': keystone_session,
    'auth': keystone_auth,
    'service_type': 'orchestration'
}
stack_name = sys.argv[2]
hc = heat_client.Client('1', **kwargs)

app = Flask(__name__)

@app.route('/qtlaas/upload')
def upload_file():
    return 'TODO: inject files through API'

@app.route('/qtlaas/start')
def start():
    template_name = 'Heat_template_start_instance.yml'
    files, template = template_utils.process_template_path(template_name)

    try:
        hc.stacks.create(stack_name=stack_name, template=template, files=files)
        stacks = hc.stacks.list(filters={'stack_name': stack_name})
        stack_id = next(stacks).id
        stack_output = hc.stacks.output_list(stack_id)

        result = {}
        for line in stack_output[1]:
            output_value = line['output_key']
            result[output_value] =  hc.stacks.output_show(stack_id, output_value)

        return jsonify(result)
        # redirect('http://IP.TO.SPARK.MASTER:60060/', 302, jsonify(result))
    except heatclient.exc.HTTPConflict as e:
        abort(400, 'Stack already exists : %s %s' % (e.error, stack_name))
    except heatclient.exc.HTTPBadRequest as e:
        abort(400, 'Bad request : %s' % e.error)


@app.route('/qtlaas/stop')
def stop():
    stack_id = hc.stacks.list(filters={'stack_name': stack_name})
    heatclient.stacks.delete(stack_id)
    return 'Deletion complete'

@app.route('/qtlaas/workers')
def number_of_workers():
    return 'TODO: Return number of workers'

@app.route('/qtlaas/workers/<int:no_workers>', methods=['POST', 'DELETE'])
def resize(no_workers):
    if no_workers < 1:
        abort(400, 'Too few workers to be added/removed.')
    else: 
        if request.method == 'POST':
            return 'TODO: Add workers'
        else: # DELETE
            return 'TODO: Remove workers'


if __name__=='__main__':
    app.run(host='0.0.0.0', debug=True)
