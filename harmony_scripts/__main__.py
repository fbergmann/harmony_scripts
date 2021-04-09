import COPASI
import libsbml
import libsedml
import libcombine
import sys

if __name__ == '__main__':
    print(f""" HARMONY utility scripts
        
        Uses: 
            COPASI     {COPASI.__version__}
            libSBML    {libsbml.__version__}
            libSEDML   {libsedml.__version__}
            libCOMBINE {libcombine.__version__}

        Provides the command line functions:
            
            check_omex <omex file> <tempdir>
            export_copasi_sedml <cps file file> <sedml_name> <sbml_name> <output_dir>
            check_sbml <sbml_file>
            sbml_inline_function_definitions <sbml_file> [output_sbml_file]

    """)
    sys.exit(0)
