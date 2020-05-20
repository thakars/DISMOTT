# DISMOTT
Distribution System Model Transformation Tool: Used to convert CYME model (CYME 8.XX) to an OpenDSS model. This tool was created at Arizona State University for their projects.

# Usage of the tool
To use the tool the following steps should be addressed:

1. Main code:

a. (29) Replace 'Casename' by your casename and create a folder with this name at the same location as input '.txt. files (equipment.txt, load.txt and network.txt).

b. (30 - 32) Write the '.txt' file names accordingly.

c. (72) Choose how the line impedances are calculated: 

  'Definitions': User should know the cable types and their cable and wire parameters, this information may be contained in CYMEDIST. This has to be configured in the 'OpenDSS_Writer_DISMOTT.py' (read points 2 and 3 in 'TODOS.txt').
  
  'Impedances': Impendance data taken directly from Cymedist for cable and wire definitions. User should export the impedaces from CYMEDIST in a '.csv' file to be readed by the code.
  
 d. (73) If 'Impedances' is choses in previous step, write '.csv' file name accordingly. If 'Definitions' is selected, this does not affect.

2. Reader code: There is no change needed*. 

*User should verify that all the sections in their '.txt. files (equipment.txt, load.txt and network.txt) are been readed, if so, no changes are needed. If user find a section is not been reading, user should add the section to be read in the code.

# Other information
