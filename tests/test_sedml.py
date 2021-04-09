import unittest
import basico
import COPASI
import libcombine
import libsedml
import libsbml
import os

import harmony_scripts

try:
    import test_utils
except ModuleNotFoundError:
    from . import test_utils


class TestSEDML(unittest.TestCase):

    def setUp(self):
        self.file_name = test_utils.get_example('Wilson2012.sedml')

        self.assertTrue(os.path.exists(self.file_name))
        self.doc = libsedml.readSedMLFromFile(self.file_name)
        self.assertTrue(self.doc.getNumErrors(libsedml.LIBSEDML_SEV_ERROR) == 0)

    def test_get_ids(self):
        self.assertTrue(self.doc.getNumModels() == 1)
        self.assertTrue(harmony_scripts.check_for_duplicated_ids(self.doc))

        # create duplicated model
        model = self.doc.createModel()
        model.setId('model')

        self.assertFalse(harmony_scripts.check_for_duplicated_ids(self.doc, print_warnings=False))

        # remove bad model
        self.doc.removeModel(1)

    def test_xpath(self):
        # get all xpath expressions
        xpaths = harmony_scripts.get_xpath_expressions_from(self.doc)
        self.assertTrue(len(xpaths) > 0)


if __name__ == "__main__":
    unittest.main()
