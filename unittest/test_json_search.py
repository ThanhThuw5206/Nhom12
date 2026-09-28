import unittest
from recursive_json_search import *
from test_data import *


class json_search_test(unittest.TestCase):
    '''test module to test search function in `recursive_json_search.py`'''

    # ---------- Functional tests (chức năng gốc) ----------
    def test_search_found(self):
        '''key should be found, return list should not be empty'''
        self.assertTrue([] != json_search(key1, data))

    def test_search_not_found(self):
        '''key should not be found, should return an empty list'''
        self.assertTrue([] == json_search(key2, data))

    def test_is_a_list(self):
        '''Should return a list'''
        self.assertIsInstance(json_search(key1, data), list)

    # ---------- Security tests (kiểm soát truy cập theo role) ----------
    def test_viewer_cannot_read_apikey(self):
        '''viewer role must NOT receive the apiKey secret'''
        self.assertEqual([], json_search("apiKey", data, role="viewer"))

    def test_only_admin_reads_apikey(self):
        '''only admin may read apiKey; operator/viewer must be denied'''
        self.assertNotEqual([], json_search("apiKey", data, role="admin"))
        self.assertEqual([], json_search("apiKey", data, role="operator"))

    def test_viewer_cannot_read_management_ip(self):
        '''operator may read managementIpAddress, viewer must be denied'''
        self.assertNotEqual([], json_search("managementIpAddress", data, role="operator"))
        self.assertEqual([], json_search("managementIpAddress", data, role="viewer"))


if __name__ == '__main__':
    unittest.main()
