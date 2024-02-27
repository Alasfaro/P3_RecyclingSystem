import sys
sys.path.append("../")
from Common.project_library import *

# Modify the information below according to your setup and uncomment the entire section

# 1. Interface Configuration
project_identifier = 'P3B'  # enter a string corresponding to P0, P2A, P2A, P3A, or P3B
ip_address = '***.***.***.**'  # enter your computer's IP address
hardware = False  # True when working with hardware. False when working in the simulation

# 2. Servo Table configuration
short_tower_angle = 315  # enter the value in degrees for the identification tower
tall_tower_angle = 90  # enter the value in degrees for the classification tower
drop_tube_angle = 1804207  # enter the value in degrees for the drop tube. clockwise rotation from zero degrees

# 3. Qbot Configuration
bot_camera_angle = 0  # angle in degrees between -21.5 and 0

# 4. Bin configuration
# Configuration for the colors for the bins and the lines leading to those bins.
# Note: The line leading up to the bin will be the same color as the bin

bin1_offset = 0.10  # offset in meters
bin1_color = [1,0,0]  # e.g. [1,0,0] for red
bin2_offset = 0.20
bin2_color = [1,1,0]
bin3_offset = 0.20
bin3_color = [1,1,1]
bin4_offset = 0.20
bin4_color = [1,1,1]

# ------------ DO NOT modify the information below ------------

if project_identifier == "P0":
    QLabs = configure_environment(project_identifier, ip_address, hardware).QLabs
    bot = qbot(0,1, ip_address, QLabs, none-hardware)

elif project_identifier in ["P2A","P2B"]:
    QLabs = configure_environment(project_identifier, ip_address, hardware).QLabs
    arm = qarm(project_identifier, ip_address, QLabs, hardware)

elif project_identifier == "P3A":
    table_configuration = [short_tower_angle, tall_tower_angle, drop_tube_angle]
    configuration_information = [table_configuration, None, None]  # Configuring just the table
    QLabs = configure_environment(project_identifier, ip_address, hardware, configuration_information).QLabs
    table = servo_table(ip_address, QLabs, hardware)
    arm = qarm(project_identifier, ip_address, QLabs, hardware)

elif project_identifier == "P3B":
    table_configuration = [short_tower_angle, tall_tower_angle, drop_tube_angle]
    bin_configuration = [bin1_offset, bin2_offset, bin3_offset, bin4_offset, bin1_color, bin2_color, bin3_color, bin4_color]
    configuration_information = [table_configuration, bin_configuration, bin_configuration]
    QLabs = configure_environment(project_identifier, ip_address, hardware, configuration_information).QLabs
    table = servo_table(ip_address, QLabs, hardware)
    arm = qarm(project_identifier, ip_address, QLabs, hardware)
    bot = qbot(0,1, ip_address, QLabs, bins, hardware)

#------------------------------------------------------------------------------------------------------------------------------
# STUDENT CODE BEGINS
#------------------------------------------------------------------------------------------------------------------------------    

import random

def arm_motion_1():  # Control the Q-arm to place the first container
    arm.rotate_elbow(-30)
    arm.rotate_shoulder(45)
    time.sleep(2)
    arm.control_gripper(35)
    time.sleep(2)
    arm.rotate_elbow(-10)
    time.sleep(1)
    arm.rotate_base(20)
    arm.rotate_shoulder(-45)
    arm.move_arm(0.016, -0.311, 0.744)
    arm.rotate_base(-2)
    time.sleep(1)
    arm.rotate_shoulder(25)
    arm.rotate_elbow(7)
    time.sleep(1)
    arm.control_gripper(-35)
    time.sleep(1)
    arm.rotate_elbow(-7)
    time.sleep(1)
    arm.rotate_shoulder(4)
    time.sleep(1)
    arm.rotate_shoulder(-10)
    arm.home()


