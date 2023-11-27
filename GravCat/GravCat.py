import time
import random
import thumby

# Define game states
START_SCREEN = 0
ONE_PLAYER_RUNNING = 1
TWO_PLAYER_RUNNING = 2
RESULTS = 3

# Global variables
is_two_player = False
game_state = START_SCREEN
high_score = 0
current_score = 0
time_held = 0
last_frame_time = time.ticks_ms()

# Platform variables
platform_speed = 1
platform_width_max = 24
platform_width_min = 14
min_distance = 20
platforms = []

# Character variables
character_position = [4, 30]
gravity_direction = 1
character_width = 8

platform_on_screen = False
top_platform_on_screen = False
platform_on_screen_2 = False
top_platform_on_screen_2 = False
platform_on_screen_3 = False
top_platform_on_screen_3 = False

prev_platform_position = [78, 0]
prev_top_platform_position = [78, 0]

thumby.display.setFPS(30)

button_state = 0
button_press_time = 0

# Sprites
# BITMAP: width: 18, height: 18
bitmap_g = bytearray([248,12,230,19,201,101,53,21,21,21,21,21,53,101,73,83,70,124,
            63,96,207,144,39,76,152,176,160,190,162,170,170,138,74,58,130,254,
            0,0,0,1,3,2,2,2,2,2,2,2,2,2,2,3,1,0])
sprite_g = thumby.Sprite(18, 18, bitmap_g, 0, 0)  

# Sprite by: Laveréna Wienclaw, Feb 2022 - https://thumby.us/Education/Moving-Walk/
catFootForward = bytearray([12,122,120,24,24,127,62,71])
catFeetForward = bytearray([12,122,56,88,24,127,62,71])
catSplit = bytearray([78,56,56,88,24,127,30,103])
catFrontSplit = bytearray([76,58,120,24,88,63,62,71])
catFeetBack = bytearray([76,58,120,24,88,63,126,7])
catBackFootTail = bytearray([76,58,58,88,88,63,126,7])

runnerSpr = thumby.Sprite(character_width, character_width, catFootForward+catFeetForward+catSplit+catFrontSplit+catFeetBack+catBackFootTail, character_position[0], character_position[1])

# Counter that will be used to index different frames
frameCtr = 0

def inputPressed():
    global button_state, button_press_time

    time_current = time.ticks_ms()
    
    if thumby.inputPressed():
        if button_state == 0:
            # print("Button pressed")
            button_state = 1
            button_press_time = time_current
        elif button_state == 1 and time.ticks_diff(time_current, button_press_time) > 2000:
            # print("Button held for 2 seconds or more")
            button_state = 2
    else:
        if button_state == 1:
            button_state = 0

    return button_state

def reset_game():
    global character_position, current_score, gravity_direction, button_state
    global platform_on_screen, top_platform_on_screen, platform_position, platform_width
    global top_platform_position, top_platform_width
    current_score = 0
    character_position = [5, 10]
    gravity_direction = -1
    button_state = 0
    platform_on_screen = True
    top_platform_on_screen = True
    platform_position = [50, 0]
    platform_width = 20
    top_platform_position = [66, 0]
    top_platform_width = 20
    
def update_character(touching_platform, touching_top_platform):
    global character_position, gravity_direction, game_state, frameCtr, character_width, current_score

    # print(character_position)

    if (not touching_platform and gravity_direction > 0) or (not touching_top_platform and gravity_direction < 0):
        character_position[1] += gravity_direction
    else:
        current_score += 1
        frameCtr+=1
        if(frameCtr==5):
            frameCtr=0

    if character_position[1] <= -character_width or character_position[1] >= 34:
        game_state = RESULTS

def update_platform(platform):
    pass

def detect_platform_collision(platform_position, platform_width):
    global character_position, character_width
    # print("high: " + str(character_position[0] + character_width))
    # print("top_plat: " + str(top_platform_position[0] + top_platform_width))
    return platform_position[0]  - character_width  <= character_position[0] and character_position[0] + character_width <= platform_position[0] + platform_width

