#!/usr/bin/python

import sys, getopt
import csv
import math

def main(argv):
    # names of input and output files
    # if outputfile is missing - print out the results
    inputfile, outputfile = '', ''

    try:
        opts, args = getopt.getopt(argv,"i:o:")
    except getopt.GetoptError:
        print('$argv[0] -i <inputfile> {-o <outputfile>}')
        sys.exit(2)
    for opt, arg in opts:
        if opt == "-i":
            inputfile = arg
        elif opt == "-o":
            outputfile = arg

    if (inputfile == ''):
        print('$argv[0] -i <inputfile> {-o <outputfile>]}')
        sys.exit(2)

    with open(inputfile, newline='') as csvin:
        if outputfile != '':
            csvout = open(outputfile, 'w')
            writer = csv.writer(csvout)
            writer.writerow(['Condition', 'Image', 'Distance', 'Angle', 'DQ_Comment'])
        else:
            print ('Condition, Image, Distance, Angle, DQ_Comment')

        header = [h.strip() for h in csvin.readline().split(',')]
        reader = csv.DictReader(csvin, fieldnames=header)
        row_num = 0
        for r in reader:

            dq = '|' # will be writing any data issues here
            # distance
            distance = abs(float(r['distance']))
            #angle
            original_angle = abs(float(r['angle']))
            if original_angle >= 180:
                dq += "angle_over180|"
                angle = abs(angle) % 360
                angle = min(angle, 360-angle)
            else:
                angle = original_angle
            # set condition based on distance and angle
            if (row_num == 0):
                condition = 'Initial'
            elif abs(distance) >= 0.1 and abs(angle) > 20:
                condition = 'Both'
            elif abs(distance) >= 0.1:
                condition = 'Distance'
            elif abs(angle) > 20:
                condition = 'Angle'
            else:
                condition = 'Unknown'

            # verify distance and angle calcs
            # store previous values of components
            if (row_num > 0):
                px, py, pz = x, y, z
                pqx, pqy, pqz, pqw = qx, qy, qz, qw

            # read component values
            calc_distance, calc_angle, norm = 0, 0, 0
            x, y, z = float(r['x']), float(r['y']), float(r['z'])
            qx, qy, qz, qw = float(r['qx']), float(r['qy']), float(r['qz']), float(r['qw'])

            # make sure q-components are normalized (<q, q> == 1)
            norm = qx*qx + qy*qy + qz*qz + qw*qw
            if (row_num > 0):
                # check distance calc d = sqrt(sum(xi^2))
                calc_distance = math.sqrt((x-px)**2 +(y-py)**2 +(z-pz)**2)
                # check angle calc angle = (180/pi) acos (2 <pq, q> ^2 -1)
                calc_angle = 180/math.pi * math.acos(-1 + 2 * (qx * pqx + qy * pqy + qz * pqz + qw * pqw)**2)

            # write data issue (if any)
            # precision 0.01 (units)
            if abs(distance - calc_distance) > 0.01:
                dq += 'dist_calc|'
            if abs(angle - calc_angle) > 0.01:
                dq += 'angle_calc|'
            if abs(norm - 1) > 0.01:
                dq += 'angle_norm|'
            # no issues detected
            if dq == '|':
                dq = '|ok|'

            if outputfile == '':
                print (condition, r['image'], distance, original_angle, dq)
            else:
                writer.writerow ([condition, r['image'], distance, original_angle, dq])

            row_num+=1
        # end of for loop

        if outputfile != '':
            csvout.close()


if __name__ == "__main__":
    main(sys.argv[1:])
