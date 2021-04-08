import unittest

import os


def get_example(file_name, example_dir='examples'):
    if os.path.exists(example_dir):
        example_file = os.path.join(example_dir, file_name)
    elif os.path.exists('../' + example_dir):
        example_file = os.path.join('..', example_dir, file_name)
    else:
        raise ValueError("Couldn't find example dir")

    if not os.path.exists(example_file):
        raise ValueError('No such example')

    return os.path.abspath(example_file)


class TestUtils(unittest.TestCase):

    def setUp(self):
        pass

    def test_get_examples(self):
        example = get_example('Wilson2012.xml')
        self.assertTrue(example)

        try:
            get_example('not_there.xml')
            self.fail('should not have gotten that file')
        except ValueError:
            pass

        try:
            get_example('Wilson2012.xml', example_dir='')
            self.fail('should not have gotten that file')
        except ValueError:
            pass


if __name__ == "__main__":
    unittest.main()
