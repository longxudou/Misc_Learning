# encoding:utf-8
import requests
import json

def get_access_token():
    # client_id 为官网获取的AK， client_secret 为官网获取的SK
    host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=RiqnlGlCco6lwYfyz5s9MdeA&client_secret=eHfNKIaS9tM533OBcUDrSpfl76rywWXk'

    response = requests.get(host)
    # if response:
    #     print(response.json())
    content = response.json()
    access_token = content["access_token"]
    return access_token


def query(query_list,access_token):
    result=[]
    request_url = "https://aip.baidubce.com/rpc/2.0/ai_custom_pro/v1/text_cls/mooc_v1" + "?access_token=" + access_token

    for token in query_list:
        query={'text':token}
        response = requests.post(request_url, data=json.dumps(query))
        content = response.json()

        tag=content['results'][0]['name']
        score = content['results'][0]['score']

        result.append((tag,score))
    return result

if __name__ == '__main__':
    query_list=['我们说采购管理的一个基本的思想是什么？']
    access_token = get_access_token()
    result=query(query_list, access_token)
    print(result)

