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


class TestSBML(unittest.TestCase):

    def setUp(self):
        self.file_name = test_utils.get_example('Wilson2012.xml')

        self.assertTrue(os.path.exists(self.file_name))
        self.doc = libsbml.readSBMLFromFile(self.file_name)
        self.assertTrue(self.doc.getModel() is not None)
        self.assertTrue(self.doc.getNumErrors(libsbml.LIBSBML_SEV_ERROR) == 0)

    def test_inline_function_definitions(self):
        self.assertTrue(self.doc.getModel().getNumFunctionDefinitions() > 0)
        self.assertTrue(harmony_scripts.convert_function_definitions(self.doc) == libsbml.LIBSBML_OPERATION_SUCCESS)
        self.assertTrue(self.doc.getModel().getNumFunctionDefinitions() == 0)

    def test_model_has_xpath_expressions(self):
        xpaths = ["/sbml:sbml/sbml:model/sbml:listOfSpecies/sbml:species[@id='T']",
                  "/sbml:sbml/sbml:model/sbml:listOfSpecies/sbml:species[@id='B']",
                  "/sbml:sbml/sbml:model/sbml:listOfSpecies/sbml:species[@id='E']",
                  "/sbml:sbml/sbml:model/sbml:listOfSpecies/sbml:species[@id='R']"]

        self.assertTrue(harmony_scripts.xpath_expressions_exist(self.doc, xpaths))

    def test_remove_copasi_annotations(self):
        self.assertTrue(harmony_scripts.sbml_tools.remove_copasi_annotations(self.doc) == 37)


if __name__ == "__main__":
    unittest.main()
