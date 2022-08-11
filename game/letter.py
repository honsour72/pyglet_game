import random
from . import physicalobject, config


class Letter(physicalobject.PhysicalObject):
    """
    Letter enemy class
    Letter can drop mini letter when die if produce_child = True
    """

    def __init__(self, letter, produce_child: bool = False, *args, **kwargs):
        """
        Initialize letter class
        :param letter: a simple string which be founded from resources as image
        :param produce_child: bool flag to determine letter producing self-copies
        :param args: pyglet common args
        :param kwargs: pyglet common kwargs
        """
        super(Letter, self).__init__(img=config.get_image(letter), *args, **kwargs)
        self.rotate_speed = 0  # letters can rotate while moving, why not?))))
        self.letter = letter
        self.produce_child = produce_child

    def handle_collision_with(self, other_object):
        """
        Produce random amount of mini-letters if self.produce_child = True
        :param other_object: pyglet.sprite.Sprite
        :return: None
        """
        super(Letter, self).handle_collision_with(other_object)

        if self.produce_child:
            if self.dead and self.scale > 0.5:
                mini_letters = random.randint(1, 3)
                for i in range(mini_letters):
                    mini_letter = Letter(letter=self.letter, x=self.x, y=self.y, batch=self.batch)
                    mini_letter.rotation = random.randint(0, 360)  # they will go every side
                    mini_letter.velocity_x = random.random() * 10 + self.velocity_x
                    mini_letter.velocity_y = -random.random() * 30 + self.velocity_y
                    mini_letter.scale = self.scale * 0.5
                    self.new_objects.append(mini_letter)