def arm_motion_2():  # Control the Q-arm to place the second container
    arm.rotate_elbow(-30)
    arm.rotate_shoulder(45)
    time.sleep(2)
    arm.control_gripper(35)
    time.sleep(2)
    arm.rotate_elbow(-10)
    time.sleep(1)
    arm.rotate_base(20)
    arm.rotate_shoulder(-45)
    arm.move_arm(0.016, -0.311, 0.744)
    arm.rotate_base(-2)
    time.sleep(1)
    arm.rotate_elbow(20)  
    time.sleep(1)  
    arm.rotate_shoulder(10) 
    time.sleep(1)
    arm.rotate_elbow(5)     
    time.sleep(1)
    arm.rotate_shoulder(3) 
    time.sleep(1)
    arm.control_gripper(-35)
    time.sleep(1)
    arm.home()


def arm_motion_3(): # Control the Q-arm to place the third container
    arm.rotate_elbow(-30)
    arm.rotate_shoulder(45)
    time.sleep(2)
    arm.control_gripper(35)
    time.sleep(2)
    arm.rotate_elbow(-10)
    time.sleep(1)
    arm.rotate_base(20)
    arm.rotate_shoulder(-45)
    arm.move_arm(0.016, -0.311, 0.744)
    arm.rotate_base(-2)
    time.sleep(3)
    bot.rotate(190)
    bot.rotate(5)
    arm.rotate_shoulder(20)
    arm.rotate_shoulder(-5)
    arm.rotate_base(-2)
    arm.rotate_base(-1)
    arm.rotate_elbow(-5)
    arm.rotate_shoulder(-5)
    arm.rotate_shoulder(10)
    arm.rotate_elbow(3)
    arm.rotate_elbow(2)
    arm.rotate_elbow(2)
    arm.rotate_elbow(2)
    arm.rotate_elbow(3)
    arm.rotate_elbow(3)
    time.sleep(2)
    arm.control_gripper(-35)
    time.sleep(2)
    arm.home()
    bot.rotate(70)
    bot.rotate(180)
    bot.rotate(-20)
    bot.rotate(-10)
    bot.rotate(10)
    bot.rotate(-10)
    bot.rotate(-5)
    bot.rotate(-2)
    bot.rotate(-3)
    bot.rotate(1)
    time.sleep(1)
    bot.rotate(-8)

#-----------------------------------------------

def track(): # simple set up boolean operator for reading the lines. the final phrase is a joke in case something does go wrong
    sensor = bot.line_following_sensors()
    if sensor == [1, 1]:
        bot.set_wheel_speed([0.2, 0.2])
    elif sensor == [0, 1]:
        bot.set_wheel_speed([0.08, 0.044])
    elif sensor == [1, 0]:
        bot.set_wheel_speed([0.044, 0.08])
    else:
        print("you stupid where that bot going?")


def Bin1():  # this sub function is created as a locator for each bin. in it runs the infinite loop for the track follower
    while True:  # the infinite loop runs in each bin location functions
        box1 = bot.position()  # variable box is set for reading positions
        if float(box1[1]) > 0.5:  # box[1] reads the y coordinates
        
            if (float(box1[0]) < 1.05) and (float(box1[0]) > 1.00):  # box[0] reads the x coordinates and the positions to stop
                print("this works fine")
                
                break  # this is used to stop the infinite loop         
        track()  # the conditions of position must be read first before the track follower as it allows it to prioritize the stopping aspect.
    print("while is not working")
    bot.stop()  # this is placed to stop the motions


def Bin2():  # uses similar system as Bin1()
    while True:
        box2 = bot.position()
        if float(box2[1]) >= 0.53:
            if (float(box2[0]) < 0.09) and (float(box2[0]) >= 0.05):
                break
                print("this works fine")  
        track()
    print("while is not working")
    bot.stop()


def Bin3():  # uses similar system as Bin1()
    while True:
        box3 = bot.position()
        if float(box3[2]) <= 0.5:
            if (float(box3[0]) <= 0.09) and (float(box3[0]) >= 0.05):
                print("this works fine")    
                break
        track()
    print("while is not working")
    bot.stop()


def Bin4():  # uses similar system as Bin1()
    while True:
        box4 = bot.position()
        
        if float(box4[2]):
            if (float(box4[0]) < 1.08) and (float(box4[0]) >= 1.00):
                print("this works fine")
                break
        track()
    print("while is not working")
    bot.stop()

