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


# this iteration uses a table-driven lookup...we've got a 3-d table where
# the indexes are curr_x, curr_y, and dir...which returns a tuple for the
# new node.
motion_table = \
    [
      [
        # Node   UL      U      UR     L      S      R      DL     D     DR
        [(0,0), (4,4), (0,4), (1,4), (4,0), (0,0), (1,0), (4,1), (0,1), (1,1)], 
        [(0,1), (4,0), (0,0), (1,0), (4,1), (0,1), (1,1), (4,2), (0,2), (1,2)],
        [(0,2), (4,1), (0,1), (1,1), (4,2), (0,2), (1,2), (4,3), (0,3), (1,3)],
        [(0,3), (4,2), (0,2), (1,2), (4,3), (0,3), (1,3), (4,4), (0,4), (1,4)],
        [(0,4), (4,3), (0,3), (1,3), (4,4), (0,4), (1,4), (4,0), (0,0), (1,0)]
      ],  
      [
        # Node   UL      U      UR     L      S      R      DL     D     DR
        [(1,0), (0,4), (1,4), (2,4), (0,0), (1,0), (2,0), (0,1), (1,1), (2,1)],
        [(1,1), (0,0), (1,0), (2,0), (0,1), (1,1), (2,1), (0,2), (1,2), (2,2)],
        [(1,2), (0,1), (1,1), (2,1), (0,2), (1,2), (2,2), (0,3), (1,3), (2,3)],
        [(1,3), (0,2), (1,2), (2,2), (0,3), (1,3), (2,3), (0,4), (1,4), (2,4)],
        [(1,4), (0,3), (1,3), (2,3), (0,4), (1,4), (2,4), (0,0), (1,0), (2,0)]
      ],
      [
        # Node   UL      U      UR     L      S      R      DL     D     DR
        [(2,0), (1,4), (2,4), (3,4), (1,0), (2,0), (3,0), (1,1), (2,1), (3,1)],
        [(2,1), (1,0), (2,0), (3,0), (1,1), (2,1), (3,1), (1,2), (2,2), (3,2)],
        [(2,2), (1,1), (2,1), (3,1), (1,2), (2,2), (3,2), (1,3), (2,3), (3,3)],
        [(2,3), (1,2), (2,2), (3,2), (1,3), (2,3), (3,3), (1,4), (2,4), (3,4)],
        [(2,4), (1,3), (2,3), (3,3), (1,4), (2,4), (3,4), (1,0), (2,0), (3,0)]
      ],
      [
        # Node   UL      U      UR     L      S      R      DL     D     DR
        [(3,0), (2,4), (3,4), (4,4), (2,0), (3,0), (4,0), (2,1), (3,1), (4,1)], 
        [(3,1), (2,0), (3,0), (4,0), (2,1), (3,1), (4,1), (2,2), (3,2), (4,2)],
        [(3,2), (2,1), (3,1), (4,1), (2,2), (3,2), (4,2), (2,3), (3,3), (4,3)],
        [(3,3), (2,2), (3,2), (4,2), (2,3), (3,3), (4,3), (2,4), (3,4), (4,4)],
        [(3,4), (2,3), (3,3), (4,3), (2,4), (3,4), (4,4), (2,0), (3,0), (4,0)]
      ],
      [
        # Node   UL      U      UR     L      S      R      DL     D     DR
        [(4,0), (4,0), (4,4), (0,4), (3,0), (4,0), (0,0), (3,1), (4,1), (4,0)],
        [(4,1), (3,0), (4,0), (1,4), (3,1), (4,1), (0,1), (3,2), (4,2), (3,0)],
        [(4,2), (3,1), (4,1), (2,4), (3,2), (4,2), (0,2), (3,3), (4,3), (2,0)],
        [(4,3), (3,2), (4,2), (3,4), (3,3), (4,3), (0,3), (3,4), (4,4), (1,0)],
        [(4,4), (3,3), (4,3), (4,4), (3,4), (4,4), (0,4), (4,4), (4,0), (0,0)]
      ]
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
    newxy = motion_table[curr_x][curr_y][dir]

    return(newxy)

######################################################################
# main 
######################################################################
current_x = 2
current_y = 2

# used for testing...
tilt = (0,0)

while True:

  display.set_pixel(current_x, current_y, 0)
  
  #  Comment this line out for test cases
  #tilt = get_tilt()

  new_position = move_pixel(current_x, current_y, tilt[0],tilt[1])
  current_x = new_position[0]
  current_y = new_position[1]

  display.set_pixel(current_x, current_y, 9)
  sleep(200)
