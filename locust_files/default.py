from locust import HttpLocust, TaskSet, task
import random

class UserBehavior(TaskSet):
    search_terms = [
        'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm',
        'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z',
        'avr', 'atmega', 'attiny', 'cd', 'hex', 'schmitt', 'quad',
        '2-input', 'nand', 'nor', 'xor', 'operational', 'amplifier',
        'lm555', '555',
    ]
    queries = []

    def on_start(self):
        """ on_start is called when a Locust start before any task is scheduled """
        for _ in range(0, 500):
            num_words = random.randint(1, 10)
            query = ''
            for _ in range(0, num_words):
                query += '{} '.format(random.choice(self.search_terms))
            self.queries.append(query)

#    def on_stop(self):
#        """ on_stop is called when the TaskSet is stopping """
#        pass

    @task(1)
    def index(self):
        self.client.get("/")

    @task(1)
    def browse_parts(self):
        self.client.get("/parts")

    @task(1)
    def search(self):
        self.client.get('/search?q=' + random.choice(self.queries), name='/search?q=[query]')


class WebsiteUser(HttpLocust):
    task_set = UserBehavior
    min_wait = 500
    max_wait = 1000
