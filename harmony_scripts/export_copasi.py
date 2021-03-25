""" This script is for exporting a copasi file, creating SBML / SED-ML files

"""

import basico
import sedml_tools
import COPASI
import os
import logging

dm = COPASI.CRootContainer.addDatamodel()
assert (isinstance(dm, COPASI.CDataModel))


def create_sedml(cps_filename, sedml_file_name, sbml_model_name='model.xml', out_dir='../out', remove_others=True):
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


if __name__ == "__main__":
    cps_file = '../examples/Wilson2012.cps'
    create_sedml(cps_file, 'Wilson2012.sedml', sbml_model_name='Wilson2012.xml')