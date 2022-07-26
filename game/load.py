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


def generate_random_words(filename: str = './resources/words.txt') -> list:
    words = []
    with open(filename) as words_file:
        for line in words_file:
            words.append(line.strip())
    return words


def asteroids(num_asteroids, player_position, batch=None):
    """Generate asteroid objects with random positions and velocities, not close to the player"""
    # for i in range(num_asteroids):
    #     asteroid_x, asteroid_y = player_position
    #     while util.distance((asteroid_x, asteroid_y), player_position) < 100:
    #         asteroid_x = random.randint(0, 800)
    #         asteroid_y = random.randint(0, 600)
    #     new_asteroid = asteroid.Asteroid(x=asteroid_x, y=asteroid_y, batch=batch)
    #     new_asteroid.rotation = random.randint(0, 360)
    #     new_asteroid.velocity_x, new_asteroid.velocity_y = random.random() * 40, random.random() * 40
    #     asteroids.append(new_asteroid)
    asteroids = []
    words = generate_random_words()
    delta_x = 800 // len(words)
    asteroid_x = 40
    for word in words:
        asteroid_y = random.randint(600, 700)
        word_velocity = -random.randint(20, 50)
        word_scale = random.choice([0.5, 0.6, 0.7, 0.8, 0.9, 1])
        for letter in word:
            # new_asteroid = asteroid.Asteroid(x=asteroid_x, y=asteroid_y, batch=batch)
            new_asteroid = asteroid.Asteroid(letter=letter, x=asteroid_x, y=asteroid_y, batch=batch)

            # new_asteroid.rotation = random.randint(0, 360)
            # new_asteroid.velocity_x, new_asteroid.velocity_y = random.random() * 40, random.random() * 40
            new_asteroid.velocity_y = word_velocity
            new_asteroid.scale = word_scale
            asteroids.append(new_asteroid)
            asteroid_y += 60
        asteroid_x += delta_x
    return asteroids
