import copy

from patterns.behavioral_patterns import ConsoleWriter, Subject 


class User:
    def __init__(self, name):
        self.name = name
        self.courses = []

class Teacher(User):
    pass

class Student(User):
    pass


class UserFactory:
    types = {
        'teacher': Teacher,
        'student': Student
    }

    # Фабричный метод
    @classmethod
    def create(cls, type_, name):
        return cls.types[type_](name)

# Прототип
class CoursePrototype:

    def clone(self):
        return copy.deepcopy(self)

class Course(CoursePrototype, Subject):
    course_id = 1

    def __init__(self, name, category, type_):
        self.id = Course.course_id
        Course.course_id += 1
        self.name = name
        self.category = category
        self.category.courses.append(self)
        self.type_alias = type_
        self.observers = []
        self.students = []

    def attach(self, observer):
        self.observers.append(observer)

    def detach(self, observer):
        self.observers.remove(observer)

    def notify(self):
        for observer in self.observers:
            observer.update(self)

    def add_student(self, student):
        self.students.append(student)

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
        return cls.types[type_](name, category, type_)
        
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
        self.students = []
        self.courses = []
        self.categories = []

        # Data for observer demo
        category = Category(name='Web разработка на Python', category=None)
        self.categories.append(category)

        course = CourseFactory().create(type_='interactive', name='Архитектура и шаблоны проектирования на Python', category=category)
        student = UserFactory().create('student', 'Максим Тимощенко')
        self.students.append(student)
        course.students.append(student)

        self.courses.append(course)

    @staticmethod
    def create_user(type_, name):
        return UserFactory.create(type_, name)

    @staticmethod
    def create_category(name, category=None):
        return Category(name, category)

    def get_category_by_id(self, id):
        for category in self.categories:
            if category.id == int(id):
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

    def get_course_by_id(self, id):
        for course in self.courses:
            if course.id == int(id):
                return course
        raise Exception(f'Курс с id = {id} не найден')

    def get_student_by_name(self, name):
        for student in self.students:
            if student.name == name:
                return student

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
    def __init__(self, writer=ConsoleWriter()):
        self.writer = writer

    def log(self, text):
        self.writer.write(text)
