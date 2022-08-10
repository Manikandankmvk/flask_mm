from urllib import response
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, request, Response, jsonify, abort
from flask.views import View
from flask.views import MethodView
from my_app.middleware import HTTPMethodOverrideMiddleware
from werkzeug.exceptions import HTTPException


# from my_app.models import Hero
app = Flask(__name__)
# app.wsgi_app = HTTPMethodOverrideMiddleware(app.wsgi_app)a

# app.config.from_object(os.environ['APP_SETTINGS'])
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost:5432/flask_db'
db = SQLAlchemy(app)
class Hero(db.Model):
    heroname = db.Column(db.String(255), primary_key=True)
    email = db.Column(db.String)

class Hello(View):
    methods = ['GET', 'POST']
    def dispatch_request(self):
        response_data = {}
        if request.method == 'POST':
            uname = request.json.get('heroname', ' ')
            email = request.json.get('email', ' ')
            if uname and email:
                try:
                    user_data = Hero(heroname=uname, email=email)
                    db.session.add(user_data)
                    db.session.commit()
                    response_data['message'] ='Created Successfully'
                    return Response(response_data['message'], status=200, mimetype='application/json')
                except:
                    response_data['message'] = 'Heroname already exists'
                    response_data['status'] = 400
                    return Response(response_data['message'], status=400, mimetype='application/json')
                    # return Response(jsonify(response_data))
        elif request.method == 'GET':
            uname = request.form.get('username')
            data = Hero.query.filter_by(heroname=uname).first_or_404()
            # l = {}
            # for i in data:
            #     l[i.heroname] = i.email
            # response_data = {'message' : 'Fetched Successfully',
            #                 'status' : 'success',
            #                 'data' : data
            #             }
            return jsonify(data.email)

app.add_url_rule("/hello/", view_func=Hello.as_view(name='hello'))

if __name__ == '__main__':
    app.run(debug=True)


