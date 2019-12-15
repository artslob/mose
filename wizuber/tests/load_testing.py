from locust import HttpLocust, TaskSet, constant, task


def wizuber_url(postfix: str = '') -> str:
    return f'/wizuber/{postfix}'


class CustomerTask(TaskSet):
    def on_start(self):
        login_url = wizuber_url('account/login/')
        response = self.client.get(login_url)
        csrf_token = response.cookies['csrftoken']
        self.client.post(
            login_url,
            {'username': 'c1', 'password': '123', 'csrfmiddlewaretoken': csrf_token},
            headers={
                'X-CSRFToken': csrf_token,
                'Referer': self.parent.host + login_url
            }
        )

    def on_stop(self):
        self.client.get(wizuber_url('account/logout/'))

    @task
    def index(self):
        self.client.get(wizuber_url())

    @task
    def account(self):
        self.client.get(wizuber_url('account/'))

    @task
    def list_wizard(self):
        self.client.get(wizuber_url('wizard/list/'))

    @task
    def first_wizard(self):
        self.client.get(wizuber_url('wizard/4/'))

    @task
    def second_wizard(self):
        self.client.get(wizuber_url('wizard/5/'))

    @task
    def wish_list(self):
        self.client.get(wizuber_url('wish/list/'))

    @task
    def wish_list_closed(self):
        self.client.get(wizuber_url('wish/list/closed/'))

    @task
    def create_wish(self):
        create_wish_url = wizuber_url('wish/create/')
        response = self.client.get(create_wish_url)
        csrf_token = response.cookies['csrftoken']
        self.client.post(
            create_wish_url,
            dict(description='load testing wish', price=322),
            headers={
                'X-CSRFToken': csrf_token,
                'Referer': self.parent.host + create_wish_url
            }
        )


class CustomerUser(HttpLocust):
    task_set = CustomerTask
    wait_time = constant(0.5)
