from locust import HttpLocust, TaskSequence, TaskSet, constant, seq_task, task


def wizuber_url(postfix: str = "") -> str:
    return f"/wizuber/{postfix}"


def get_csrf_token(task_set: TaskSet, url: str, name=None):
    """ https://stackoverflow.com/questions/51693930 """
    response = task_set.client.get(url, name=name)
    csrf_token = response.cookies["csrftoken"]
    return (
        csrf_token,
        {
            "X-CSRFToken": csrf_token,
            # 'Referer': task_set.parent.host + url
        },
    )


class CreateAndDeleteForWish(TaskSequence):
    @seq_task(1)
    def create_and_pay_wish(self):
        create_wish_url = wizuber_url("wish/create/")
        csrf_token, headers = get_csrf_token(self, create_wish_url)
        data = dict(description="load testing wish", price=322)
        response = self.client.post(create_wish_url, data, headers=headers)
        self.created_wish_url = response.url

    @seq_task(2)
    def post_action(self):
        self._post_action()

    def _post_action(self):
        """ delete this wish after creation """
        csrf_token, headers = get_csrf_token(
            self, self.created_wish_url, name=wizuber_url("wish/[id]/")
        )
        pay_url = self.created_wish_url + "handle/delete"
        self.client.post(
            pay_url, headers=headers, name=wizuber_url("wish/[id]/handle/delete")
        )

    @seq_task(3)
    def stop(self):
        self.interrupt()


class CreateWish(CreateAndDeleteForWish):
    def _post_action(self):
        """ Do not delete created wish """


class CustomerTask(TaskSet):
    tasks = [CreateAndDeleteForWish, CreateWish]

    def on_start(self):
        login_url = wizuber_url("account/login/")
        csrf_token, headers = get_csrf_token(self, login_url)
        data = dict(username="c1", password="123", csrfmiddlewaretoken=csrf_token)
        self.client.post(login_url, data, headers=headers)

    def on_stop(self):
        self.client.get(wizuber_url("account/logout/"))

    @task
    def index(self):
        self.client.get(wizuber_url())

    @task
    def account(self):
        self.client.get(wizuber_url("account/"))

    @task
    def list_wizard(self):
        self.client.get(wizuber_url("wizard/list/"))

    @task
    def first_wizard(self):
        self.client.get(wizuber_url("wizard/4/"))

    @task
    def second_wizard(self):
        self.client.get(wizuber_url("wizard/5/"))

    @task
    def wish_list(self):
        self.client.get(wizuber_url("wish/list/"))

    @task
    def wish_list_last_page(self):
        self.client.get(wizuber_url("wish/list/") + "?page=last")

    @task
    def wish_list_closed(self):
        self.client.get(wizuber_url("wish/list/closed/"))


class CustomerUser(HttpLocust):
    task_set = CustomerTask
    wait_time = constant(0.5)
