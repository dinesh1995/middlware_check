from flask import Flask, jsonify, request
from datetime import datetime, timedelta
import requests
import pdb
import json
import uuid
from flask_bcrypt import Bcrypt

app = Flask(__name__)
bcrypt = Bcrypt(app)


def get_auth_token():
	auth_url = "https://04f17b24-94cd-447b-82ef-1b391e99778e-us-east1.apps.astra.datastax.com/api/rest/v1/auth"
	auth_headers = {'Content-type': 'application/json'}
	auth_data = {"username":"dinesh","password":"test1234"}
	response = requests.post(auth_url, headers=auth_headers, json=auth_data)
	return response.json()['authToken']

# Create Patient (User Singup)
# {
# 	"name": "Patient5",
# 	"email": "patient5@test.com",
# 	"password": "test1234",
# 	"phone_number": "123456789",
# 	"age": 40,
# 	"gender": "Female",
# 	"profession": "Test",
# 	"city": "India",
# 	"patient_details": [{
# 			"key":"Have you ever suffered from suicidal thoughts?",
# 			"value":"No"
# 		},{ "key":"Are you suffering from panic attack",
# 			"value":"Sometimes"
# 		},{	"key":"Are you spiritual",
# 			"value":"Yes"
#		},{
# 			"key":"Is your financial condition bothering you?",
# 			"value":"Yes it does"	
# 		}
# 	]
# }
@app.route('/api/users/patient', methods=['POST'])
def create_patient():
	request.json['id'] = str(uuid.uuid1())
	request.json['type'] = "patient"
	request.json['password'] = bcrypt.generate_password_hash(request.json['password']).decode("utf-8")
	patient_url = "https://04f17b24-94cd-447b-82ef-1b391e99778e-us-east1.apps.astra.datastax.com/api/rest/v2/keyspaces/healthapp_keyspace/users"
	headers = {'Content-type': 'application/json','x-cassandra-token': get_auth_token()}
	response = requests.post(patient_url, headers=headers, json=request.json).json()
	patient_url = "https://04f17b24-94cd-447b-82ef-1b391e99778e-us-east1.apps.astra.datastax.com/api/rest/v2/keyspaces/healthapp_keyspace/users/" + response['id']
	headers = {'Content-type': 'application/json','x-cassandra-token': get_auth_token()}
	response = requests.get(patient_url, headers=headers).json()
	del response['data'][0]['doctor_details']
	return response

# Update patient - Sample payload
# {
# 	"name":"patient edited"
# }
@app.route('/api/users/patient/<user_id>', methods=['PUT'])
def update_patient(user_id):
	patient_url = "https://04f17b24-94cd-447b-82ef-1b391e99778e-us-east1.apps.astra.datastax.com/api/rest/v2/keyspaces/healthapp_keyspace/users/" + user_id
	headers = {'Content-type': 'application/json','x-cassandra-token': get_auth_token()}
	response = requests.patch(patient_url, headers=headers, json=request.json).json()
	patient_url = "https://04f17b24-94cd-447b-82ef-1b391e99778e-us-east1.apps.astra.datastax.com/api/rest/v2/keyspaces/healthapp_keyspace/users/" + user_id
	headers = {'Content-type': 'application/json','x-cassandra-token': get_auth_token()}
	response = requests.get(patient_url, headers=headers).json()
	del response['data'][0]['doctor_details']
	return response

