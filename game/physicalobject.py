import pyglet
from . import config


class PhysicalObject(pyglet.sprite.Sprite):
    """
    Base game class physical object
    """

    def __init__(self, *args, **kwargs):
        """
        Initialize base-class physical object
        :param args:
        :param kwargs:
        """
        super(PhysicalObject, self).__init__(*args, **kwargs)
        self.velocity_x, self.velocity_y = 0.0, 0.0  # maybe we should move objs horizontally too?
        self.reacts_to_bullets = True
        self.is_bullet = False
        self.dead = False
        self.new_objects = []
        self.event_handlers = []

    def update(self, dt):
        """
        Update class states every dt second
        Increase speed if it needed
        Check object bounds
        :param dt: seconds
        :return: None
        """
        self.x += self.velocity_x * dt
        self.y += self.velocity_y * dt
        self.check_bounds()

    def check_bounds(self):
        """
        Bring back object from out of game window border
        :return: updates obj coordinates
        """
        min_x = -self.image.width / 2
        min_y = -self.image.height / 2
        max_x = config.screen_width + self.image.width / 2
        max_y = config.screen_height + self.image.height / 2
        if self.x < min_x:
            self.x = max_x
        if self.y < min_y:
            self.y = max_y
        if self.x > max_x:
            self.x = min_x

    def collides_with(self, other_object):
        """
        Detects collision with other game object
        :param other_object: pyglet.sprite.Sprite
        :return: bool: True if objects can effect each other otherwise False
        """
        if not self.reacts_to_bullets and other_object.is_bullet:
            return False
        if self.is_bullet and not other_object.reacts_to_bullets:
            return False
        collision_distance = self.image.width * 0.5 * self.scale + other_object.image.width * 0.5 * other_object.scale
        actual_distance = config.distance(self.position, other_object.position)

        return actual_distance <= collision_distance

    def handle_collision_with(self, other_object):
        """
        Kills current object if other game object is not the same one
        :param other_object: pyglet.sprite.Sprite
        :return: update dead attribute
        """
        if other_object.__class__ is not self.__class__:
            self.dead = True
