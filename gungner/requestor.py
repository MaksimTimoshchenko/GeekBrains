import quopri


class Requestor:

    @staticmethod
    def parse_input_data(data: str):
        result = {}
        if data:
            params = data.split('&')
            for param in params:
                k, v = param.split('=')
                result[k] = v
        return result

    @staticmethod
    def get_wsgi_input_data(environ) -> bytes:
        content_length_data = environ.get('CONTENT_LENGTH')
        content_length = int(content_length_data) if content_length_data else 0

        data = environ['wsgi.input'].read(content_length) if content_length > 0 else b''
        return data
    
    def parse_wsgi_input_data(self, data: bytes) -> dict:
        result = {}
        if data:
            data_str = data.decode(encoding='utf-8')
            result = self.parse_input_data(data_str)
        return result

    @staticmethod
    def decode_value(data):
        new_data = {}
        for k, v in data.items():
            val = bytes(v.replace('%', '=').replace("+", " "), 'UTF-8')
            val_decode_str = quopri.decodestring(val).decode('UTF-8')
            new_data[k] = val_decode_str
        return new_data

    def get_request_params(self, environ):
        request = {}
        method = environ['REQUEST_METHOD']
        request['method'] = method
        if method == 'GET':
            query_string = environ['QUERY_STRING']
            request_params = self.parse_input_data(query_string)
        elif method == 'POST':
            data = self.get_wsgi_input_data(environ)
            request_params = self.decode_value(self.parse_wsgi_input_data(data))

        request['params'] = request_params

        return request
