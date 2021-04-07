from Autopilot import connecting_with_autopilot
from Autopilot import get_alt
from Autopilot import get_attitude_massage
from Autopilot import get_roll
from Autopilot import get_pitch
from Autopilot import get_yaw
import time
from Autopilot import *


vechial = connecting_with_autopilot()
massage_atttitude = get_attitude_massage(vechial)
print(get_roll(massage_atttitude))
print(get_pitch(massage_atttitude))
print(get_yaw(massage_atttitude))

print(vechial.location())



    