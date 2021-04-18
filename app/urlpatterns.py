from datetime import date
from secrets import token_hex
from .views import About, Contact, Index, Learning

def generate_promocode_front_controller(request):
    request['promocode'] = token_hex(16)

def fixate_request_date_front_controller(request):
    request['date'] = date.today()

front_controllers = [
    generate_promocode_front_controller,
    fixate_request_date_front_controller
]

urlpatterns = {
    '/': Index(),
    '/about': About(),
    '/learning': Learning(),
    '/contact': Contact(),
}