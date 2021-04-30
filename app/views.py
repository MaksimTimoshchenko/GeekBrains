from gungner import render
from patterns.creational_patterns import Logger, Engine
from patterns.structural_patterns import Router, Debug


engine = Engine()
logger = Logger('main')
routes = {}


# контроллер - главная страница
@Router(url='/', routes=routes)
class Index:
    @Debug(name='Index')
    def __call__(self, request):
        # print(logger, logger2)
        logger.log('LogLine: ' + str(request.get('date').strftime('%H:%M:%S')) + ' - главная страница!')
        return '200 OK', render('index.html', page='index')

@Router(url='/about', routes=routes)
class About:
    @Debug(name='About')
    def __call__(self, request):
        return '200 OK', render('about.html', page='about')

@Router(url='/learning', routes=routes)
class Learning:
    @Debug(name='Learning')
    def __call__(self, request):
        promocode = request.get('promocode', None)
        date = request.get('date', None)
        cities = ['Москва', 'Санкт-Петербург', 'Екатеринбург']
        courses = [
            {
                'title': 'Основы Python',
                'schedule': [
                    {
                        'date': 'Сб, 20 февраля 2021',
                        'time': '11:00 - 14:00'
                    },
                    {
                        'date': 'Сб, 6 марта 2021',
                        'time': '11:00 - 14:00'
                    },
                    {
                        'date': 'Сб, 20 марта 2021',
                        'time': '11:00 - 14:00'
                    },
                ]
            },
            {
                'title': 'Алгоритмы и структуры данных на Python',
                'schedule': [
                    {
                        'date': 'Сб, 10 апреля 2021',
                        'time': '11:00 - 13:00'
                    },
                    {
                        'date': 'Сб, 1 мая 2021',
                        'time': '11:00 - 13:00'
                    },
                    {
                        'date': 'Сб, 8 мая 2021',
                        'time': '11:00 - 13:00'
                    },
                ]
            },
            {
                'title': 'Основы Django',
                'schedule': [
                    {
                        'date': 'Сб, 26 июня 2021',
                        'time': '11:00 - 13:00'
                    },
                    {
                        'date': 'Сб, 3 июля 2021',
                        'time': '11:00 - 13:00'
                    },
                    {
                        'date': 'Сб, 10 июля 2021',
                        'time': '11:00 - 13:00'
                    },
                ]
            },
            {
                'title': 'Основы Flask',
                'schedule': [
                    {
                        'date': 'Сб, 28 августа 2021',
                        'time': '11:00 - 16:00'
                    },
                    {
                        'date': 'Сб, 4 сентября 2021',
                        'time': '11:00 - 16:00'
                    },
                    {
                        'date': 'Сб, 11 сентября 2021',
                        'time': '11:00 - 16:00'
                    },
                ]
            }
        ]
        return '200 OK', render('learning.html', date=date, cities=cities, courses=courses, promocode=promocode, page='learning')

@Router(url='/contact', routes=routes)
class Contact:
    @Debug(name='Contact')
    def __call__(self, request):
        if 'params' in request and request['method'] == 'POST':
            contact = ', '.join("{!s}={!r}".format(key,val) for (key,val) in request['params'].items())
            with open("contacts.txt", "a+") as contacts_file:
                contacts_file.write(contact + "\n")
        
        return '200 OK', render('contact.html', page='contact')

@Router(url='/categories/create', routes=routes)
class CreateCategory:
    def __call__(self, request):
        logger.log('LogLine: ' + str(request.get('date').strftime('%H:%M:%S')) + ' - создание категории!')
        if request['method'] == 'POST':
            name = request['params'].get('name', None)
            
            # TODO: Session postback
            if engine.get_category_by_name(name) is not None:
                raise Exception('Категория с таким именем уже создана!')

            category = engine.create_category(name)
            engine.categories.append(category)

            return '200 OK', render('categories.html', categories_list=engine.categories, page='categories')
        else:
            return '200 OK', render('category_create.html', page='category_create')

@Router(url='/categories', routes=routes)
class CategoriesList:
    def __call__(self, request):
        logger.log('LogLine: ' + str(request.get('date').strftime('%H:%M:%S')) + ' - список категорий')
        return '200 OK', render('categories.html', categories_list=engine.categories, page='categories')

@Router(url='/courses/create', routes=routes)
class CreateCourse:
    category_id = 0

    def __call__(self, request):
        logger.log('LogLine: ' + str(request.get('date').strftime('%H:%M:%S')) + ' - создание курса!')
        if request['method'] == 'POST':
            name = request['params'].get('name', None)
            type_alias = request['params'].get('type_alias', None)

            # TODO: Session postback
            if not name:
                raise Exception('Необходимо указать название курса!')

            if type_alias not in ['webinar', 'interactive', 'video']:
                raise Exception('Некорректный тип курса!')
                
            category = None
            if self.category_id != 0:
                category = engine.get_category_by_id(int(self.category_id))

                course = engine.create_course(type_alias, name, category)
                engine.courses.append(course)

            return '200 OK', render('courses.html', courses_list=engine.courses)

        else:
            try:
                self.category_id = request['params'].get('id')
                category = engine.get_category_by_id(int(self.category_id))

                return '200 OK', render('course_create.html', category=category)
            except KeyError:
                return '200 OK', 'Сначала нужно добавить категории!'

@Router(url='/courses', routes=routes)
class CoursesList:
    def __call__(self, request):
        logger.log('LogLine: ' + str(request.get('date').strftime('%H:%M:%S')) + ' - список курсов!')
        try:
            category = engine.get_category_by_id(request['params'].get('id'))
            return '200 OK', render('courses.html', courses_list=category.courses, page='courses')
        
        except KeyError:
            return '200 OK', 'Список курсов пуст!'

@Router(url='/courses/copy', routes=routes)
class CopyCourse:
    def __call__(self, request):
        logger.log('LogLine: ' + str(request.get('date').strftime('%H:%M:%S')) + ' - копирование курса!')
            
        try:
            name = request['params'].get('name', None)
            
            if not name:
                raise Exception('Не указано название курса, который будет скопирован!')

            copied_course = engine.get_course_by_name(name)

            if not copied_course:
                raise Exception('Курс с таким именем не найден!')

            if copied_course:
                new_name = f'copy_{name}'
                course = copied_course.clone()
                course.name = new_name
                engine.courses.append(course)

            return '200 OK', render('courses.html', courses_list=engine.courses)
        
        except KeyError:
            return '200 OK', 'Список курсов пуст!'
        