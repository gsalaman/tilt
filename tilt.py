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
# move_pixel 
#   function based rollover to preserve the line the dots are traveling.
#   returns a new x,y tuple.
######################################################################
def move_pixel(curr_x, curr_y, roll, pitch):
    # First, we need to calculate "slope" based on our pitch and roll.
    # Since 0,0 is on the top-left corner, positive slope is a line down and right
    #    (or up and left)
    # Negative slope is a line up and right (or down and left)
    # Zero slope means we're going straight left-right or up-down.  
    #   (yes, one of those should really be infinity.  Deal with it.)
    slope = roll * pitch
    
    # Move the x and y one dot.  We may go off the screen...we'll adjust that next.
    new_x = curr_x + roll
    new_y = curr_y + pitch

    # first set of roll-over cases:  just up-down or left-right...no diagonals.
    if (slope == 0):
        if (new_x > 4):
            new_x = 0
        if (new_x < 0):
            new_x = 4
        if (new_y > 4):
            new_y = 0
        if (new_y < 0):
            new_y = 4
    
    # The rest of these roll-over cases are a little tricker...if we're going 
    # diagonally, our new spot is dependent on both slope and which "edge" we've
    # moved off.  This means we have *8* special cases.  Bleah.  Extra credit if 
    # you can condense these into a simpler, readable form.
    
    # postive slope conditions (up-and-left or down-and-right)
    if (slope == 1):
        # top edge:  new y is -1.  We'll roll-over to the right edge
        if (new_y == -1):
            new_x = 4
            new_y = 4 - curr_x
        # bottom edge:  new y is 5.  Roll over to the left edge
        elif (new_y == 5):
            new_x = 0
            new_y = 4 - curr_x
        # left edge:  new x is -1.  Roll over to the bottom edge
        elif (new_x == -1):
            new_y = 4
            new_x = 4 - curr_y
        # right dege:  new y is 5.  Roll over to the top edge
        elif (new_x == 5):
            new_y = 0
            new_x = 4 - curr_y
    # Negative slope conditons:  either up-and-right or down-and-left
    elif (slope == -1):
        # top edge:  new y is -1.  Roll over to the left edge
        if (new_y == -1):
            new_x = 0
            new_y = curr_x
        # bottom edge:  new y is 5.  Roll over to the right edge
        elif (new_y == 5):
            new_x = 4
            new_y = curr_x
        # left edge:  new x is -1.  Roll over to the top edge.
        elif (new_x == -1):
            new_y = 0
            new_x = curr_y
        # right edge:  new x is 5.  Roll over to the bottom edge
        elif (new_x == 5):
            new_y = 4
            new_x = curr_y
            
    return(new_x,new_y)

######################################################################
# main 
######################################################################
current_x = 2
current_y = 2

while True:

  display.set_pixel(current_x, current_y, 0)
  tilt = get_tilt()
  new_position = move_pixel(current_x, current_y, tilt[0],tilt[1])
  current_x = new_position[0]
  current_y = new_position[1]

  display.set_pixel(current_x, current_y, 9)
  sleep(200)
