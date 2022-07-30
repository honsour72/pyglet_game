import math
import pyglet
import random
from . import letter


# ==================================================================================================================== #
#                                                   ALL FUNCTIONS                                                      #
# ==================================================================================================================== #


def player_lives(num_icons, batch=None):
    player_lives = []
    for i in range(num_icons):
        new_sprite = pyglet.sprite.Sprite(img=player_image, x=20 + i * 30, y=555, batch=batch)
        new_sprite.scale = 0.5
        player_lives.append(new_sprite)
    return player_lives


def generate_random_words(filename: str = './resources/words.txt', amount: int = None) -> list:
    all_words = []
    words = []
    with open(filename) as words_file:
        for line in words_file:
            all_words.append(line.strip())
    for w in range(amount):
        word = random.choice(all_words)
        all_words.remove(word)
        words.append(word)
    return words


def get_words(words_amount: int = None, batch=None):
    letters = []
    words = generate_random_words(amount=words_amount)
    for word in words:
        word_x = random.randint(1, 750)
        word_y = random.randint(600, 700)
        word_scale = random.choice([0.5, 0.6, 0.7, 0.8, 0.9, 1])
        word_velocity = -random.randint(10, 50) * (1/word_scale)
        letter_distance = word_scale * 60
        for let in word[::-1]:
            new_letter = letter.Letter(letter=let, x=word_x, y=word_y, batch=batch)
            new_letter.velocity_y = word_velocity
            new_letter.scale = word_scale
            letters.append(new_letter)
            word_y += letter_distance
    return letters


def distance(point_1=(0, 0), point_2=(0, 0)):
    return math.sqrt((point_1[0] - point_2[0]) ** 2 + (point_1[1] - point_2[1]) ** 2)


def center_image(image):
    image.anchor_x = image.width / 2
    image.anchor_y = image.height / 2


def get_image(letter: str) -> pyglet.resource.image:
    img = pyglet.resource.image(f"{letter}.png")
    center_image(img)
    return img


# ==================================================================================================================== #
#                                                   ALL CONSTANTS                                                      #
# ==================================================================================================================== #

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

