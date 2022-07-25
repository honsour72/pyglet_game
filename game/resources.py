import pyglet


def get_image(letter: str) -> pyglet.resource.image:
    img = pyglet.resource.image(f"{letter}.png")
    center_image(img)
    return img


def center_image(image):
    """Sets an image's anchor point to its center"""
    image.anchor_x = image.width / 2
    image.anchor_y = image.height / 2


# Tell pyglet where to find the resources
pyglet.resource.path = ['./resources']
pyglet.resource.reindex()

# Load the three main resources and get them to draw centered
player_image = pyglet.resource.image("player2.png")
center_image(player_image)
player_fire = pyglet.resource.image("player_fire.png")
center_image(player_fire)

bullet_image = pyglet.resource.image("bullet.png")
center_image(bullet_image)

asteroid_image = pyglet.resource.image("asteroid.png")
center_image(asteroid_image)

# The engine flame should not be centered on the ship. Rather, it should be shown 
# behind it. To achieve this effect, we just set the anchor point outside the
# image bounds.
engine_image = pyglet.resource.image("engine_flame.png")
engine_image.anchor_x = engine_image.width * 1.5
engine_image.anchor_y = engine_image.height / 2

# Load the bullet sound _without_ streaming so we can play it more than once at a time
bullet_sound = pyglet.resource.media("bullet.wav", streaming=False)
