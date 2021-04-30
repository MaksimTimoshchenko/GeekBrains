import copy

from datetime import datetime


class User:
    def __init__(self, name):
        self.name = name
        self.courses = []

class Teacher(User):
    pass

class User(User):
    pass


class UserFactory:
    types = {
        'teacher': Teacher,
        'user': User
    }

    # Фабричный метод
    @classmethod
    def create(cls, type_, name):
        return cls.types[type_](name)

# Прототип
class CoursePrototype:

    def clone(self):
        return copy.deepcopy(self)

class Course(CoursePrototype):

    def __init__(self, name, category):
        self.name = name
        self.category = category
        self.category.courses.append(self)

class WebinarCourse(Course):
    pass

class InteractiveCourse(Course):
    pass

class VideoCourse(Course):
    pass


class CourseFactory:
    types = {
        'webinar': WebinarCourse,
        'interactive': InteractiveCourse,
        'video': VideoCourse
    }

    # Фабричный метод
    @classmethod
    def create(cls, type_, name, category):
        return cls.types[type_](name, category)
        
class Category:
    category_id = 1

    def __init__(self, name, category):
        self.id = Category.category_id
        Category.category_id += 1
        self.name = name
        self.parent_category = category
        self.courses = []

    def courses_count(self):
        result = len(self.courses)
        if self.parent_category:
            result += self.parent_category.courses_count()
        return result


class Engine:
    def __init__(self):
        self.teachers = []
        self.users = []
        self.courses = []
        self.categories = []

    @staticmethod
    def create_user(type_, name):
        return UserFactory.create(type_, name)

    @staticmethod
    def create_category(name, category=None):
        return Category(name, category)

    def get_category_by_id(self, id):
        for category in self.categories:
            if category.id == id:
                return category
        raise Exception(f'Категория с id = {id} не найдена')

    def get_category_by_name(self, name):
        for category in self.categories:
            if category.name == name:
                return category
        return None

    @staticmethod
    def create_course(type_, name, category):
        return CourseFactory.create(type_, name, category)

    def get_course_by_name(self, name):
        for course in self.courses:
            if course.name == name:
                return course
        return None

# Синглтон
class MetaSingleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if args:
            name = args[0]
        if kwargs:
            name = kwargs['name']

        if name not in cls._instances:
            cls._instances[name] = super().__call__(*args, **kwargs)
        return cls._instances[name]

class Logger(metaclass=MetaSingleton):
    def __init__(self, name):
        self.name = name

    def log(self, text):
        # в зависимости от имени переданного в инициализацию логгера сами логи пишутся в разные файлы
        with open("log_" + str(self.name) + "_" + datetime.now().strftime("%Y-%m-%d") + ".txt", "a+") as log_file:
            log_file.write(text + "\n")
