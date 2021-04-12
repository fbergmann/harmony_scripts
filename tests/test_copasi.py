import unittest
import COPASI
import os

try:
    import test_utils
except ModuleNotFoundError:
    from . import test_utils


class TestCOPASI(unittest.TestCase):

    def setUp(self):
        self.file_name = test_utils.get_example('Orton2009.cps')

        self.assertTrue(os.path.exists(self.file_name))
        self.dm = COPASI.CRootContainer.addDatamodel()
        assert (isinstance(self.dm, COPASI.CDataModel))
        self.assertTrue(self.dm.loadModel(self.file_name))

    def test_export_sedml(self):
        assert (isinstance(self.dm, COPASI.CDataModel))
        sedml = self.dm.exportSEDMLToString(None, 1, 2)
        print(sedml)
        self.assertTrue(self.dm.exportCombineArchive('../out/test_omex.omex', includeCOPASI=True,
                                             includeSEDML=True, includeSBML=True))


if __name__ == "__main__":
    unittest.main()
