import libsbml
import logging
import sys
from lxml import etree


def convert_function_definitions(doc):
    props = libsbml.ConversionProperties()
    props.addOption("expandFunctionDefinitions", True)
    return doc.convert(props)


def inline_function_definitions(sbml_file, output_file=None):
    """ Inlines all function definitions in the given SBML file
    
    :param sbml_file: the sbml file to load
    :param output_file: the output file where to write the SBML to
    :return: 
    """

    doc = libsbml.readSBMLFromFile(sbml_file)
    if doc.getNumErrors(libsbml.LIBSBML_SEV_ERROR) > 0:
        logging.error("invalid SBML document " + doc.getErrorLog().toString())
        return False

    if convert_function_definitions(doc) != libsbml.LIBSBML_OPERATION_SUCCESS:
        logging.error("Conversion failed with: " + doc.getErrorLog().toString())
        return False

    if output_file is None:
        output_file = sbml_file

    libsbml.writeSBMLToFile(doc, output_file)


def validate_sbml_file(sbml_file, xpath_expressions=None):
    doc = libsbml.readSBMLFromFile(sbml_file)

    if doc.getNumErrors(libsbml.LIBSBML_SEV_ERROR) > 0:
        logging.error(f"file {sbml_file} had errors: " + doc.getErrorLog().toString())
        return False

    elif doc.getNumErrors(libsbml.LIBSBML_SEV_WARNING) > 0:
        logging.warning(f"file {sbml_file} had warnings:  " + doc.getErrorLog().toString())

    if xpath_expressions is not None:
        return xpath_expressions_exist(doc, xpath_expressions)

    return True


class _CopasiAnnotationFilter(libsbml.ElementFilter):

    def __init__(self):
        libsbml.ElementFilter.__init__(self)

    def filter(self, element):
        assert(isinstance(element, libsbml.SBase))
        if element.isSetMetaId():
            node = element.getAnnotation()
            for i in range(node.getNumChildren()):
                child = node.getChild(i)
                if child.getURI() == 'http://www.copasi.org/static/sbml':
                    return True
        return False


def remove_copasi_annotations(doc):
    # type: (libsbml.SBMLDocument) -> int
    """Removes the COPASI RDF annotations from the given SBML document"""
    num_removed = 0
    model = doc.getModel()
    assert(isinstance(model, libsbml.Model))
    annotated_list = model.getListOfAllElements(_CopasiAnnotationFilter())

    for element in annotated_list:
        node = element.getAnnotation()
        assert(isinstance(node, libsbml.XMLNode))
        num_children = node.getNumChildren()
        for i in reversed(range(num_children)):
            child = node.getChild(i)
            if child.getURI() == 'http://www.copasi.org/static/sbml':
                node.removeChild(i)
                num_removed += 1

    return num_removed


def xpath_expressions_exist(doc, xpath_expressions):
    # type: (libsbml.SBMLDocument, List[str]) -> bool
    sbml = libsbml.writeSBMLToString(doc)
    tree = etree.fromstring(sbml.encode('utf-8'))
    result = True
    for xpath in xpath_expressions:
        if ':' not in xpath:
            logging.warning(f"no prefix used in xpath expression: {xpath} this likely cannot be resolved")
        try:
            elements = tree.xpath(xpath, namespaces={'sbml': doc.getSBMLNamespaces().getURI()})
            num_elements = len(elements)
            if num_elements == 0:
                logging.error(f"no match for xpath expression: {xpath}")
                result = False
            if num_elements > 1:
                logging.warning(f"more than one match for xpath expression, this is not supported by many tools: {xpath}")
        except TypeError:
            logging.error(f"invalid xpath expression: {xpath}")
            result = False
    return result


def validate_sbml_main():
    if len(sys.argv) < 2:
        print("usage: check_sbml <sbml file>")
        sys.exit(1)

    sys.exit(0 if validate_sbml_file(sys.argv[1]) else 1)


def inline_function_definitions_main():
    if len(sys.argv) < 2:
        print("usage: inline_function_definitions <sbml file> [output file]")
        sys.exit(1)

    if len(sys.argv) > 2:
        inline_function_definitions(sys.argv[1], sys.argv[2])
    else:
        inline_function_definitions(sys.argv[1])


if __name__ == "__main__":
    inline_function_definitions_main()
