""" functions needed for modifying sbml files

"""
import libsedml


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