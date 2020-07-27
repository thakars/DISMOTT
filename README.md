# DISMOTT
Developed by Karen Montano and Sushrut Thakar

Distribution System Model Transformation Tool: Used to convert CYME model (CYME 8.XX) to an OpenDSS model. This tool was created at Arizona State University as a part of their projects.

# Usage of the tool
To use the tool the following steps should be addressed:

1. Main code (MainScript_DISMOTT.py):

a. (29) Replace 'Casename' by your casename and create a folder with this name at the same location as input '.txt. files (equipment.txt, load.txt and network.txt).

b. (30 - 32) Write the '.txt' file names accordingly.

c. (72) Choose how the line impedances are calculated: 

  'Definitions': User should know the cable types and their cable and wire parameters, this information may be contained in CYMEDIST. This has to be configured in the 'OpenDSS_Writer_DISMOTT.py' (read points 2 and 3 in 'TODOS.txt').
  
  'Impedances': Impendance data taken directly from Cymedist for cable and wire definitions. User should export the impedaces from CYMEDIST in a '.csv' file to be readed by the code. The '.csv' files readed should have the following column order (columns no specified can have any data):
  Column C: Equipment Id
  F: Phase
  J: #parallel
  U: Concentric Neutral
  V: Line R1 (ohms)
  W: Line X1 (ohms)
  X: Line B1 (uS)
  Y: Line R0 (ohms)
  Z: Line X0 (ohms)
  AA: Line B0 (uS)
  
 d. (73) If 'Impedances' is choses in previous step, write '.csv' file name accordingly. If 'Definitions' is selected, this does not affect.

2. Reader code (Cyme_Reader_DISMOTT.py): There is no change needed*. 

*User should verify that all the sections in their '.txt. files (equipment.txt, load.txt and network.txt) are been readed, if so, no changes are needed. If user find a section is not been reading, user should add the section to be read in the code.

3. Writer code (OpenDSS_Writer_DISMOTT.py):

a. (50 - 69) The OpenDSS writer would create all the files specified here, however, some of them would be blank acording to the impedances definition selected in 1c. 

b. (begining 260) If 'Definitions' is selected in 1c, user shoud use the cable layout there to fill the information necesary for all cable types in their system. 

c. (390) If one or more cables have R1=0, cables name must be spefified here.

d. (549) Select the loadmodel number from CYMEDIST. This can be found in the table [LOAD MODEL INFORMATION] in 'load.txt' file. The defaulf is '1'.  

e. (660) Select the loadmodel name from CYMEDIST. This can be found in the table [LOAD MODEL INFORMATION] in 'load.txt' file. The defaulf is 'DEFAULT' (change 'LoadModelName'). 

# Other information

1. System units is configured in meters.
2. User must install the following packages in Python to use the code: os, collections, math, numpy and cmath.
