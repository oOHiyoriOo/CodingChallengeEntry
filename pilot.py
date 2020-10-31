import filecmp
import os
import json

from flask import Flask, request
from flask_restful import Resource, Api


#if not filecmp.cmp('bot.py','github.py'):
#    #os.system('pm2 stop bot.py')
#    os.system('git pull')
#else:
#    print('Up to Date')




app = Flask(__name__)
api = Api(app)

class webhook(Resource):
    def post(self):
        data = str(request.data)[2:len(str(request.data)) -1]
        data = json.loads(data)
        print(data['repository']['name'] )
        return 200

api.add_resource(webhook, '/github.push')

if __name__ == '__main__':
    app.run(debug=False,host='0.0.0.0',port=8080)
