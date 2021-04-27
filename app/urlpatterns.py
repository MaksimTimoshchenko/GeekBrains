from datetime import datetime
from secrets import token_hex
from .views import About, CategoriesList, Contact, CopyCourse, CreateCategory, CreateCourse, CoursesList, Index, Learning

def generate_promocode_front_controller(request):
    request['promocode'] = token_hex(16)

def fixate_request_date_front_controller(request):
    request['date'] = datetime.now()

front_controllers = [
    generate_promocode_front_controller,
    fixate_request_date_front_controller
]

urlpatterns = {
    '/': Index(),
    '/about': About(),
    '/categories/create': CreateCategory(),
    '/categories': CategoriesList(),
    '/contact': Contact(),
    '/courses/copy': CopyCourse(),
    '/courses/create': CreateCourse(),
    '/courses': CoursesList(),
    '/learning': Learning(),
}