#-----------------------------------------------

def dumping():  # simple dump functions
    bot.activate_linear_actuator()
    time.sleep(2)
    bot.dump()
    time.sleep(2)
    print("pls run")


def dispose_container():
    bot.activate_color_sensor()
    RGB = bot.read_color_sensor()
    if RGB[0] == [0,1,0]:
        dumping()
        bot.deactivate_color_sensor()
    elif RGB[0] == [1,0,0]:
        dumping()
        bot.deactivate_color_sensor()
    elif RGB[0] == [0,0,1]:
        dumping()
        bot.deactivate_color_sensor()


def return_home():
    while True:
        home_spot = bot.position()
        if float(home_spot[0]) >= 1.3 and float(home_spot[1]) >= -0.01:
            print("this is dum")
            break
        track()
    bot.rotate(3)
    print("so we are done huh?")
    bot.stop()


def dispense_load(last_binID, disk, rest_mass, rest_binID):
    # function for dispense and load the container
    options = [1, 2, 3, 4, 5, 6]  # all optional IDs
    n = 0  # number of containers on Q-bot
    weight_bot = 0  # weight on bot
    total_weight = 0
    # set a variable to check the total weight before pick it up to Q-bot
    if len(disk) != 0 and disk[-1] == 'full':
        # used to see if there are any remaining containers on the table
        arm_motion(1)
        n += 1 # 1 more container on the Q-bot
        weight_bot += float(rest_mass)  # get the weight on the Q-bot
        last_binID.append(rest_binID)
        # set the target box for the remaining container

    while weight_bot <= 90 and n < 3 and total_weight <= 90:
        # the total amount cannot exceed 90 grams
        # no more than three boxes are on the machine
        # total_weight is used to check weight before pick the container up to Q-bot
        option = random.choice(options)  # a random number is drawn from one to six
        material_mass_binID = table.dispense_container(option, True)  # Three characteristics are obtained
        print(material_mass_binID)
        material = material_mass_binID[0]
        mass = float(material_mass_binID[1])
        binID = material_mass_binID[2]
        # get its mass, binID separately
        total_weight = weight_bot + mass
        if total_weight <= 90 and weight_bot <= 90:
            if len(last_binID) == 0 or binID != last_binID[-1]:
                # use "len()=0" to prevent errors from the first run
                last_binID.append(binID)
                # get the target bin
                weight_bot += mass
                n += 1
                if n == 1:
                    arm_motion(1)
                    disk.append('empty')  # The table is empty and can continue
                    print('the table is empty')
                elif n == 2:
                    arm_motion(2)
                    disk.append('empty')
                    print('the table is empty')
                elif n == 3:
                    arm_motion(3)
                    disk.append('empty')
                    print('the table is empty')
                    break

        if total_weight > 90 or binID != last_binID[-1]:
            # if the total weight exceeds 90 or the destination of the new bottle is different from the previous one
            disk.append('full')
            print('the table is full')
            break
    rest_mass
    rest_binID = binID
    destination = last_binID[-1]
    return [mass, binID, last_binID[-1]] #get these values from this function


def transfer_deposit(ID):  # four different destinations
    if ID == 'Bin01':
        Bin1()
    if ID == 'Bin02':
        Bin2()
    if ID == 'Bin03':
        Bin3()
    if ID == 'Bin04':
        Bin4()
    dispose_container()
    return_home()


def main():
    prompt = "\nEnter 'quit' to end it."  # people can input ‘quit’ to end the program
    message = ''
    last_binID = []
    disk = []  # Refers to the state of the table, not the word ‘table’ to avoid confusion with ‘table.dispense()'
    rest_mass
    rest_binID
    while message != "quit":
        list = dispense_load(last_binID, disk, rest_mass, rest_binID)  # get these values
        rest_mass = list[0]
        rest_binID = list[1]
        destination = list[2]
        print(destination)  # the target bin
        ID = destination
        transfer_deposit(ID)
        message = input(prompt)
        print(message)

#------------------------------------------------------------------------------------------------------------------------------