# Create Doctor (Will be added by admin)
# {
# 	"name": "Doctor1",
# 	"email": "doctor1@test.com",
# 	"password": "test1234",
# 	"phone_number": "123456789",
# 	"age": 40,
# 	"gender": "Male",
# 	"profession": "Test",
# 	"city": "India",
# 	"doctor_details": [{
# 			"key":"Specialization",
# 			"value":"Phyciatrist"
# 		},{
# 			"key":"Experience",
# 			"value":"10 years"	
# 		}
# 	]
# }
@app.route('/api/users/doctor', methods=['POST'])
def create_doctor():
	request.json['id'] = str(uuid.uuid1())
	request.json['type'] = "doctor"
	request.json['password'] = bcrypt.generate_password_hash(request.json['password']).decode("utf-8")
	doctor_url = "https://04f17b24-94cd-447b-82ef-1b391e99778e-us-east1.apps.astra.datastax.com/api/rest/v2/keyspaces/healthapp_keyspace/users"
	headers = {'Content-type': 'application/json','x-cassandra-token': get_auth_token()}
	response = requests.post(doctor_url, headers=headers, json=request.json).json()
	doctor_url = "https://04f17b24-94cd-447b-82ef-1b391e99778e-us-east1.apps.astra.datastax.com/api/rest/v2/keyspaces/healthapp_keyspace/users/" + response['id']
	headers = {'Content-type': 'application/json','x-cassandra-token': get_auth_token()}
	response = requests.get(doctor_url, headers=headers).json()
	del response['data'][0]['patient_details']
	return response

# Update doctor - Sample payload
# {
# 	"name":"doctor edited"
# }
@app.route('/api/users/doctor/<user_id>', methods=['PUT'])
def update_doctor(user_id):
	doctor_url = "https://04f17b24-94cd-447b-82ef-1b391e99778e-us-east1.apps.astra.datastax.com/api/rest/v2/keyspaces/healthapp_keyspace/users/" + user_id
	headers = {'Content-type': 'application/json','x-cassandra-token': get_auth_token()}
	response = requests.patch(doctor_url, headers=headers, json=request.json).json()
	doctor_url = "https://04f17b24-94cd-447b-82ef-1b391e99778e-us-east1.apps.astra.datastax.com/api/rest/v2/keyspaces/healthapp_keyspace/users/" + user_id
	headers = {'Content-type': 'application/json','x-cassandra-token': get_auth_token()}
	response = requests.get(doctor_url, headers=headers).json()
	del response['data'][0]['patient_details']
	return response

# View all users
@app.route('/api/users')
def users():
	users_url = "https://04f17b24-94cd-447b-82ef-1b391e99778e-us-east1.apps.astra.datastax.com/api/rest/v1/keyspaces/healthapp_keyspace/tables/users/rows"
	headers = {'Content-type': 'application/json','x-cassandra-token': get_auth_token()}
	response = requests.get(users_url, headers=headers).json()
	for index, data in enumerate(response['rows']):
		if data['type'] == "patient":
			del response['rows'][index]['doctor_details']
		else:
			del response['rows'][index]['patient_details']
	return response

# View single user - Can be patient or doctor
@app.route('/api/user/<user_id>')
def view_user(user_id):
	users_url = "https://04f17b24-94cd-447b-82ef-1b391e99778e-us-east1.apps.astra.datastax.com/api/rest/v2/keyspaces/healthapp_keyspace/users/" + user_id
	headers = {'Content-type': 'application/json','x-cassandra-token': get_auth_token()}
	response = requests.get(users_url, headers=headers).json()
	if response['data'][0]['type'] == "patient":
		del response['data'][0]['doctor_details']
	else:
		del response['data'][0]['patient_details']
	return response

# View All Doctors
@app.route('/api/users/doctors', methods=['GET'])
def doctors():
	find_doctors_url = "https://04f17b24-94cd-447b-82ef-1b391e99778e-us-east1.apps.astra.datastax.com/api/rest/v2/keyspaces/healthapp_keyspace/users"
	query_data = {'type': {'$eq': "doctor"}}
	headers = {'Content-type': 'application/json','x-cassandra-token': get_auth_token()}
	response = requests.get(find_doctors_url, headers=headers, params={'where':json.dumps(query_data)}).json()
	for index, data in enumerate(response['data']):
		del response['data'][index]['patient_details']
	return response

