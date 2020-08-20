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
#   simple iteration...no cool rollover.
#   returns a new x,y tuple.
######################################################################
def move_pixel(x, y, roll, pitch):
  x = x + roll
  if (x > 4):
      x = 0
  if (x < 0):
      x = 4
        
  y = y + pitch
  if (y > 4):
      y = 0
  if (y < 0):
      y = 4
  
  return(x,y)

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
