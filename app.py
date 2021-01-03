from flask import Flask, jsonify, request
from datetime import datetime
import requests
import pdb
import json
import uuid

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
	users_url = "https://04f17b24-94cd-447b-82ef-1b391e99778e-us-east1.apps.astra.datastax.com/api/rest/v1/keyspaces/healthapp_keyspace/tables/users/rows"
	headers = {'Content-type': 'application/json','x-cassandra-token': get_auth_token()}
	response = requests.get(users_url, headers=headers).json()
	return response


# Login User - Sample payload
# {
# 	"email":"test1@test.com",
# 	"password":"test1234"
# }
@app.route('/api/users/login', methods=['POST'])
def users_login():
	user_email = request.json['email']
	user_password = request.json['password']
	find_user_url = "https://04f17b24-94cd-447b-82ef-1b391e99778e-us-east1.apps.astra.datastax.com/api/rest/v2/keyspaces/healthapp_keyspace/users"
	query_data = {'email': {'$eq': user_email}}
	headers = {'Content-type': 'application/json','x-cassandra-token': get_auth_token()}
	response = requests.get(find_user_url, headers=headers, params={'where':json.dumps(query_data)}).json()
	if response['count'] == 1:
		if response['data'][0]['password'] == user_password:
			return {"success":"valid user"}, 200
		else:
			return {"error":"Password is wrong"}, 403
	else:
		return {"error":"Email not found"}, 403


# View Doctors
@app.route('/api/users/doctors', methods=['GET'])
def docters():
	find_doctors_url = "https://04f17b24-94cd-447b-82ef-1b391e99778e-us-east1.apps.astra.datastax.com/api/rest/v2/keyspaces/healthapp_keyspace/users"
	query_data = {'type': {'$eq': 1}}
	headers = {'Content-type': 'application/json','x-cassandra-token': get_auth_token()}
	response = requests.get(find_doctors_url, headers=headers, params={'where':json.dumps(query_data)}).json()
	return response


# View Patients
@app.route('/api/users/patients', methods=['GET'])
def patients():
	find_patients_url = "https://04f17b24-94cd-447b-82ef-1b391e99778e-us-east1.apps.astra.datastax.com/api/rest/v2/keyspaces/healthapp_keyspace/users"
	query_data = {'type': {'$eq': 0}}
	headers = {'Content-type': 'application/json','x-cassandra-token': get_auth_token()}
	response = requests.get(find_patients_url, headers=headers, params={'where':json.dumps(query_data)}).json()
	return response


# Book Appointments - Sample payload
# {
# 	"patient_id": "f7b7efe1-765a-44f5-a125-87afac0cdc4e",
# 	"doctor_id": "27e50a8c-03eb-4cb3-a3c2-74cea7faa84a",
# 	"start_time": 1299038700000,
# 	"end_time": 1299038700000
# }
@app.route('/api/book_appointment', methods=['POST'])
def book_appointment():
	request.json['id'] = str(uuid.uuid1())
	appointments_url = "https://04f17b24-94cd-447b-82ef-1b391e99778e-us-east1.apps.astra.datastax.com/api/rest/v2/keyspaces/healthapp_keyspace/appointments"
	headers = {'Content-type': 'application/json','x-cassandra-token': get_auth_token()}
	response = requests.post(appointments_url, headers=headers, json=request.json).json()
	return response


if __name__ == "__main__":
    app.run(port=5000)
