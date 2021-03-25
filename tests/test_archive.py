import unittest
import basico
import COPASI
import libcombine
import libsedml
import libsbml
import os


class TestExample(unittest.TestCase):

    def setUp(self):
        self.archive = libcombine.CombineArchive()
        file_name = './examples/BIOMD0000000791-20210325-094855.omex'
        if not os.path.exists(file_name):
            file_name = '.' + file_name

        self.assertTrue(os.path.exists(file_name))
        self.archive.initializeFromArchive(file_name)

    def test_archive_read(self):
        self.assertTrue(self.archive is not None)
        manifest = self.archive.getManifest()
        assert (isinstance(manifest, libcombine.CaOmexManifest))
        self.assertTrue(manifest.getNumContents() > 0)


if __name__ == "__main__":
    unittest.main()
