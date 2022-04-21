BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

STAR_SPEEDS = (1, 2, 3)
STARS_AMOUNT = 250
ASTEROIDS_SPEED = 4
ASTEROIDS_AMOUNT = 25
ROCKETS_SPEED = 6
ROCKETS_AMOUNT = 1
SATELLITES_SPEED = 5
SATELLITES_AMOUNT = 1
LEVEL_MULTIPLIER = [3,1,2]
MENU_SECONDS = 7

POINTS_TO_PASS = 100
LIVES = 3
TEXT_SECONDS = 45
FRAME_RATE = 120
EXPLOSION_STOP_FRAMES = 120 #this % 10 cant be bigger than the amount of frames for the explosion

SPACESHIP_SPRITE = r'./resources/spaceship.png'
METEORITE_SPRITE = r'./resources/meteorite.png'
ROCKET_SPRITE1 = r'./resources/rocket1.png'
ROCKET_SPRITE2 = r'./resources/rocket2.png'
SATELLITE_SPRITE = r'./resources/satellite.png'
EXPLOSION_SPRITE = r'./resources/explosion{}.png'
BACKGROUNDS = r'./resources/backgrounds/background{}.png'
PLANET_SPRITE = r'./resources/planet.png'
MENU_IMAGES = r'./resources/menuscreen{}.png'
BACKGROUNDS_NUMBER = 10

MENU_SOUND = r'./resources/menusound.wav'
CRASH_SOUND = r'./resources/explosion.wav'
MENU_MUSIC = r'./resources/menumusic.wav'
LEVEL_MUSIC = r'./resources/epicmusic.wav'
GUITAR_MUSIC = r'./resources/guitar.wav'

GAME_FONT = r'./resources/Grand9K_Pixel.ttf'
FONT_SIZE = 32

DATABASE_FILE = r'./resources/highscores.db'

HIGHSCORE_SAVE_TEXT = ["CONGRATS! YOUR SCORE IS IN THE TOP TEN!!", "INPUT YOUR INITIALS", "_  _  _", "press space when finished"]
HIGHSCORE_HEADER1 = "TOP SCORES"
HIGHSCORE_HEADER2 = ""
HIGHSCORE_HEADER3 = "RANK.................NAME........................POINTS"
LEVEL_END_TEXT = ["LEVEL {level} FINISHED", "{points} EXTRA POINTS WILL BE AWARDED FOR LANDING", "PRESS SPACE TO CONTINUE"]
STORY_TEXT = ["YEAR 3022:", "EARTH HAS BEEN DEVASTATED BY WAR", "MAKIND IS SEARCHING FOR A NEW HOME", "YOU, AS THE BEST PILOT IN THE GALAXY", "ARE EARTH'S LAST HOPE", "FIND EXOPLANETS VIABLE FOR LIFE ALL OVER THE GALAXY", "BUT BEWARE! SPACE IS A DANGEROUS PLACE","THE SPACE JUNK WILL TEST YOUR DODGING SKILLS!!!","","", "press space to return to main menu"]
INSTRUCTIONS_TEXT = ["PRESS UP OR DOWN ARROWS TO MOVE THE SPACESHIP", "EVERY OBSTACLE DODGED GRANTS 1 POINT", "IF YOU CRASH YOU LOSE POINTS!!", "YOU WILL COMPLETE THE LEVEL IF YOU REACH A CERTAIN AMOUNT OF POINTS", "THE PLANET IS THE GOAL, LANDING GRANTS EXTRA POINTS", "YOU CAN EXIT THE GAME AT ANY POINT WITH ALT + F4", "", "", "press space to return to main menu"]
RESOLUTION_SCALES = {
    600  : 0.42,
    664  : 0.46,
    720  : 0.5,
    768  : 0.53,
    800  : 0.55,
    864  : 0.6,
    900  : 0.625,
    960  : 0.66,
    1024 : 0.71,
    1050 : 0.72,
    1080 : 0.75,
    1152 : 0.8,
    1200 : 0.83,
    1440 : 1,
    2160 : 1.5
}