# Main game loop
while True:
    thumby.display.fill(0)  # Clear the screen

    if game_state == START_SCREEN:
        # Display start screen UI
        # start_text = "Two Player" if is_two_player else "One Player"
        # thumby.display.drawText("Start Screen: " + start_text, 0, 0, 1)
        thumby.display.drawSprite(sprite_g)
        thumby.display.drawText("rav Cat", 22, 10, 1)
        thumby.display.drawText("Hold to", 20, 22, 1)
        thumby.display.drawText("Start", 24, 32, 1)
        
        frameCtr += 1
        runnerSpr = thumby.Sprite(character_width, character_width, catFootForward+catFeetForward+catSplit+catFrontSplit+catFeetBack+catBackFootTail,  character_position[0], character_position[1])
        runnerSpr.setFrame(frameCtr)
        thumby.display.drawSprite(runnerSpr)
        inputPressedResult = inputPressed()
        if inputPressedResult == 1:
            # game_state = TWO_PLAYER_RUNNING
            pass
        elif inputPressedResult == 2:
            reset_game()
            game_state = ONE_PLAYER_RUNNING

    elif game_state == ONE_PLAYER_RUNNING:
        touching_platform = False
        touching_top_platform = False
        
        if character_position[1] + character_width == 35:
            touching_platform = detect_platform_collision(platform_position, platform_width) \
            or detect_platform_collision(platform_position_2, platform_width_2) \
            or detect_platform_collision(platform_position_3, platform_width_3) 
        
        if character_position[1] == 4:
            touching_top_platform = detect_platform_collision(top_platform_position, top_platform_width) \
            or detect_platform_collision(top_platform_position_2, top_platform_width_2) \
            or detect_platform_collision(top_platform_position_3, top_platform_width_3)
        
        # print(str(touching_platform))
        update_character(touching_platform, touching_top_platform)

        if not platform_on_screen:
            platform_width = random.randint(platform_width_min, platform_width_max)
            platform_on_screen = True
            # platform_position = [78 + random.randint(2, 10),36]
            
            min_x_position = prev_platform_position[0] + platform_width + min_distance
            platform_position = [max(min_x_position, 78 + random.randint(2, 10)), 36]
            
            prev_platform_position = platform_position.copy()
            
        if not top_platform_on_screen:
            top_platform_width = random.randint(platform_width_min, platform_width_max)
            top_platform_on_screen = True
            # top_platform_position = [78,0]
            
            top_min_x_position = prev_top_platform_position[0] + top_platform_width + min_distance
            top_platform_position = [max(top_min_x_position, 78 + random.randint(2, 10)), 0]
            
            prev_top_platform_position = top_platform_position.copy()
            
        if not platform_on_screen_2:
            platform_width_2 = random.randint(platform_width_min, platform_width_max)
            platform_on_screen_2 = True
            platform_position_2 = [78 + random.randint(2, 10), 36]
            
            min_x_position = prev_platform_position[0] + platform_width + min_distance
            platform_position_2 = [max(min_x_position, 78 + random.randint(2, 10)), 36]
            
            prev_platform_position = platform_position_2.copy()
            
        if not top_platform_on_screen_2:
            top_platform_width_2 = random.randint(platform_width_min, platform_width_max)
            top_platform_on_screen_2 = True
            
            top_min_x_position = prev_top_platform_position[0] + top_platform_width + min_distance
            top_platform_position_2 = [max(top_min_x_position, 78 + random.randint(2, 10)), 0]
            
            prev_top_platform_position = top_platform_position_2.copy()

        if not platform_on_screen_3:
            platform_width_3 = random.randint(platform_width_min, platform_width_max)
            platform_on_screen_3 = True
            platform_position_3 = [78 + random.randint(2, 10), 36]
            
            min_x_position = prev_platform_position[0] + platform_width + min_distance
            platform_position_3 = [max(min_x_position, 78 + random.randint(2, 10)), 36]
            
            prev_platform_position = platform_position_3.copy()
            
        if not top_platform_on_screen_3:
            top_platform_width_3 = random.randint(platform_width_min, platform_width_max)
            top_platform_on_screen_3 = True

            top_min_x_position = prev_top_platform_position[0] + top_platform_width + min_distance
            top_platform_position_3 = [max(top_min_x_position, 78 + random.randint(2, 10)), 0]
            
            prev_top_platform_position = top_platform_position_3.copy()

        
        for _ in range(platform_speed):
            # Draw platforms
            thumby.display.drawFilledRectangle(platform_position[0], platform_position[1], platform_width, 4, 1)
            thumby.display.drawFilledRectangle(top_platform_position[0], top_platform_position[1], top_platform_width, 4, 1)

            thumby.display.drawFilledRectangle(platform_position_2[0], platform_position_2[1], platform_width_2, 4, 1)
            thumby.display.drawFilledRectangle(top_platform_position_2[0], top_platform_position_2[1], top_platform_width_2, 4, 1)

            thumby.display.drawFilledRectangle(platform_position_3[0], platform_position_3[1], platform_width_3, 4, 1)
            thumby.display.drawFilledRectangle(top_platform_position_3[0], top_platform_position_3[1], top_platform_width_3, 4, 1)


            # Draw character
            # thumby.display.drawFilledRectangle(character_position[0], character_position[1], character_width, 5, 1)
            if gravity_direction > 0:
                runnerSpr = thumby.Sprite(character_width, character_width, catFootForward+catFeetForward+catSplit+catFrontSplit+catFeetBack+catBackFootTail,  character_position[0], character_position[1])
            else:
                runnerSpr = thumby.Sprite(character_width, character_width, catFootForward+catFeetForward+catSplit+catFrontSplit+catFeetBack+catBackFootTail,  character_position[0], character_position[1], -1, False, True)
            runnerSpr.setFrame(frameCtr)
            thumby.display.drawSprite(runnerSpr)

            #DEBUG to hold platforms still
            # platform_position[0] = 5
            # top_platform_position[0] = 5

            platform_position[0] -= 1
            top_platform_position[0] -= 1
            if platform_position[0] < 0 - platform_width:
                platform_on_screen = False
            if top_platform_position[0] < 0 - top_platform_width:
                top_platform_on_screen = False
            
            platform_position_2[0] -= 1
            top_platform_position_2[0] -= 1
            if platform_position_2[0] < 0 - platform_width_2:
                platform_on_screen_2 = False
            if top_platform_position_2[0] < 0 - top_platform_width_2:
                top_platform_on_screen_2 = False
                
            
            if thumby.inputJustPressed():
                gravity_direction = -gravity_direction
                # Gives a "freeze" feel as the gravity reverses
                time.sleep(0.05)
        thumby.display.drawText(str(current_score), 52, 16, 1)

    elif game_state == TWO_PLAYER_RUNNING:
        # Stubbed as instructions screen for now
        thumby.display.drawText("Pressing", 0, 0, 1)
        thumby.display.drawText("flips grav.", 0, 10, 1)
        thumby.display.drawText("Run on plats ", 0, 20, 1)
        thumby.display.drawText("to score.", 0, 30, 1)
        thumby.display.update()
        
        time.sleep(3)
        game_state = START_SCREEN

    elif game_state == RESULTS:
        # Display results screen UI
        thumby.display.drawText("Curr: " + str(current_score), 0, 10, 1)
        thumby.display.drawText("High: " + str(high_score), 0, 20, 1)

        if inputPressed() == 1:
            if current_score > high_score:
                high_score = current_score
            game_state = START_SCREEN
            character_position = [4, 30]

    thumby.display.update()
    
    # TODO:
    # Add front collision
    # Stagger platforms
    # Change scoring based on platform difficulty
    # Clean Up
