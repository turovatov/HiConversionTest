import os

from flask import Response


class StaticHandler(object):
    """

    """

    @staticmethod
    def root_dir() -> str:
        """

        :return:
        """
        return os.getcwd() + '/frontend'

    @staticmethod
    def get_file(filename: str):
        try:
            with open(filename, 'rb') as f:
                return f.read()
        except IOError as exc:
            return str(exc)

    @staticmethod
    def index() -> Response:
        """

        :return:
        """
        return StaticHandler.get_resource()

    @staticmethod
    def get_resource(path: str = 'index.html') -> Response:
        """

        :param path:
        :return:
        """
        mimetypes = {
            '.css': 'text/css',
            '.js': 'application/javascript'
        }
        complete_path = '/'.join([StaticHandler.root_dir(), path])
        ext = os.path.splitext(path)[1]
        mimetype = mimetypes.get(ext, 'text/html')
        content = StaticHandler.get_file(complete_path)
        return Response(content, mimetype=mimetype)
