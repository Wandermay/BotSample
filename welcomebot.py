from flask import Flask, jsonify, abort, request
from flask_cors import CORS, cross_origin
import requests
import json

app = Flask(__name__)

#功能:每当有一个新的Issue创建时，问候创建者并表示欢迎
@app.route('/issuewelcome', methods=['POST'])
@cross_origin()
def issue_welcome():
    payload = request.json
    print(payload)
    #判断是新创建issue，还是issue的状态发生改变
    if payload.action != 'opened':
        return 'Hello~!There is an state of issue changed!'
    url_basic = 'https://api.github.com/repos/{user_repos}/issues/{number}/comments'
    # 拼接修改url
    user_repos = payload['repository']['full_name']
    number = payload['issue']['number']
    url = url_basic.format(user_repos=user_repos, number=number)
    header = {
        'User-Agent': 'Mozilla/5.0',
        'Authorization': 'token  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',
        'Content-Type': 'application/json',
        'Accept': 'application/vnd.github.v3+json'
    } #定制 header 的优先级低于某些特定的信息源
    data = json.dumps({'body': 'Welcome to join our project!\n Thank you for your Issue. Let us work together'})
    response = requests.post(url,data=data, headers=header)
    print(response)
    return 'Hello~!There is a new issue created!'

if __name__ == '__main__':
    app.run(port=4688)