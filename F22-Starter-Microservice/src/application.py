from flask import Flask, Response, request, render_template
from datetime import datetime
import json
from columbia_student_resource import ColumbiaStudentResource
from qualifying_resource import F1
from flask_cors import CORS
import rest_utils
# Create the Flask application object.
app = Flask(__name__,
            static_url_path='/',
            static_folder='static/class-ui/',
            template_folder='web/templates')

CORS(app)

# @app.route('/')
# def Home():
#     return render_template('../../front-end/template/Home.html')
@app.route('/')
def hello_world():
    return '<u>Hello World!</u>'

# @app.route("/f1/qualifying/add/")
# def ad():
#     return render_template('../../front-end/template/add.html')

# @app.route("/f1/<qualifyId>", methods = ['GET'])
# def qualifying(qualifyId):
#     q = F1.get_qualifying(qualifyId)
#     if q:
#         rsp = Response(json.dumps(q), status=200, content_type="application/json")
#     else:
#         rsp = Response(json.dumps(q), status=404, content_type="text/plain")
#     return rsp
#
#
# @app.route("/f1/qualifying/add", methods = ['POST'])
# def add_qualify(qualifyId,raceId,driverId,constructorId,number,position,q1,q2,q3):
#     # qualifyId = request.form.get('qualifyId')
#     # raceId = request.form.get('raceId')
#     # driverId = request.form.get('driverId')
#     # constructorId = request.form.get('constructorId')
#     # number = request.form.get('number')
#     # position = request.form.get('position')
#     # q1 = request.form.get('q1')
#     # q2 = request.form.get('q2')
#     # q3 = request.form.get('q3')
#     res = F1.append_new_qualifying(qualifyId, raceId, driverId, constructorId, number, position, q1, q2, q3)
#     if res:
#         return '<script> alert("Fail to add data");location.href = "/";</script>'
#     else:
#         return '<script> alert("Success");location.hred = "/";</script>'
#
#
# @app.route('/f1/qualifying/update')
# def update():
#     return render_template('PUT.html')
# @app.route('/f1/qualifying/update/<qualifyId>/<driverId>', methods = ['GET'])
# def update_qualify(qualifyId, driverId):
#     # qualifyId = request.form.get('qualifyId')
#     # driverId = request.form.get('driverId')
#     res = F1.update_qualifying(qualifyId, driverId)
#     if res:
#         return '<script> alert("Fail to update data");location.href = "/";</script>'
#     else:
#         return '<script> alert("Success");location.hred = "/";</script>'


@app.route('/f1/qualifying/<qualifyId>', methods = ['GET','PUT','DELETE','POST'])
def delete_qualify(qualifyId):

    #print(F1)
    request_inputs = rest_utils.RESTContext(request, qualifyId)
    F2 = F1()
    print(qualifyId)
    if request_inputs.method == "GET":
        q = F2.get_qualifying(qualifyId)
        if q:
            rsp = Response(json.dumps(q), status=200, content_type="application/json")
        else:
            rsp = Response(json.dumps(q), status=404, content_type="text/plain")
    elif request_inputs.method == "DELETE":

        res = F2.delete_qualifying(qualifyId)
        rsp = Response(json.dumps(res, default=str), status=200, content_type="application/json")
        # if res:
        #     return '<script> alert("Fail to delete data");location.href = "/";</script>'
        # else:
        #     return '<script> alert("Success");location.hred = "/";</script>'
    elif request_inputs.method == "PUT":
        data = request_inputs.data
        data['qualifyId'] = qualifyId
        print(data)
        res = F2.append_new_qualifying(data)
        rsp = Response(json.dumps(res, default=str), status=200, content_type="application/json")
        #rsp = Response("CREATED", status=201, headers=headers, content_type="text/plain")
    elif request_inputs.method == "POST":
        data = request_inputs.data
        data['qualifyId'] = qualifyId
        res = F2.update_qualifying(data)
        rsp = Response(json.dumps(res, default=str), status=200, content_type="application/json")
    return rsp






# @app.get("/api/health")
# def get_health():
#     t = str(datetime.now())
#     msg = {
#         "name": "F22-Starter-Microservice",
#         "health": "Good",
#         "at time": t
#     }
#
#     # DFF TODO Explain status codes, content type, ... ...
#     result = Response(json.dumps(msg), status=200, content_type="application/json")
#
#     return result


@app.route("/api/students/<uni>", methods=["POST"])
def get_student_by_uni(uni):

    result = ColumbiaStudentResource.get_by_key(uni)

    if result:
        rsp = Response(json.dumps(result), status=200, content_type="application.json")
    else:
        rsp = Response("NOT FOUND", status=404, content_type="text/plain")

    return rsp

if __name__ == "__main__":
    app.run(host="192.168.0.82", port=5011)

