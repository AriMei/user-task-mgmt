from flask import Flask, jsonify, request, render_template, make_response, redirect
from flask_restful import Resource, Api
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime as dt

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']="mysql+pymysql://root:@localhost/user_task"
db = SQLAlchemy(app)
api = Api(app)

class Tasks(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    task = db.Column(db.String(256),nullable=False)
    username = db.Column(db.String(100),nullable=False)
    updated_ts = db.Column(db.String(12),nullable=False)

class Home(Resource):
    def get(self):
        task = Tasks.query.all()
        return make_response(render_template('index.html', tasks=task))
    
    def post(self):
        tsk = request.form.get('subject')
        username = 'vivek'
        date = dt.now()
        db.session.add(Tasks(task=tsk,username=username,updated_ts=date))
        db.session.commit()
        return redirect('/')

class Edit(Resource):
    def get(self,id):
        if(id!='0'):
            task = Tasks.query.filter(Tasks.id==id).first()
            return make_response(render_template('edit.html', tasks=task))
        else:
            task = Tasks(id=0,task='')
            return make_response(render_template('edit.html', tasks=task))
    
    def post(self,id):
        tsk = request.form.get('subject')
        username = 'vivek'
        date = dt.now()
        if(id=='0'):
            db.session.add(Tasks(task=tsk,username=username,updated_ts=date))
            db.session.commit()
            return redirect('/')
        else:
            task = Tasks.query.filter(Tasks.id==id).first()
            task.task = tsk
            task.username = username
            task.updated_ts = date
            db.session.commit()
            return redirect('/')

class Delete(Resource):
    def get(self,id):
        task = Tasks.query.filter(Tasks.id==id).one_or_none()
        if(task):
            db.session.delete(task)
            db.session.commit()
            return redirect('/')
        else:
            abort(406,f"The task you are trying to delete does not exist")

api.add_resource(Home,"/")
api.add_resource(Edit,"/edit/<string:id>")
api.add_resource(Delete,"/delete/<string:id>")

if __name__ == '__main__':
    app.run(debug=True)