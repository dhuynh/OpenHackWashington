import requests

url = "https://dcchallenge.azurewebsites.net/qnamaker/knowledgebases/ec651253-e736-4b1b-bc18-a2d69f35e94b/generateAnswer"

payload = "{\"question\":\"What do you do?\"}"
headers = {
    'authorization': "EndpointKey 7eaae320-7d57-4f5f-8c26-f408a1215e97",
    'content-type': "application/json",
    'cache-control': "no-cache",
    'postman-token': "b1c360e9-22d7-4484-1910-45f992eb04bc"
    }

response = requests.request("POST", url, data=payload, headers=headers)

print(response.text)