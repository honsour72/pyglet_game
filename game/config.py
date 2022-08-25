import math
import pyglet
import random
from . import letter
from screeninfo import get_monitors


# ==================================================================================================================== #
#                                                   ALL FUNCTIONS                                                      #
# ==================================================================================================================== #


def player_lives(num_icons: int, batch=None) -> list:
    """
    Pin N player sprites on the top left window corner
    :param num_icons: integer - player lives per game
    :param batch: main pyglet window batch to draw objects' events
    :return: pl - list of N positioned player sprites
    """
    pl = []
    for i in range(num_icons):
        new_sprite = pyglet.sprite.Sprite(img=player_image, x=20 + i * 30, y=40, batch=batch)
        new_sprite.scale = 0.5
        pl.append(new_sprite)
    return pl


def generate_random_words(filename: str = './resources/words.txt', amount: int = None) -> list:
    """
    Read all word per row in <filename> (commonly: ./resources/words.txt)
    And return random positions from words list
    Yes, this is a crutch too...
    :param filename: text file with words
    :param amount: integer, how many words we needed
    :return: list of random words from txt file
    """
    all_words = []
    words = []
    # read-file construction
    with open(filename) as words_file:
        for line in words_file:
            all_words.append(line.strip())

    # get random words
    for w in range(amount):
        word = random.choice(all_words)
        all_words.remove(word)
        words.append(word)
    return words


def get_words(words_amount: int = None, batch=None) -> list:
    """
    Make list of positioned letters in words
    :param words_amount: integer - amount of words in the beginning of the game
    :param batch: main pyglet window batch to draw objects' events
    :return: list of letter-objects in words order
    """
    letters = []
    words = generate_random_words(amount=words_amount)
    for word in words:
        # configure word params
        word_x = random.randint(1, screen_width)
        word_y = random.randint(screen_height, screen_height + 50 * len(word))
        word_scale = random.choice([0.5, 0.6, 0.7, 0.8, 0.9, 1, 1.1, 1.2, 1.3, 1.4])
        word_velocity = -random.randint(20, 70) * (1/word_scale)
        letter_distance = word_scale * 60  # interval between letters
        for let in word[::-1]:  # word will fall in reverse order
            new_letter = letter.Letter(letter=let, x=word_x, y=word_y, batch=batch, produce_child=False)
            new_letter.velocity_y = word_velocity
            new_letter.scale = word_scale
            letters.append(new_letter)
            word_y += letter_distance
    return letters


def distance(point_1: tuple = (0, 0), point_2: tuple = (0, 0)) -> float:
    """
    Calculate distance between two points
    :param point_1:
    :param point_2:
    :return: float answer
    """
    return math.sqrt((point_1[0] - point_2[0]) ** 2 + (point_1[1] - point_2[1]) ** 2)


def center_image(image: pyglet.resource.image) -> None:
    """
    Centred images
    :param image: pyglet.resource.image
    :return: None
    """
    image.anchor_x = image.width / 2
    image.anchor_y = image.height / 2


def get_image(letter: str) -> pyglet.resource.image:
    """
    Set an image for a letter sprite
    :param letter: string letter to find out image
    :return: pyglet.resource.image object
    """
    img = pyglet.resource.image(f"{letter}.png")
    center_image(img)
    return img


# ==================================================================================================================== #
#                                                   ALL CONSTANTS                                                      #
# ==================================================================================================================== #

# SCREEN RESOLUTION
monitor_data = get_monitors()[0]
screen_width = monitor_data.width
screen_height = monitor_data.height

pyglet.resource.path = ['./resources']
pyglet.resource.reindex()

player_image = pyglet.resource.image("player.png")
center_image(player_image)
player_fire = pyglet.resource.image("player_fire.png")
center_image(player_fire)

bullet_image = pyglet.resource.image("bullet.png")
center_image(bullet_image)

x_image = pyglet.resource.image("X.png")
center_image(x_image)

engine_image = pyglet.resource.image("engine_flame.png")
engine_image.anchor_x = engine_image.width * 1.5
engine_image.anchor_y = engine_image.height / 2

bullet_sound = pyglet.resource.media("bullet.wav", streaming=False)

player_speed = 4