# View All Patients
@app.route('/api/users/patients', methods=['GET'])
def patients():
	find_patients_url = "https://04f17b24-94cd-447b-82ef-1b391e99778e-us-east1.apps.astra.datastax.com/api/rest/v2/keyspaces/healthapp_keyspace/users"
	query_data = {'type': {'$eq': "patient"}}
	headers = {'Content-type': 'application/json','x-cassandra-token': get_auth_token()}
	response = requests.get(find_patients_url, headers=headers, params={'where':json.dumps(query_data)}).json()
	for index, data in enumerate(response['data']):
		del response['data'][index]['doctor_details']
	return response


# Login User - Both patient and doctor
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
		if bcrypt.check_password_hash(response['data'][0]['password'],user_password):
			user_url = "https://04f17b24-94cd-447b-82ef-1b391e99778e-us-east1.apps.astra.datastax.com/api/rest/v2/keyspaces/healthapp_keyspace/users/" + response['data'][0]['id']
			headers = {'Content-type': 'application/json','x-cassandra-token': get_auth_token()}
			response = requests.get(user_url, headers=headers).json()
			if response['data'][0]['type'] == "patient":
				del response['data'][0]['doctor_details']
			else:
				del response['data'][0]['patient_details']
			response['data'][0]['success'] = 'Valid user'
			return response['data'][0], 200
		else:
			return {"error":"Password is wrong"}, 403
	else:
		return {"error":"Email not found"}, 403


# Book Appointments - Sample payload
# {
# 	"patient_id": "f7b7efe1-765a-44f5-a125-87afac0cdc4e",
# 	"doctor_id": "27e50a8c-03eb-4cb3-a3c2-74cea7faa84a",
# 	"start_time": "2021-01-04T18:25:43Z",
# 	"end_time": "2021-01-04T19:25:43Z"
# }
@app.route('/api/book_appointment', methods=['POST'])
def book_appointment():
	request.json['id'] = str(uuid.uuid1())
	appointments_url = "https://04f17b24-94cd-447b-82ef-1b391e99778e-us-east1.apps.astra.datastax.com/api/rest/v2/keyspaces/healthapp_keyspace/appointments"
	headers = {'Content-type': 'application/json','x-cassandra-token': get_auth_token()}
	response = requests.post(appointments_url, headers=headers, json=request.json).json()
	appointments_url = "https://04f17b24-94cd-447b-82ef-1b391e99778e-us-east1.apps.astra.datastax.com/api/rest/v2/keyspaces/healthapp_keyspace/appointments/" + response['id']
	headers = {'Content-type': 'application/json','x-cassandra-token': get_auth_token()}
	response = requests.get(appointments_url, headers=headers).json()
	response['data'][0]['start_time'] = (datetime.fromtimestamp(response['data'][0]['start_time']['epochSecond']) - timedelta(hours=5, minutes=30)).strftime('%Y-%m-%dT%H:%M:%SZ')
	response['data'][0]['end_time'] = (datetime.fromtimestamp(response['data'][0]['end_time']['epochSecond']) - timedelta(hours=5, minutes=30)).strftime('%Y-%m-%dT%H:%M:%SZ')
	response['success'] = 'Appointment created successfully'
	return response

# View Appointments of a doctor
@app.route('/api/view_appointment/doctor/<user_id>', methods=['GET'])
def view_appointment_doctor(user_id):
	appointments_url = "https://04f17b24-94cd-447b-82ef-1b391e99778e-us-east1.apps.astra.datastax.com/api/rest/v2/keyspaces/healthapp_keyspace/appointments"
	query_data = {'doctor_id': {'$eq': user_id}}
	headers = {'Content-type': 'application/json','x-cassandra-token': get_auth_token()}
	response = requests.get(appointments_url, headers=headers, params={'where':json.dumps(query_data)}).json()
	return response

