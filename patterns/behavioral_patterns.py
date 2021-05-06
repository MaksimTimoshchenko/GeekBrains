import jsonpickle

from abc import ABCMeta, abstractmethod
from datetime import datetime

from gungner import render


class TemplateView:
    template_name = 'template.html'
    page = ''

    def get_context_data(self):
        return {}

    def get_template(self):
        return self.template_name

    def render_with_context(self):
        template_name = self.get_template()
        context = self.get_context_data() | { 'page': self.page }
        return '200 OK', render(template_name, **context)

    def __call__(self, request):
        return self.render_with_context()

class CreateView(TemplateView):
    template_name = 'create.html'

    @staticmethod
    def get_request_params(request):
        return request['params']

    def create_object(self, data):
        pass

    def __call__(self, request):
        if request['method'] == 'POST':
            data = self.get_request_params(request)
            self.create_object(data)

            return self.render_with_context()
        else:
            return super().__call__(request)

class ListView(TemplateView):
    queryset = []
    template_name = 'list.html'
    context_object_name = 'objects_list'

    def get_queryset(self):
        return self.queryset

    def get_context_object_name(self):
        return self.context_object_name

    def get_context_data(self):
        queryset = self.get_queryset()
        context_object_name = self.get_context_object_name()
        context = {context_object_name: queryset}
        return context

class UpdateView(TemplateView):
    object = []
    template_name = 'edit.html'
    context_object_name = 'object'
    request_params = []

    def get_object(self, data):
        pass

    def update_object(self, data):
        pass

    def get_context_object_name(self):
        return self.context_object_name

    def get_context_data(self):
        context = {self.context_object_name: self.object}
        return context

    def __call__(self, request):
        request_params = request.get('params')
        if request['method'] == 'GET':
            self.object = self.get_object(request_params)
        elif request['method'] == 'POST':
            self.update_object(request_params)

        return self.render_with_context()

class Observer(metaclass=ABCMeta):
    """Паттерн Наблюдатель"""

    @abstractmethod
    def update(self, subject):
        pass

class Subject(metaclass=ABCMeta):

    @abstractmethod
    def attach(self, observer):
        pass

    @abstractmethod
    def detach(self, observer):
        pass

    @abstractmethod
    def notify(self):
        pass

class SmsNotifier(Observer):

    def update(self, subject):
        for student in subject.students:
            print('SMS: Привет, ', student.name, '! Курс «', subject.name, '» изменился!')


class EmailNotifier(Observer):

    def update(self, subject):
        for student in subject.students:
            print('Email: Привет, ', student.name, '! Курс «', subject.name, '» изменился!')

# поведенческий паттерн - Стратегия
class ConsoleWriter:

    def write(self, text):
        print(text)


class FileWriter:

    def __init__(self, name):
        self.name = name

    def write(self, text):        
        # в зависимости от имени переданного в инициализацию логгера сами логи пишутся в разные файлы
        with open("log_" + str(self.name) + "_" + datetime.now().strftime("%Y-%m-%d") + ".txt", "a+") as log_file:
            log_file.write(f'{text}\n')

class BaseSerializer:

    def __init__(self, obj):
        self.obj = obj

    def save(self):
        return jsonpickle.dumps(self.obj)

    @staticmethod
    def load(data):
        return jsonpickle.loads(data)