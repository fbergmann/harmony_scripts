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

    if doc.getNumErrors(libsedml.LIBSEDML_SEV_ERROR) > 0:
        logging.error('invalid SED-ML document: ' + doc.getErrorLog().toString())

    elif doc.getNumErrors(libsedml.LIBSEDML_SEV_WARNING) > 0:
        logging.warning('warnings in SED-ML document: ' + doc.getErrorLog().toString())

    name = os.path.splitext(os.path.basename(sedml_file_name))[0]
    directory = os.path.dirname(sedml_file_name)

    model_ids = [model.getId() for model in doc.getListOfModels()]
    result = True
    model_file_name = ''
    for i in range(doc.getNumModels()):
        model = doc.getModel(i)
        assert (isinstance(model, libsedml.SedModel))

        if model.getSource() in model_ids:
            # derived model skip
            continue

        model_file_name = os.path.join(directory, model.getSource())

        if not os.path.exists(model_file_name):
            logging.error(f'missing model file "{model.getSource()}" in sedml-file "{name}"')
            result = False

        if ':' in model_file_name and not model_file_name.startswith('urn:'):
            logging.warning(f'source {model.getSource()} contains colon, and is likely not to resolve on all platforms')

    check_for_duplicated_ids(doc, True)

    xpath_expressions = get_xpath_expressions_from(doc)

    return result, xpath_expressions, model_file_name


class _IdFilter(libsedml.SedElementFilter):

    def __init__(self):
        libsedml.SedElementFilter.__init__(self)
        self.ids = []
        self.ids_per_type = {}
        self.messages = []
        self.duplicated_ids = []

    def filter(self, element):
        assert(isinstance(element, libsedml.SedBase))
        if element.isSetId():
            tc = element.getTypeCode()
            type_string = libsedml.SedTypeCode_toString(tc)
            sed_id = element.getId()
            if type_string not in self.ids_per_type:
                self.ids_per_type[type_string] = []
            if sed_id in self.ids:
                self.duplicated_ids.append(sed_id)
                self.messages.append(f'Duplicated id "{sed_id}" of type "{type_string}"')

            self.ids.append(sed_id)
            self.ids_per_type[type_string].append(sed_id)

        return False


def check_for_duplicated_ids(doc, print_warnings=False):
    # type: (libsedml.SedDocument) -> bool

    filter = _IdFilter()

    elements = doc.getListOfAllElements(filter)

    result = len(filter.messages) == 0

    if print_warnings:
        for message in filter.messages:
            logging.warning(message)

    return result


class _XpathFilter(libsedml.SedElementFilter):

    def __init__(self):
        libsedml.SedElementFilter.__init__(self)
        self.xpath_expressions = []

    def filter(self, element):
        assert(isinstance(element, libsedml.SedBase))
        tc = element.getTypeCode()

        if isinstance(element, libsedml.SedVariable) or isinstance(element, libsedml.SedChange):
            if element.isSetTarget():
                target = element.getTarget()
                if target not in self.xpath_expressions:
                    self.xpath_expressions.append(target)
        return False


def get_xpath_expressions_from(doc):
    # type: (libsedml.SedDocument) -> [str]

    xpath_filter = _XpathFilter()

    doc.getListOfAllElements(xpath_filter)

    return xpath_filter.xpath_expressions


if __name__ == "__main__":
    pass

