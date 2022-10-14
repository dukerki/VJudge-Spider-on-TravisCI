import requests
import json


def run():
    payload = json.dumps({"ref": "main"})
    header = {'Authorization': 'token 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',
              "Accept": "application/vnd.github.v3+json"}
    response_decoded_json = requests.post(
        f'https://api.github.com/repos/CUCCS/VJudge-Spider-on-TravisCI/actions/workflows/ci.yml/dispatches',
        data=payload, headers=header)
    print(response_decoded_json)


run()  # 云函数入口
