""" functions needed for modifying sbml files

"""
import libsedml
import logging
import os


def rename_model(sedml_file_name, old_name, new_name, output_file=None):
    """ renames a model source in the SED-ML file

    :param sedml_file_name: full path to the sedml file
    :param old_name: old model source to be renamed
    :param new_name: new model source
    :param output_file: optional target filename where the new sed-ml file will be saved (otherwise the original
          one will be overwritten)
    :return: None
    """
    doc = libsedml.readSedMLFromFile(sedml_file_name)
    assert (isinstance(doc, libsedml.SedDocument))
    for i in range(doc.getNumModels()):
        model = doc.getModel(i)
        assert (isinstance(model, libsedml.SedModel))

        if model.getSource() == old_name:
            model.setSource(new_name)

    if output_file is None:
        output_file = sedml_file_name

    libsedml.writeSedMLToFile(doc, output_file)


def check_files_exist(sedml_file_name):
    """ Utility function that checks whether all the model sources do exist

    :param sedml_file_name: full path to a sedml file
    :return: True, if all model sources exist, False otherwise.
    """
    doc = libsedml.readSedMLFromFile(sedml_file_name)
    assert (isinstance(doc, libsedml.SedDocument))

    name = os.path.splitext(os.path.basename(sedml_file_name))[0]
    directory = os.path.dirname(sedml_file_name)

    model_ids = [model.getId() for model in doc.getListOfModels()]
    result = True
    for i in range(doc.getNumModels()):
        model = doc.getModel(i)
        assert (isinstance(model, libsedml.SedModel))

        if model.getSource() in model_ids:
            # derived model skip
            continue

        model_file_name = os.path.join(directory, model.getSource())

        if not os.path.exists(model_file_name):
            logging.error(f'missing model file {model.getSource()} in sedml-file {name}')
            result = False

    return result
