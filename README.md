# imageQA
QA script to check image logs

Usage:

python imageQA.py <inputfile> {<outputfile>}

if outputfile is not specified, the output is shown stdout (eg terminal)

Input:

Input file is expected to be a CSV file with the following fields (in any order)
time - Timestamp (date/string)
image - Image name (string)
x, y, z - Position of the device in meters (float)
qx, qy, qz, qw - The orientation of the device as a quaternion (float)
distance - The distance to the previous image in meters (float)
angle - The angle difference to the previous image in degrees (float)
  
N.B. 
  
1. We are not checking the types of the input of the completeness of the file
  
Output:
A CSV file (or std output) if a form:

Condition - intial image ('Initial'), triggered by distance over 0.1m ('Distance'), by angle over 20 degrees ('Angle'), both conditions ('Both') or neither ('Unknown')
Image - image name as provided in the input file
Distance - distance as provided in the input file
Angle - angle as provided in the input file
DQ_Comment - pipe (|) separated data quality issues found in the row ('|ok|' if no issues found)
  
List of DQ issues checked:
  
angle_over180 - angle value is over 180, the 360-angle value will be used for further calculations (the output will contain the original value)
angle_norm - quaternion vector is not normalized (sum of squares of vector components is not equal to 1)
distance_calc - distance is different from the size based on the components (calc_distance = sqrt(delta_x^2 + delta_y^2 + delta_z^2)
angle_calc - angle is different from the value based on the components (calc_angle = 180/pi * acos (2<q, prev_q>^2 -1))
N.B. all comparison are done with the precision of 0.01 of corresponding units
  
Further checks can added to the framework (e.g. distance, angle are not negative, image name numbers are subsequent, numerical values of a right type, etc.)  

