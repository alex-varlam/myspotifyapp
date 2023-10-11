import requests
import json

class BaseRest:
    def __init__(self):
        self.session = requests.Session()

    def check_response(self, response):
        if response.status_code != 200:
            raise Exception(f'Something went wrong! Got status code {response.status_code} and text {response.text}')
        try:
            data_response = json.loads(response.text)
        except:
            raise Exception('Response text was not a valid JSON!')
        return data_response

    def send_post(self, apiPath, data_json, headers):
        response = self.session.post(apiPath, data=data_json, headers=headers)
        print(f"POST message response with status code {response.status_code} and text {response.text}")
        return self.check_response(response)

    def send_get(self, apiPath, headers):
        response = self.session.get(apiPath, headers=headers)
        # print(f"GET message response with status code {response.status_code} and text {response.text}")
        return self.check_response(response)

    def send_put(self, apiPath, data, headers):
        response = self.session.put(apiPath, data=data, headers=headers)
        print(f"PUT message response with status code {response.status_code} and text {response.text}")
        return self.check_response(response)

    def send_delete(self,apiPath, headers):
        response = self.session.delete(apiPath, headers=headers)
        print(f"DELETE message response with status code {response.status_code} and text {response.text}")
        return self.check_response(response)

    def close(self):
        self.session.close()