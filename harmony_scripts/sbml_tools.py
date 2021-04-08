import libsbml
import logging
import sys
import xml


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
        logging.error("[Error] " + doc.getErrorLog().toString())
        return False

    if convert_function_definitions(doc) != libsbml.LIBSBML_OPERATION_SUCCESS:
        logging.error("[Error] Conversion failed...")
        logging.error("[Error] " + doc.getErrorLog().toString())
        return False

    if output_file is None:
        output_file = sbml_file

    libsbml.writeSBMLToFile(doc, output_file)


def validate_sbml_file(sbml_file):
    doc = libsbml.readSBMLFromFile(sbml_file)

    if doc.getNumErrors(libsbml.LIBSBML_SEV_ERROR) > 0:
        logging.error("[Error] " + doc.getErrorLog().toString())
        return False

    elif doc.getNumErrors(libsbml.LIBSBML_SEV_WARNING) > 0:
        logging.error("[Error] " + doc.getErrorLog().toString())
        return False

    return True


def xpath_expressions_exist(doc, xpaths):
    # type: (libsbml.SBMLDocument, [str]) -> bool
    return True


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
