""" Кастомные исключения. """
from rest_framework.exceptions import APIException


class DeletionError(APIException):
    """ Исключение для случаев, когда после удаления элемента число элементов в категории будет меньше необходимого. """
    status_code = 400
    default_code = "DELETION_ERROR"


class EditionError(APIException):
    """ Исключение для случаев изменения запрещённых к изменению полей. """
    status_code = 400
    default_code = 'EDITION_ERROR'
