import random
from . import physicalobject, config


class Letter(physicalobject.PhysicalObject):
    def __init__(self, letter, produce_child: bool = False, *args, **kwargs):
        super(Letter, self).__init__(img=config.get_image(letter), *args, **kwargs)

        self.rotate_speed = 0
        self.letter = letter
        self.produce_child = produce_child

    def update(self, dt):
        super(Letter, self).update(dt)
        # self.rotation += self.rotate_speed * dt

    def handle_collision_with(self, other_object):
        super(Letter, self).handle_collision_with(other_object)

        if self.produce_child:
            # Superclass handles deadness already
            if self.dead and self.scale > 0.5:
                mini_letters = random.randint(1, 3)
                for i in range(mini_letters):
                    mini_letter = Letter(letter=self.letter, x=self.x, y=self.y, batch=self.batch)
                    mini_letter.rotation = random.randint(0, 360)
                    mini_letter.velocity_x = random.random() * 10 + self.velocity_x
                    mini_letter.velocity_y = -random.random() * 30 + self.velocity_y
                    # mini_letter.velocity_y = self.velocity_y
                    mini_letter.scale = self.scale * 0.5
                    self.new_objects.append(mini_letter)
