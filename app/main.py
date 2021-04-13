from gungner import Gungner
from .urlpatterns import urlpatterns, front_controllers


application = Gungner(urlpatterns, front_controllers)

if __name__ == '__main__':
    application.run()
