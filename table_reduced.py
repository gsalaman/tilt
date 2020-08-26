from microbit import *

######################################################################
# get_tilt
#   returns roll and pitch as a tuple. 
#   roll and pitch can only be -1, 0, or +1.
######################################################################
def get_tilt():
  # These are our threshold values...anything above will yield +1
  # and anything below (-thold) will yield -1.  All others 0.
  roll_thold = 200
  pitch_thold = 200
  
  # get the raw values of our accelerometer
  accel_x = accelerometer.get_x()
  accel_y = accelerometer.get_y()
  print("raw accels: ",accel_x,",",accel_y)

  if (accel_x > roll_thold):
      roll = 1
  elif (accel_x < 0-roll_thold):
      roll = -1
  else:
      roll = 0

  if (accel_y > pitch_thold):
      pitch = 1
  elif (accel_y < 0-pitch_thold):
      pitch = -1
  else:
      pitch = 0        

  return (roll, pitch)
        
######################################################################
# get_dir
#    Inputs:  roll and pitch (-1, 0, +1)
#    Outputs:  a number representing direction:
#                      
#                        roll  pitch
#      1 = Up-Left         -1    -1
#      2 = Up               0    -1
#      3 = Up-Right         1    -1
#      4 = Left             -1    0
#      5 = stopped          0     0
#      6 = Right            1     0
#      7 = Down-Left        -1    1
#      8 = Down             0     1
#      9 = Down-Right       1     1
######################################################################
def get_dir(roll, pitch):
  # so here's some cool math:  we can treat both pitch and roll as base-3
  # digits (as they have only 3 possible values).  If you add one to them,
  # they scale to 0-to-2...a proper base 3 digit.  The value of "direction"
  # is really the base 3 number where roll is the "ones" digit and pitch is the
  # "three's" digit.
  # This gives us a "zero based" index...if we want it ones based, we need
  # to add 1.
  return ( ((pitch + 1) * 3) + (roll + 1) + 1 )


######################################################################
# map_node
# 
#   This function takes x and y indexes and returns a "node number".
#   Node number starts at 0 for (0,0), and increases first along the 
#   x axis...1 is (1,0), 2 is (2,0)
#    ...and then along the y axis:  5 is (0,1), 6 is (1,1), up to 24 being
#    4,4.
######################################################################
def map_node(x,y):
  # same cool math as above in get_dir...with a couple differences:
  #   - We're base 5 rather than base 3 (0-4 rather than -1,0,1)
  #   - No offset needed (we start at 0 rather than -1)
  #   - Our output is zero-based rather than ones based
  return( (y*5)+(x) )


######################################################################
# node_to_xy
#
######################################################################
def node_to_xy(node):
  x = node % 5
  y = node // 5

  return(x,y)

# this iteration uses a table-driven lookup. 
# the nodes indexed as 0-24, where 0 maps to 0,0 and 24 4,4.
motion_table = \
[
 # N  UL   U  UR   L   S   R  DL   D  DR
 [ 0, 24, 20,  0,  4,  0,  1,  0,  5,  6],    # node 0
 [ 1, 19, 21,  5,  0,  1,  2,  5,  6,  7],    # node 1
 [ 2, 14, 22, 10,  1,  2,  3,  6,  7,  8],    # node 2
 [ 3,  9, 23, 15,  2,  3,  4,  7,  8,  9],    # node 3
 [ 4,  4, 24, 20,  3,  4,  0,  8,  9,  4],    # node 4
 [ 5, 23,  0,  1,  9,  5,  6,  1, 10, 11],    # node 5
 [ 6,  0,  1,  2,  5,  6,  7, 10, 11, 12],    # node 6
 [ 7,  1,  2,  3,  6,  7,  8, 11, 12, 13],    # node 7
 [ 8,  2,  3,  4,  7,  8,  9, 12, 13, 14],    # node 8
 [ 9,  3,  4, 21,  8,  9,  5, 13, 14,  3],    # node 9
 [10, 22,  5,  6, 14, 10, 11,  2, 15, 16],    # node 10
 [11,  5,  6,  7, 10, 11, 12, 15, 16, 17],    # node 11
 [12,  6,  7,  8, 11, 12, 13, 16, 17, 18],    # node 12
 [13,  7,  8,  9, 12, 13, 14, 17, 18, 19],    # node 13
 [14,  8,  9, 22, 13, 14, 10, 18, 19,  2],    # node 14
 [15, 21, 10, 11, 19, 15, 16,  3, 20, 21],    # node 15
 [16, 10, 11, 12, 15, 16, 17, 20, 21, 22],    # node 16
 [17, 11, 12, 13, 16, 17, 18, 21, 22, 23],    # node 17
 [18, 12, 13, 14, 17, 18, 19, 22, 23, 24],    # node 18
 [19, 13, 14, 23, 18, 19, 15, 23, 24,  1],    # node 19
 [20, 20, 15, 16, 24, 20, 21,  4,  0, 20],    # node 20
 [21, 15, 16, 17, 20, 21, 22,  9,  1, 15],    # node 21
 [22, 16, 17, 18, 21, 22, 23, 14,  2, 10],    # node 22
 [23, 17, 18, 19, 22, 23, 24, 19,  3,  5],    # node 23
 [24, 18, 19, 24, 23, 24, 20, 24,  4,  0]     # node 24
]


######################################################################
# move_pixel 
#   function based rollover to preserve the line the dots are traveling.
#   returns a new x,y tuple.
######################################################################
def move_pixel(curr_x, curr_y, roll, pitch):
    global motion_table

    dir= get_dir(roll, pitch)
    print("dir ", dir)
    curr_node = map_node(curr_x, curr_y)
    print("curr_node ",curr_node)
    new_node = motion_table[curr_node][dir]
    
    return(node_to_xy(new_node))

######################################################################
# main 
######################################################################
current_x = 2
current_y = 2

# used for testing...
#tilt = (1,0)

while True:

  display.set_pixel(current_x, current_y, 0)
  
  #  Comment this line out for test cases
  tilt = get_tilt()

  new_position = move_pixel(current_x, current_y, tilt[0],tilt[1])
  current_x = new_position[0]
  current_y = new_position[1]

  display.set_pixel(current_x, current_y, 9)
  sleep(200)
