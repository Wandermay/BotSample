from flask import Flask, jsonify, abort, request
from flask_cors import CORS, cross_origin
import requests
import json

app = Flask(__name__)

#根据issue标题和内容确定标签
def decide_label(title,body):
    labels_list = ['bug','duplicate','enhancement','help wanted','good first issue','question','wontfix','invalid']
    #issue标题不为空，根据标题内容判断标签
    if title:
        for i in labels_list:
            if (title.find(i) == -1):
                continue
            else:
                return i
    #issue标题不为空，根据标题内容判断标签
    if body:
        for i in labels_list:
            if (body.find(i) == -1):
                continue
            else:
                return i
    #默认情况下为bug标签
    return 'bug'

# 功能:issue创建后如果没有添加标签则自动添加标签
@app.route('/issuelabel', methods=['POST'])
@cross_origin()
def add_issue_lables():
    payload = request.json
    #判断是新创建issue，还是issue的状态发生改变
    if payload.action != 'opened':
        return 'Hello~!There is an state of issue changed!'
    # 判断是创建的issue是否添加标签
    if payload.issue.labels:
        return 'Hello~!There is a new issue with label!'

    url_basic = 'https://api.github.com/repos/{owner}/{repo}/issues/{issue_number}/labels'
    # 拼接修改url
    owner = payload['repository']['owner']['login']
    repos = payload['repository']['name']
    number = payload['issue']['number']
    url = url_basic.format(owner=owner,repos=repos, issue_number=number)
    header = {
        'User-Agent': 'Mozilla/5.0',
        'Authorization': 'token  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',
        'Content-Type': 'application/json',
        'Accept': 'application/vnd.github.v3+json'
    }
    #提取title和body信息
    issue_title = payload['issue']['title']
    issue_body= payload['issue']['body']
    label = decide_label(issue_title,issue_body)
    data = json.dumps({'labels': label})
    response = requests.post(url,data=data, headers=header)
    return 'Hello~!There is a new issue with no label!'

if __name__ == '__main__':
    app.run(port=4688)