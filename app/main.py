from gungner import Gungner
from .urlpatterns import front_controllers
from .views import routes


application = Gungner(routes, front_controllers)

if __name__ == '__main__':
    application.run()
