from flask import Flask, jsonify
import requests
import pdb

app = Flask(__name__)


def get_auth_token():
	auth_url = "https://04f17b24-94cd-447b-82ef-1b391e99778e-us-east1.apps.astra.datastax.com/api/rest/v1/auth"
	auth_headers = {'Content-type': 'application/json'}
	auth_data = {"username":"dinesh","password":"test1234"}
	response = requests.post(auth_url, headers=auth_headers, json=auth_data)
	return response.json()['authToken']


# View all users
@app.route('/api/users')
def users():
	global db_token
	users_url = "https://04f17b24-94cd-447b-82ef-1b391e99778e-us-east1.apps.astra.datastax.com/api/rest/v1/keyspaces/healthapp_keyspace/tables/users/rows"
	headers = {'Content-type': 'application/json','x-cassandra-token': get_auth_token()}
	response = requests.get(users_url, headers=headers)
	return response.json()


if __name__ == "__main__":
    app.run(port=5000)
