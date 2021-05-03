from time import time


class Router:

    def __init__(self, url, routes):
        self.url = url
        self.routes = routes

    def __call__(self, cls):
        self.routes[self.url] = cls()

class Debug:

    def __init__(self, name):
        self.name = name

    def __call__(self, cls):
        def wrapper(function):
            def executed_delta(*args, **kwargs):
                initial_time = time()
                result = function(*args, **kwargs)
                executed_time = time()
                time_delta = executed_time - initial_time

                print(f'Debug {self.name}: executed time {time_delta:2.2f} ms.')
                return result

            return executed_delta

        return wrapper(cls)
        