# View Appointments of a patient
@app.route('/api/view_appointment/patient/<user_id>', methods=['GET'])
def view_appointment_patient(user_id):
	appointments_url = "https://04f17b24-94cd-447b-82ef-1b391e99778e-us-east1.apps.astra.datastax.com/api/rest/v2/keyspaces/healthapp_keyspace/appointments"
	query_data = {'patient_id': {'$eq': user_id}}
	headers = {'Content-type': 'application/json','x-cassandra-token': get_auth_token()}
	response = requests.get(appointments_url, headers=headers, params={'where':json.dumps(query_data)}).json()
	return response

# Delete Appointments
@app.route('/api/delete_appointment/<id>', methods=['DELETE'])
def delete_appointment(id):
	appointments_url = "https://04f17b24-94cd-447b-82ef-1b391e99778e-us-east1.apps.astra.datastax.com/api/rest/v2/keyspaces/healthapp_keyspace/appointments/"+id
	headers = {'Content-type': 'application/json','x-cassandra-token': get_auth_token()}
	response = requests.delete(appointments_url, headers=headers)
	if response.status_code == 204:
		return {"success":"Appointment deleted"}, 204
	else:
		return {"error":"Error in deleting appointment"}, 500


# Add medicine - Sample payload
# {
# 	"name" : "BP Tablet",
# 	"patient_id": "f7b7efe1-765a-44f5-a125-87afac0cdc4e",
# 	"doctor_id": "27e50a8c-03eb-4cb3-a3c2-74cea7faa84a",
#	"quantity": "1",
# 	"intake_day_time": ["Mon-21:00","Tue-21:00","Thur-12:00","Fri-12:00"]
# }
@app.route('/api/add_medicine', methods=['POST'])
def add_medicine():
	request.json['id'] = str(uuid.uuid1())
	medicines_url = "https://04f17b24-94cd-447b-82ef-1b391e99778e-us-east1.apps.astra.datastax.com/api/rest/v2/keyspaces/healthapp_keyspace/medicines"
	headers = {'Content-type': 'application/json','x-cassandra-token': get_auth_token()}
	response = requests.post(medicines_url, headers=headers, json=request.json).json()
	return response

# View all medicines of a patient
@app.route('/api/medicines/patient/<user_id>', methods=['GET'])
def view_medicines_patient(user_id):
	medicines_url = "https://04f17b24-94cd-447b-82ef-1b391e99778e-us-east1.apps.astra.datastax.com/api/rest/v2/keyspaces/healthapp_keyspace/medicines"
	query_data = {'patient_id': {'$eq': user_id}}
	headers = {'Content-type': 'application/json','x-cassandra-token': get_auth_token()}
	response = requests.get(medicines_url, headers=headers, params={'where':json.dumps(query_data)}).json()
	return response

# View medicines of a patient at specific day and time - Sample payload
# GET - http://127.0.0.1:5000/api/medicines/patient/f7b7efe1-765a-44f5-a125-87afac0cdc4e/notify?day_time=Mon-21:00
@app.route('/api/medicines/patient/<user_id>/notify', methods=['GET'])
def view_medicines_patient_notify(user_id):
	day_time = request.args['day_time']
	medicines_url = "https://04f17b24-94cd-447b-82ef-1b391e99778e-us-east1.apps.astra.datastax.com/api/rest/v2/keyspaces/healthapp_keyspace/medicines"
	#query_data = {'patient_id': {'$eq': user_id}, 'intake_day_time': {'$contains':day_time}}
	query_data = {'patient_id': {'$eq': user_id}}
	headers = {'Content-type': 'application/json','x-cassandra-token': get_auth_token()}
	response = requests.get(medicines_url, headers=headers, params={'where':json.dumps(query_data)}).json()
	notify = {"notify" : []}
	if response["data"]:
		for data in response["data"]:
			if day_time in data['intake_day_time']:
				notify["notify"].append({"name":data["name"],"quantity":data["quantity"],"day_time":day_time})
	return notify, 200


if __name__ == "__main__":
    app.run(port=5000)
