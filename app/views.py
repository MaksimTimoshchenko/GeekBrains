from gungner import render


class Index:
    def __call__(self, request):
        return '200 OK', render('index.html', page='index')

class About:
    def __call__(self, request):
        return '200 OK', render('about.html', page='about')

class Learning:
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

class Contact:
    def __call__(self, request):
        if 'params' in request and request['method'] == 'POST':
            contact = ', '.join("{!s}={!r}".format(key,val) for (key,val) in request['params'].items())
            with open("contacts.txt", "a+") as contacts_file:
                contacts_file.write(contact + "\n")
        
        return '200 OK', render('contact.html', page='contact')