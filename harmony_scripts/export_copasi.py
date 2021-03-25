""" This script is for exporting a copasi file, creating SBML / SED-ML files

"""

import COPASI
import os
import logging
import sys

try:
    import sedml_tools
except ImportError:
    from . import sedml_tools


dm = COPASI.CRootContainer.addDatamodel()
assert (isinstance(dm, COPASI.CDataModel))


def create_sedml(cps_filename, sedml_file_name, sbml_model_name='model.xml', out_dir='../out', remove_others=False):
    """ Creates a new sedml file and sbml model in the specified folder

    :param cps_filename: full path to the COPASI file
    :param sedml_file_name: target sbml filename (basename only)
    :param sbml_model_name: target sbml filename (basename only), optional will be 'model.xml' if not defined
    :param out_dir: target output folder (defaults to '../out')
    :param remove_others: should a 'model.xml' file already exist in the output folder, this file will be removed
                          if remove_others is True, otherwise export will be stopped with error.
    :return: tuple of sedml filename and sbml filename created
    """
    if not dm.loadModel(cps_filename):
        raise ValueError(COPASI.CCopasiMessage.getAllMessageText())

    print(dm.getModel().getObjectName())

    default_output_sbml_file = os.path.join(out_dir, 'model.xml')
    output_sbml_file = default_output_sbml_file

    if os.path.exists(default_output_sbml_file):
        if remove_others:
            os.remove(default_output_sbml_file)
        else:
            logging.error('model.xml already exists in output dir, please remove')
            return

    output_sedml_file = os.path.join(out_dir, sedml_file_name)

    if not dm.exportSEDML(output_sedml_file, True, 1, 3):
        raise ValueError(COPASI.CCopasiMessage.getAllMessageText())

    if sbml_model_name != 'model.xml':
        # rename file
        output_sbml_file = os.path.join(out_dir, sbml_model_name)
        os.rename(default_output_sbml_file, output_sbml_file)

        # rename file in sedml
        sedml_tools.rename_model(output_sedml_file, 'model.xml', sbml_model_name)

    return output_sedml_file, output_sbml_file


def export_sedml():
    """ Entry point for copasi sedml export from command line
    """
    # cps_file = '../examples/Wilson2012.cps'
    # create_sedml(cps_file, 'Wilson2012.sedml', sbml_model_name='Wilson2012.xml')

    if len(sys.argv) < 4:
        print('usage: export_copasi_sedml <cps file file> <sedml_name> <sbml_name> <output_dir>')
        sys.exit(1)

    create_sedml(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
    sys.exit(0)


if __name__ == "__main__":
    export_sedml()
