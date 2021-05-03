from gungner import DebugGungner
from .urlpatterns import front_controllers
from .views import routes


application = DebugGungner(routes, front_controllers)

if __name__ == '__main__':
    application.run()
