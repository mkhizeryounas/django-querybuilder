import ddt
from django.test import SimpleTestCase
import logging
from ..query_filter import rename_operation_name, tokenize, array_to_tree
from django.db.models import Q

logger = logging.getLogger(__name__)


def construct_actual_filter(conn_type=Q.AND, both_params_not=False):
    """Construct actual Q filter

        Args:
            conn_type (str, optional): Connection type. Defaults to Q.AND.

        Returns:
            Q: Query filter
        """
    filter = Q()

    if both_params_not:
        filter.add(~Q(id="first-post"), conn_type=conn_type)
    else:
        filter.add(Q(id="first-post"), conn_type=conn_type)

    filter.add(~Q(views__lt=2), conn_type=conn_type)
    return filter


@ddt.ddt
class TestQueryFilter(SimpleTestCase):
    # Set base params to reuse the same query and parsed_query
    query = 'EQUAL(id, "first-post")'
    parsed_query = {'operator': 'EQUAL',
                    'param1': 'id', 'param2': 'first-post'}
    parsed_query_lt = {'operator': 'LESS_THAN',
                       'param1': 'views', 'param2': 2}

    @ddt.data(
        {'input': 'LESS_THAN', 'actual': 'lt'},
        {'input': 'GREATER_THAN', 'actual': 'gt'},
        {'input': 'EQUAL', 'actual': 'eq'},
    )
    def test_should_rename_operation_name(self, param):
        """Test rename_operation_name function"""
        self.assertEqual(rename_operation_name(
            param['input']), param['actual']
        )

    @ddt.data(
        {
            'input': query,
            'actual': [
                parsed_query
            ]
        },
        {
            'input': "",
            'actual': []
        },
        {
            'input': f'NOT({query})',
            'actual': [
                {'operator': 'NOT'},
                parsed_query
            ]
        },
        {
            'input': f'OR({query}, NOT({query}))',
            'actual': [
                {'operator': 'OR'},
                parsed_query,
                {'operator': 'NOT'},
                parsed_query
            ]
        },
        {
            'input': f'AND({query}, NOT({query}))',
            'actual': [
                {'operator': 'AND'},
                parsed_query,
                {'operator': 'NOT'},
                parsed_query
            ]
        },
    )
    def test_should_tokenize_query(self, params):
        """Test Tokenizes query"""
        self.assertListEqual(tokenize(params['input']), params['actual'])

    @ddt.data(
        f'{query})',
        f'({query}'
    )
    def test_should_tokenize_raise_exception_with_invalid_query(self, param):
        """Test raises exception with invalid query"""
        with self.assertRaises(Exception):
            # The passed query is not valid because the paranethesis are not balanced
            tokenize(param)

    @ddt.data(
        {
            'input': [parsed_query],
            'actual': Q(id="first-post")
        },
        # Checking for OR and NOT operators
        {
            'input': [
                {'operator': 'OR'},
                parsed_query,
                {'operator': 'NOT'},
                parsed_query_lt
            ],
            'actual': construct_actual_filter(conn_type=Q.OR)
        },
        # Checking for AND and NOT operators
        {
            'input': [
                {'operator': 'AND'},
                parsed_query,
                {'operator': 'NOT'},
                parsed_query_lt
            ],
            'actual': construct_actual_filter(conn_type=Q.AND)
        },
        {
            'input': [
                {'operator': 'AND'},
                {'operator': 'NOT'},
                parsed_query,
                {'operator': 'NOT'},
                parsed_query_lt
            ],
            'actual': construct_actual_filter(conn_type=Q.AND, both_params_not=True)
        },
    )
    def test_should_array_to_tree_return_filter_tree(self, params):
        """Test converts operator array to query tree"""
        self.assertEqual(
            array_to_tree(array=params['input'], filter=Q()),
            params['actual']
        )
