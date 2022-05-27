from rest_framework.response import Response

ERROR_CODES = {
    400: 'Bad Request',
    401: 'Unauthorized',
    403: 'Forbidden',
    404: 'Not Found',
    409: 'Conflict',
    422: 'Unprocessable Entity',
    429: 'Too Many Requests',
}


def ok(data=None):
    """Format success response

    Args:
        data (dict, optional): _description_. Defaults to None.

    Returns:
        Response: Re-formated response
    """
    return Response(data)


def error(data=None, status=400):
    """Format error response

    Args:
        data (dict, optional): _description_. Defaults to None.
        status (int, optional): _description_. Defaults to 400.

    Returns:
        Response: Re-formated response
    """
    if status not in ERROR_CODES:
        status = 400
    return Response({"message": ERROR_CODES[status], "error": data}, status=status)
