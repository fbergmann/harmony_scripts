import COPASI
import libsbml
import libsedml
import libcombine

if __name__ == '__main__':
    print(f""" HARMONY utility scripts
        
        Uses: 
            COPASI {COPASI.__version__}
            libSBML {libsbml.__version__}
            libSEDML {libsedml.__version__}
            libCOMBINE {libcombine.__version__}

        Provides the command line functions:
            
            check_omex <omex file> <tempdir>
            export_copasi_sedml <cps file file> <sedml_name> <sbml_name> <output_dir>

    """)

