import pyglet
import random
from . import asteroid, resources, util


def player_lives(num_icons, batch=None):
    """Generate sprites for player life icons"""
    player_lives = []
    for i in range(num_icons):
        new_sprite = pyglet.sprite.Sprite(img=resources.player_image,
                                          x=785 - i * 30, y=585,
                                          batch=batch)
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


def asteroids(words_amount: int = None, batch=None):
    """Generate asteroid objects with random positions and velocities, not close to the player"""
    asteroids = []
    words = generate_random_words(amount=words_amount)
    delta_x = 800 // len(words)
    asteroid_x = 40
    for word in words:
        asteroid_x = random.randint(1, 750)
        asteroid_y = random.randint(600, 700)
        word_scale = random.choice([0.5, 0.6, 0.7, 0.8, 0.9, 1])
        word_velocity = -random.randint(10, 50) * (1/word_scale)
        letter_distance = word_scale * 60
        for letter in word[::-1]:
            # new_asteroid = asteroid.Asteroid(x=asteroid_x, y=asteroid_y, batch=batch)
            new_asteroid = asteroid.Asteroid(letter=letter, x=asteroid_x, y=asteroid_y, batch=batch)

            # new_asteroid.rotation = random.randint(0, 360)
            # new_asteroid.velocity_x, new_asteroid.velocity_y = random.random() * 40, random.random() * 40
            new_asteroid.velocity_y = word_velocity
            new_asteroid.scale = word_scale
            asteroids.append(new_asteroid)
            asteroid_y += letter_distance
        # asteroid_x += delta_x
    return asteroids
