from locust import HttpUser, task, between
from random import randint

class LoadTestUser(HttpUser):
    wait_time = between(1, 5)

    @task
    def get_square(self):
        self.client.get("/square-numbers")

    @task
    def load_test_endpoint(self):
        a = randint(0, 10)
        b = randint(0, 10)
        self.client.get(f'/add-two-numbers/?a={a}&b={b}')

    @task
    def user_flow(self):
        self.client.get("/")
        self.client.get("/square-numbers")
        self.client.get("/add-two-numbers/?a=5&b=3")

    @task(3)
    def get_square(self):
        self.client.get("/square-numbers")

    @task(1)
    def add_numbers(self):
        self.client.get("/add-two-numbers/?a=2&b=3")

    @task
    def add_numbers_random(self):
        a = randint(-1000, 1000)
        b = randint(-1000, 1000)
        self.client.get(f'/add-two-numbers/?a={a}&b={b}')

    @task
    def invalid_requests(self):
        self.client.get("/add-two-numbers/?a=hello&b=world")
        self.client.get("/add-two-numbers/")
        self.client.get("/square-numbers/?n=invalid")


    def on_start(self):

        response = self.client.get("/accounts/login/")
        csrf_token = response.cookies["csrftoken"]

        self.client.post("/accounts/login/", {
            "username": "UsuarioPrueba",
            "password": "UsuarioPrueba",
            "csrfmiddlewaretoken": csrf_token
        }, headers={"Referer": "/accounts/login/"})

    @task
    def authenticated_request(self):
        self.client.get("/favorites/")

    @task
    def test_response(self):
        with self.client.get("/add-two-numbers/?a=2&b=3", catch_response=True) as response:
            if response.text != "5":
                response.failure("Wrong result")

    @task
    def full_flow(self):
        self.client.get("/")
        self.client.get("/airport/LEMD")
        self.client.get("/airport/LEMD/decoded/")
        self.client.get("/favorites")
        self.client.get("/airport_compare/?icao1=LEMD&icao2=LEBL")