""" Utility methods for COMBINE archives

"""

import libcombine
import logging
import os
import shutil
import sys

try:
    import sedml_tools
    import sbml_tools
except ImportError:
    from . import sedml_tools
    from . import sbml_tools


def check_archive(archive_file, tempdir='../out'):
    """ Checks the given COMBINE archive

    :param archive_file: combine archive
    :param tempdir: temp folder where to extract files too
    :return: boolean indicating whether issues were found (False), or all is good (True)
    """
    archive = libcombine.CombineArchive()
    archive.initializeFromArchive(archive_file)

    name = os.path.splitext(os.path.basename(archive_file))[0]

    temp_dir = os.path.join(tempdir, name)
    if os.path.exists(temp_dir):
        logging.error('remove existing temp dir {}'.format(temp_dir))

    # print files in manifest
    manifest = archive.getManifest()
    expected_locations = []
    sedml_files = []
    sbml_files = []
    assert (isinstance(manifest, libcombine.CaOmexManifest))

    for i in range(manifest.getNumContents()):
        entry = manifest.getContent(i)
        assert (isinstance(entry, libcombine.CaContent))

        # print(f'location: {entry.getLocation()}, master: {entry.getMaster()}, format: {entry.getFormat()}')

        expected_locations.append(entry.getLocation())
        if 'identifiers.org/combine.specifications/sed-ml' in entry.getFormat():
            sedml_files.append(entry.getLocation())
        if 'identifiers.org/combine.specifications/sbml' in entry.getFormat():
            sbml_files.append(entry.getLocation())

    # extract archive to see if all files are in the manifest
    archive.extractTo(temp_dir)

    result = True
    # check for files not included in manifest
    for root, dirs, files in os.walk(temp_dir):
        for file in files:
            if file not in expected_locations and file not in ['manifest.xml', 'metadata.rdf']:
                logging.error(f'Encountered unexpected file in archive "{file}" in archive "{name}"')
                result = False

    # check SED-ML files:
    for sedml_file in sedml_files:
        valid, xpath_expressions, model_file = sedml_tools.check_files_exist(os.path.join(temp_dir, sedml_file))
        result = result and valid

        if len(xpath_expressions) > 0 and os.path.exists(model_file):
            sbml_tools.validate_sbml_file(model_file, xpath_expressions)

        # check that SBML files are valid
    for sbml_file in sbml_files:
        sbml_tools.validate_sbml_file(os.path.join(temp_dir, sbml_file))

    # cleanup
    shutil.rmtree(temp_dir)
    return result


def check_omex():
    # archive_file = '../examples/BIOMD0000000791-20210325-094855.omex'
    # check_archive(archive_file)

    if len(sys.argv) < 3:
        print('usage: check_omex <omex file> <tempdir>')
        sys.exit(1)

    sys.exit(0 if check_archive(sys.argv[1], sys.argv[2]) else 1)


if __name__ == "__main__":
    check_omex()
