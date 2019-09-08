# --*-- encoding:utf-8 --*--
import json
# import queue
from apis import get_api, SHARE_DATA
from locust import HttpLocust, TaskSet, task


class WebsiteTasks(TaskSet):
    def on_start(self):
        self.index = 0
        parmas = {"username": "ecidi", "password": "ecid@123456"}
        self.client.get("/index.php?m=sso&f=login&t=json&", data=parmas)

    @task
    def major_scene(self):
        method = self.locust.method[self.index]
        url = self.locust.urls[self.index]
        params = self.locust.params[self.index]
        # try:
        #     params = self.locust.params_queue.get()
        # except queue.Empty:
        #     print('account data run out, test ended.')
        #     exit(0)
        self.index = (self.index + 1) % (len(self.locust.urls))
        if str.lower(method) == 'post':
            if params is not None:
                self.client.post(url, data=json.loads(params))
            else:
                self.client.post(url)
        elif str.lower(method) == "put":
            if params is not None:
                self.client.put(url, data=json.loads(params))
            else:
                self.client.put(url)
        elif str.lower(method) == 'patch':
            if params is not None:
                self.client.patch(url, data=json.loads(params))
            else:
                self.client.patch(url)
        elif str.lower(method) == 'get':
            if params is not None:
                self.client.get(url, data=json.loads(params))
            else:
                self.client.get(url)
        elif str.lower(method) == 'delete':
            if params is not None:
                self.client.delete(url, data=json.loads(params))
            else:
                self.client.delete(url)
        # self.locust.post_params_queue.put_nowait(params)


class WebsiteUser(HttpLocust):
    task_set = WebsiteTasks
    host = "http://39.106.128.155"
    urls = []
    method = []
    params = []
    # params_queue = queue.Queue()

    get_api()
    for i in range(len(SHARE_DATA)):
        method.insert(-1, SHARE_DATA[i]['method'])
        urls.insert(-1, SHARE_DATA[i]['url'])
        params.insert(-1, SHARE_DATA[i]['params'])
        # params_queue.put_nowait(SHARE_DATA[i]['params'])

    min_wait = 1000
    max_wait = 5000
