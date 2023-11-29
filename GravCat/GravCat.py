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
platform_width_max = 24
platform_width_min = 14
min_distance = 10
max_distance = 20
bottom_platforms = [{'position': [0, 0], 'width':20, 'on_screen': False}] * 3
top_platforms = [{'position': [0, 0], 'width':20, 'on_screen': False}] * 3

# Character variables
character_position = [4, 30]
gravity_direction = 1
character_width = 8

prev_platform_position_x = 0
prev_top_platform_position_x = 0

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
    global top_platforms, bottom_platforms
    current_score = 0
    character_position = [5, 10]
    gravity_direction = 1
    button_state = 0
    bottom_platforms[0] = {'position': [5, 36], 'width':40, 'on_screen': True, 'id': 'B1'}
    top_platforms[0] = {'position': [5, 0], 'width':40, 'on_screen': True, 'id': 'T1'}
    bottom_platforms[1] = {'position': [0, 0], 'width':0, 'on_screen': False, 'id': 'B2'}
    top_platforms[1] = {'position': [0, 0], 'width':0, 'on_screen': False, 'id': 'T2'}
    bottom_platforms[2] = {'position': [0, 0], 'width':0, 'on_screen': False, 'id': 'B3'}
    top_platforms[2] = {'position': [0, 0], 'width':0, 'on_screen': True, 'id': 'T3'}
    
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

def detect_platform_collision(platform):
    global character_position, character_width
# TODO: Think about reducing leeway
    # print(character_position)
    return platform['position'][0]  - character_width  <= character_position[0] \
        and character_position[0] + character_width <= platform['position'][0] + platform['width']

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
            for platform in bottom_platforms:
                if detect_platform_collision(platform):
                    touching_platform = True
                    break;

        if character_position[1] == 4:
            for platform in top_platforms:
                if detect_platform_collision(platform):
                    touching_top_platform = True
                    break;
        
        update_character(touching_platform, touching_top_platform)

        
        for platform in bottom_platforms:
            if not platform['on_screen']:
                platform['width'] = random.randint(platform_width_min, platform_width_max)
                platform['on_screen'] = True
                platform['position'] = [prev_platform_position_x + random.randint(min_distance, max_distance), 36]
                
            prev_platform_position_x = platform['position'][0] + platform['width']

            thumby.display.drawFilledRectangle(platform['position'][0], platform['position'][1], platform['width'], 4, 1)
            platform['position'][0] -= 1
            if platform['position'][0] < 0 - platform['width']:
                platform['on_screen'] = False

        for platform in top_platforms:
            if not platform['on_screen']:
                platform['width'] = random.randint(platform_width_min, platform_width_max)
                platform['on_screen'] = True
                platform['position'] = [prev_top_platform_position_x + random.randint(min_distance, max_distance), 0]

            prev_top_platform_position_x = platform['position'][0] + platform['width']


            thumby.display.drawFilledRectangle(platform['position'][0], platform['position'][1], platform['width'], 4, 1)
            platform['position'][0] -= 1
            if platform['position'][0] < 0 - platform['width']:
                platform['on_screen'] = False

        # Draw character
        # thumby.display.drawFilledRectangle(character_position[0], character_position[1], character_width, character_width, 1)
        if gravity_direction > 0:
            runnerSpr = thumby.Sprite(character_width, character_width, catFootForward+catFeetForward+catSplit+catFrontSplit+catFeetBack+catBackFootTail,  character_position[0], character_position[1])
        else:
            runnerSpr = thumby.Sprite(character_width, character_width, catFootForward+catFeetForward+catSplit+catFrontSplit+catFeetBack+catBackFootTail,  character_position[0], character_position[1], -1, False, True)
        runnerSpr.setFrame(frameCtr)
        thumby.display.drawSprite(runnerSpr)
        
        if thumby.inputJustPressed() and (touching_top_platform or touching_platform):
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
    # Change scoring based on platform difficulty
    # Clean Up
