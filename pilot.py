import filecmp
import os

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
        print(request.data,end="===\nDATA\n===\n")
        print(request.form,end="===\nFORM\n===\n")
        return 200

api.add_resource(webhook, '/github.push')

if __name__ == '__main__':
    app.run(debug=True,port=8080)
