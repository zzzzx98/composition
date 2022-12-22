from flask import Flask, Response, request
from flask_cors import CORS
import json
import requests
import rest_utils
from qualifying_resource import F1
from formula1_resource import Formula1Resource
from typing import *

app = Flask(__name__)
CORS(app)



USR_ADDR_PROPS = {
    'microservice': 'qualifying',
    # 'api': 'http://ec2-18-117-241-244.us-east-2.compute.amazonaws.com:5000/api/users',
    'api': 'http://192.168.0.82:5011/f1/qualifying/',
    'required': set(),
    'fields': ('qualifyId', 'raceId', 'driverId', 'constructorId', 'number', 'position', 'q1','q2','q3')
}
USR_PREF_PROPS = {
    'microservice': 'circuits',
    # 'api': 'http://ec2-3-145-83-228.us-east-2.compute.amazonaws.com:5000/api/profile',
    'api': 'http://192.168.0.82:5012/api/circuits/',
    'required': set(),
    'fields': ('circuitRef','name', 'location', 'country', 'lat', 'lng', 'alt', 'url')
}

USR_STUDENT = {
    'microservice': 'students',
    # 'api': 'http://ec2-3-145-83-228.us-east-2.compute.amazonaws.com:5000/api/profile',
    'api': 'http://54.89.81.97:5014/api/students/',
    'required': set(),
    'fields': ('auto_id', 'last_name', 'first_name', 'middle_name', 'email', 'uni', 'address_line1', 'address_line2','city','state')
}
PROPS = (USR_ADDR_PROPS, USR_PREF_PROPS,USR_STUDENT)


def project_req_data(req_data: dict, props: tuple, required_props: set) -> dict:
    res = dict()
    for prop in props:
        if prop in req_data:
            res[prop] = req_data[prop]
        else:
            if len(required_props) and prop in required_props:
                return None
    return res

def get_information(id):
    futures = []
    i = 0
    for props in (USR_ADDR_PROPS, USR_PREF_PROPS,USR_STUDENT):
        if id[i] == "None":
            i += 1
            futures.append("nothing")
            continue
        print(props['api'] + str(id[i]))
        res = requests.get(props['api'] + str(id[i]))
        futures.append(res)
        i += 1
    temp = ""
    flag = 1
    code = 0
    for i, future in enumerate(futures):
        microservice = PROPS[min(i, 2)]['microservice']
        res = future
        if id[i] == "None":
            temp += f"{microservice} did nothing."
            continue
        if res is None:
            return 408, temp + f"{microservice} did not response."
        elif not res.ok:
            flag = 0
            code = res.status_code
            temp += f"{microservice} query information failed." + "\n"
        else:
            temp += f"{microservice} query information successfully." + "\n" + str(res.json()) + "\n"
    if flag == 1:
        return 200, temp
    else:
        return code, temp

def create_microservices(req_data: dict,
                                id,
                                headers: Dict) -> (int, str):
    futures = []
    i = 0
    for props in (USR_ADDR_PROPS, USR_PREF_PROPS,USR_STUDENT):
        if id[i] == "None":
            i += 1
            futures.append("nothing")
            continue
        data = project_req_data(req_data, props['fields'], set())   # params in PUT requests are optional
        if len(data) == 0:
            return 400, f"Missing data field(s) for {props['microservice']}"
        print(props['api'] + str(id[i]))
        print(data)
        futures.append(
            requests.put(props['api'] + str(id[i]),
                     data=json.dumps(data),
                     headers=headers))
        i += 1
    print(futures)
    temp = ""
    flag = 1
    code = 0
    for i, future in enumerate(futures):
        microservice = PROPS[min(i, 2)]['microservice']
        res = future
        print(future.json())
        if id[i] == "None":
            temp += f"{microservice} did nothing."
            continue
        if res is None:
            return 408, temp + f"{microservice} did not response."
        elif not res.ok:
            flag = 0
            code = res.status_code
            temp += f"{microservice} insert failed." + "\n"
        else:
            temp += f"{microservice} insert successfully." + "\n"
    if flag == 1:
        return 200, "User info insert successfully!"
    else:
        return code, temp

def update_information(req_data: dict,
                                id,
                                headers: Dict) -> (int, str):
    futures = []
    i = 0
    for props in (USR_ADDR_PROPS, USR_PREF_PROPS,USR_STUDENT):
        if id[i] == "None":
            i += 1
            futures.append("nothing")
            continue
        data = project_req_data(req_data, props['fields'], set())   # params in PUT requests are optional
        print(props['api'] + str(id[i]))
        print(data)
        if len(data) == 0:
            return 400, f"Missing data field(s) for {props['microservice']}"

        futures.append(
            requests.post(props['api'] + str(id[i]),
                     data=json.dumps(data),
                          headers=headers))
        i += 1
    print(futures)
    temp = ""
    flag = 1
    code = 0
    for i, future in enumerate(futures):
        microservice = PROPS[min(i, 2)]['microservice']
        res = future
        if id[i] == "None":
            temp += f"{microservice} did nothing."
            continue
        if res is None:
            return 408, temp + f"{microservice} did not response."
        elif not res.ok:
            flag = 0
            code = res.status_code
            temp += f"{microservice} update failed." + "\n"
        else:
            temp += f"{microservice} update successfully." + "\n"
    if flag == 1:
        return 200, temp
    else:
        return code, temp

def delete_information(id):
    futures = []
    i = 0
    for props in (USR_ADDR_PROPS, USR_PREF_PROPS,USR_STUDENT):
        if id[i] == "None":
            i += 1
            futures.append("nothing")
            continue
        res = requests.delete(props['api'] + str(id[i]))
        futures.append(res)
        i += 1
    temp = ""
    flag = 1
    code = 0
    for i, future in enumerate(futures):
        microservice = PROPS[min(i, 2)]['microservice']
        res = future
        if id[i] == "None":
            temp += f"{microservice} did nothing."
            continue
        if res is None:
            return 408, temp + f"{microservice} did not response."
        elif not res.ok:
            flag = 0
            code = res.status_code
            temp += f"{microservice} delete information failed." + "\n"
        else:
            temp += f"{microservice} delete information successfully." + "\n" + str(res.json()) + "\n"
    if flag == 1:
        return 200, temp
    else:
        return code, temp

@app.route('/api/composition/<id_1>/<id_2>/<id_3>', methods=['GET','PUT','POST','DELETE'])
def composition(id_1,id_2,id_3):
    request_inputs = rest_utils.RESTContext(request)
    id = [id_1, id_2,id_3]
    print(id)
    if request_inputs.method == "PUT":
        req_data = request.get_json()
        status_code, message = create_microservices(req_data, id, request.headers)
        return Response(f"{status_code} - {message}", status=status_code, mimetype="application/json")

    elif request_inputs.method == "GET":
        status_code, message = get_information(id)
        return Response(f"{status_code} - {message}", status=status_code, mimetype="application/json")

    elif request_inputs.method == "POST":
        req_data = request.get_json()
        status_code, message = update_information(req_data,id,request.headers)
        return Response(f"{status_code} - {message}", status=status_code, mimetype="application/json")
    elif request_inputs.method == "DELETE":
        status_code, message = delete_information(id)
        return Response(f"{status_code} - {message}", status=status_code, mimetype="application/json")
if __name__ == "__main__":
    app.run(host="192.168.0.82", port=5015)