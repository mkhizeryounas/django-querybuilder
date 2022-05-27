from django.test import SimpleTestCase
import logging
from ..query_filter import rename_operation_name, tokenize, array_to_tree
from django.db.models import Q

logger = logging.getLogger(__name__)


class TestQueryFilter(SimpleTestCase):
    # Set base params to reuse the same query and parsed_query
    query = 'EQUAL(id, "first-post")'
    parsed_query = {'operator': 'EQUAL',
                    'param1': 'id', 'param2': 'first-post'}

    def test_should_rename_operation_name(self):
        """Test rename_operation_name function"""
        self.assertEqual(rename_operation_name("LESS_THAN"), "lt")
        self.assertEqual(rename_operation_name("GREATER_THAN"), "gt")
        self.assertEqual(rename_operation_name("EQUAL"), "eq")
        self.assertEqual(rename_operation_name("NOT_EQUAL"), "ne")

    def test_should_tokenize_query(self):
        """Test Tokenizes query"""
        self.assertListEqual(tokenize(self.query), [self.parsed_query])
        self.assertListEqual(tokenize(f'NOT({self.query})'), [
            {'operator': 'NOT'},
            self.parsed_query
        ])
        self.assertListEqual(tokenize(f'OR({self.query}, NOT({self.query}))'), [
            {'operator': 'OR'},
            self.parsed_query,
            {'operator': 'NOT'},
            self.parsed_query
        ])

    def test_should_tokenize_raise_exception_with_invalid_query(self):
        """Test raises exception with invalid query"""
        with self.assertRaises(Exception):
            # The passed query is not valid because the paranethesis are not balanced
            tokenize(f'{self.query})')

    def test_should_array_to_tree_return_filter_tree(self):
        """Test converts operator array to query tree"""
        # Construct Q tree for EQUAL operator
        self.assertEqual(array_to_tree(
            array=[self.parsed_query], filter=Q()), Q(id="first-post"))

        # Construct Q tree for OR operator
        filter = Q()
        filter.add(Q(id="first-post"), Q.OR)
        filter.add(~Q(id="first-post"), Q.OR)

        self.assertEqual(
            array_to_tree(array=[
                {'operator': 'OR'},
                self.parsed_query,
                {'operator': 'NOT'},
                self.parsed_query], filter=Q()
            ), filter
        )

        # Construct Q tree for AND operator
        filter = Q()
        filter.add(Q(id="first-post"), Q.AND)
        filter.add(~Q(id="first-post"), Q.AND)

        self.assertEqual(
            array_to_tree(array=[
                {'operator': 'AND'},
                self.parsed_query,
                {'operator': 'NOT'},
                self.parsed_query], filter=Q()
            ), filter
        )
