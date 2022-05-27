from distutils.log import debug
from django.db.models import Q
import logging

logger = logging.getLogger(__name__)


def rename_operation_name(op):
    """Converts operation name to Django ORM compatible name
    Args:
        op (str): operation name
    Returns:
        str: Django ORM compatible name
    """
    if op == "LESS_THAN":
        op = "lt"
    elif op == "GREATER_THAN":
        op = "gt"
    elif op == "EQUAL":
        op = "eq"
    return op


def array_to_tree(array, filter=Q()):
    """Converts operator arrat to query tree

    Args:
        array (dict): List of operators and their parameters

    Returns:
        Q: Django ORM filter query
    """
    if len(array) == 0:
        return filter
    if array[0]['operator'] == 'OR' or array[0]['operator'] == 'AND':
        # Condition for OR and AND operators

        # Set the accessor for the 2nd parameter if either operation is 'NOT'
        index_p2 = 2
        if len(array) > 3 and (array[1]['operator'] == "NOT" or array[3]['operator'] == "NOT"):
            index_p2 = 3

        # Construct params for the operators and call array_to_tree recursively
        param1 = array_to_tree(array[1:], filter)
        param2 = array_to_tree(array[index_p2:], filter)

        conn_type = Q.OR if array[0]['operator'] == 'OR' else Q.AND

        filter.add(param1, conn_type)
        filter.add(param2, conn_type)
    elif array[0]['operator'] == 'NOT':
        # Condition for NOT operator
        # Returns the negated filter
        sub_tree = ~array_to_tree(array[1:], filter)
        return sub_tree
    else:
        # Rename LESS_THAN to lt, GREATER_THAN to gt, EQUAL to eq
        op = rename_operation_name(array[0]['operator'])
        key = array[0]['param1']

        if op != "eq":
            key = f"{key}__{op}"
        # Return the filter
        return Q(**{
            key: array[0]['param2']
        })
    return filter


def tokenize(query):
    """Tokenize the provided query to an array of operators and their perameters

    Args:
        query (str): Query strong to format

    Raises:
        Exception: if brakets are not matching

    Returns:
        list: [{operator:..., param1: ..., param2: ...}, ...]
    """
    if query is None:
        return []
    query = query.strip()
    if len(query) == 0:
        return []
    OPEN_BRACKETS = {
        "(": ")",
        "{": "}",
        "[": "]",
    }

    CLOSE_BRACKETS = {
        ")": "(",
        "}": "{",
        "]": "[",
    }

    stack = []
    op = ""
    tokens = []
    single_op = {}
    for i in range(0, len(query)):
        char = query[i]
        token_position = None
        # Check if the passed query is valid by checking if the brakets are matching
        if char in OPEN_BRACKETS:
            # When braket opens, it means the pre word was an operator
            stack.append(char)
            token_position = 'operator'
        elif char in CLOSE_BRACKETS:
            if len(stack) == 0 or stack.pop() != CLOSE_BRACKETS[char]:
                raise Exception('Invalid query')
            # When braket closes, it means the pre word was an 2nd parameter
            token_position = "param2"
        else:
            if char in [' ', '"', '\'']:
                continue
            if char == ',':
                # When comma is found, it means the pre word was an 1st parameter
                token_position = 'param1'
            else:
                op += char
        if token_position and len(op) > 0:
            # when we found a new operator, add the previous operator to the tokens and reset the pre operator
            if token_position == "operator":
                tokens.append(single_op)
                single_op = {}
                single_op["operator"] = op
            elif token_position == "param1":
                single_op["param1"] = op
            elif token_position == "param2":
                single_op["param2"] = op
            op = ""
    # Check if the brakets are matching
    if len(stack) > 0:
        raise Exception('Invalid query')
    # Add the last operator to the tokens
    tokens.append(single_op)
    # Filter the empty tokens as we always push an empty token on the first operation
    tokens = [token for token in tokens if token]
    return tokens


def convert_query_to_filter(query):
    """Converts query to Django ORM compatible query

    Args:
        query (str): Query string

    Returns:
        Q: Django ORM filter query
    """
    return array_to_tree(tokenize(query), Q())
