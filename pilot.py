import os
import json

from flask import Flask, request
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

class webhook(Resource):
    def post(self):
        data = str(request.data)[2:len(str(request.data)) -1]
        data = json.loads(data)
        if (data['repository']['name'] ) == "CodingChallengeEntry":
            os.system('pm2 stop bot.py')
            os.system('git pull')
            os.system('pm2 start bot.py')
            print("Updated Bot from github.")
        return 200

api.add_resource(webhook, '/github.push')

if __name__ == '__main__':
    app.run(debug=False,host='0.0.0.0',port=8080)
