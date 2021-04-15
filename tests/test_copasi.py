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
        if os.path.exists('./out/test_omex.omex'):
            os.remove('./out/test_omex.omex')
        self.dm.exportCombineArchive('./out/test_omex.omex',
                                     includeCOPASI=True,
                                     includeSEDML=True,
                                     includeSBML=True,
                                     includeData=True)

        self.assertTrue(COPASI.CCopasiMessage.getHighestSeverity() <= COPASI.CCopasiMessage.WARNING)


if __name__ == "__main__":
    unittest.main()
