# Installation procedure

*This installation procedure was tested with success on Mac OS X Mountain Lion (10.8) and on Mac OS X Yosemite (10.10). This installation procedure FAILED on Mac OS X Sierra (10.12). If ppv1 can be installed on Mac OS X Sierra is still an open problem.*

## Prerequisites
* gfortran. See https://gitlab.com/Takuvik/resources_public/blob/master/Gfortran.md.
* SWIG. See https://gitlab.com/Takuvik/resources_public/blob/master/swig.md.
* Anaconda Python 2.7. See https://gitlab.com/Takuvik/resources_public/blob/master/Python2Anaconda.md.

## Procedure
1. Build.
    1. Change directory to the directory where ppv1 was cloned.
    2. `cd ppv1/trunk/Source`
    3. `make clean`
    4. `make`
2. Test.
    1. `./test_remote_sensing.py`
    
# Examples

## Easy
* See run_oneimage.py for an example on how to generate one image using the machine taku-eirikr.


## Intermediate
* See run_map.sh for an example on how to generate a map to test the image generated above using the machine taku-eirikr.
  * You will need GMT4. See https://gitlab.com/Takuvik/resources_public/blob/master/GMT4.md.

## Advanced
* See SLURM_run_all.sh for an example on how to generate one image using the supercomputer katak. To pull and push the files automatically between the machine taku-eirikr and the supercomputer katak:
  * Remove the need for a password to scp on katak to transfer a file between taku-eirikr and katak. See http://www.linuxjournal.com/article/8600.
  * In the function write_outfiles_from_to(...) of write_outfiles_from_to.py, change the variable **user** for your own username on taku-eirikr.
* Note.
  * Build on katak with
    `make -f Makefile_katak`
  
# Other general information

See https://gitlab.com/Takuvik/ppv1/blob/master/trunk/Source/KnowledgeTransfer_v07.pptx.