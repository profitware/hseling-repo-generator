import unittest

import hseling_api_generator


class HSELing_API_GeneratorTestCase(unittest.TestCase):

    def setUp(self):
        self.app = hseling_api_generator.app.test_client()

    def test_index(self):
        rv = self.app.get('/')
        self.assertIn('Welcome to hseling_api_Generator', rv.data.decode())


if __name__ == '__main__':
    unittest.main()
