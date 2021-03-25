## HARMONY scripts
This repository contains a number of example python scripts that make it easier to deal with Combine Archives


### Get started
Clone the repository, create a new virtual environment. And install the requirements: 

	pip install -r requirements.txt

make changes, commit and have fun. Or add issues on what would be nice to have. 

### Command Line tools
You could also just install the package and use it straight from the command line. Again i'd use a virtual environment for that: 

	python3 -m venv venv
	. ./venv/bin/activate

then install with: 

	pip install git+git://github.com/fbergmann/harmony_scripts#egg=harmony_scripts

this gives you the following two command line scripts: 

 * `check_omex`: just checks the given omex file, to see if all files are in there and if it contains SED-ML files whether those contain all models 
 * `export_copasi_sedml`: given a copasi file, this lets you export it as SED-ML, allowing to specify the SBML filename and where to place it. 

To test whether the installation works you can run: 

	(venv) frank@BQFRANK:/tmp#  python -m harmony_scripts
 	HARMONY utility scripts

        Uses:
            COPASI 4.30.240
            libSBML 5.19.0
            libSEDML 2.0.16
            libCOMBINE 0.2.7

        Provides the command line functions:

            check_omex <omex file> <tempdir>
            export_copasi_sedml <cps file file> <sedml_name> <sbml_name> <output_dir>
		 


### Examples `check_omex`

Called without arg: 

	(venv) frank@BQFRANK:/tmp# check_omex
	usage check_omex <omex file> <tempdir>

Called with arg: 

	(venv) frank@BQFRANK:/tmp# check_omex ./harmony_scripts/examples/BIOMD0000000791-20210325-094855.omex /tmp
	ERROR:root:missing model file model.xml

Testing a biomodel: 

	(venv) frank@BQFRANK:/tmp#  curl -L http://www.ebi.ac.uk/biomodels/model/download/BIOMD0000000001 -o BIOMD0000000001.omex
	  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                   	 Dload  Upload   Total   Spent    Left  Speed
  	  0     0    0     0    0     0      0      0 --:--:-- --:--:-- --:--:--     0
	100  277k    0  277k    0     0   131k      0 --:--:--  0:00:02 --:--:--  160k
	(venv) frank@BQFRANK:/tmp#  check_omex ./BIOMD0000000001.omex /tmp
	(venv) frank@BQFRANK:/tmp# 

And another test:

	(venv) frank@BQFRANK:/tmp#  curl -L http://www.ebi.ac.uk/biomodels/model/download/BIOMD0000000791 -o BIOMD0000000791.omex
	  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 	 Dload  Upload   Total   Spent    Left  Speed
	  0     0    0     0    0     0      0      0 --:--:-- --:--:-- --:--:--     0
	100 15980    0 15980    0     0  10760      0 --:--:--  0:00:01 --:--:--  200k
	(venv) frank@BQFRANK:/tmp# check_omex ./BIOMD0000000791.omex /tmp
	ERROR:root:missing model file model.xml in sedml-file Wilson2012	
	(venv) frank@BQFRANK:/tmp# 


### Examples `export_copasi_sedml`

Called without arg: 

	(venv) frank@BQFRANK:/tmp# export_copasi_sedml
	usage export_copasi_sedml <cps file file> <sedml_name> <sbml_name> <output_dir>

Called with arg: 

	(venv) frank@BQFRANK:/tmp# export_copasi_sedml ./harmony_scripts/examples/Wilson2012.cps Wilson2012.sedml Wilson2012.xml /tmp
	
	(venv) frank@BQFRANK:/tmp# ls *Wi*
	Wilson2012.sedml  Wilson2012.xml	

	(venv) frank@BQFRANK:/tmp# cat Wilson2012.sedml  | grep "<model"
    <model id="model" language="urn:sedml:language:sbml" source="Wilson2012.xml"/>

## License 
Just as COPASI, the packages available on this page are provided under the 
[Artistic License 2.0](http://copasi.org/Download/License/), 
which is an [OSI](http://www.opensource.org/) approved license. This license 
allows non-commercial and commercial use free of charge.
