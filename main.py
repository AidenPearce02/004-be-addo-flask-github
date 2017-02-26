from flask import Flask, render_template, abort, request
import requests

app = Flask(__name__)


@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')


@app.route('/', methods=['POST'])
def user_info():
    username = request.values.get('username', None)
    u = requests.get('https://api.github.com/users/' + username)
    if u.status_code == 200:
        dbinfo = ["Username : "+username,"Name : " + str(u.json().get('name')),"Email : " + str(u.json().get('email')),"Followers : " + str(u.json().get('followers'))]
        listRepo=[]
        r = requests.get('https://api.github.com/users/' + username + '/repos')
        for repo in range(len(r.json())):
            c = requests.get('https://api.github.com/repos/' + username + '/' + r.json()[repo].get('name') + '/commits')
            b = requests.get('https://api.github.com/repos/' + username + '/' + r.json()[repo].get('name') + '/branches')
            result=r.json()[repo].get('name') + ': ' + str(len(c.json())) + ' commits; ' + str(len(b.json())) + ' branches.'
            listRepo.insert(repo,result)
        return render_template('index.html', dbinfo=dbinfo,listRepo=listRepo)
    else:
        return render_template('index.html', **{'error': 'Incorrect username'})


if __name__ == '__main__':
    app.run()
