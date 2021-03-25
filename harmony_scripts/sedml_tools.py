""" functions needed for modifying sbml files

"""
import libsedml
import logging
import os


def rename_model(sedml_file_name, old_name, new_name, output_file=None):
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
