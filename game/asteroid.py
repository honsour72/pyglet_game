import random
from . import physicalobject, resources


class Asteroid(physicalobject.PhysicalObject):
    """An asteroid that divides a little before it dies"""

    # def __init__(self, *args, **kwargs):
    def __init__(self, letter, produce_child: bool = False, *args, **kwargs):
        super(Asteroid, self).__init__(img=resources.get_image(letter), *args, **kwargs)

        # Slowly rotate the asteroid as it moves
        # self.rotate_speed = random.random() * 100.0 - 50.0
        self.rotate_speed = 0
        self.letter = letter
        self.produce_child = produce_child

    def update(self, dt):
        super(Asteroid, self).update(dt)
        # self.rotation += self.rotate_speed * dt

    def handle_collision_with(self, other_object):
        super(Asteroid, self).handle_collision_with(other_object)

        if self.produce_child:
            # Superclass handles deadness already
            if self.dead and self.scale > 0.5:
                num_asteroids = random.randint(2, 3)
                for i in range(num_asteroids):
                    new_asteroid = Asteroid(letter=self.letter, x=self.x, y=self.y, batch=self.batch)
                    new_asteroid.rotation = random.randint(0, 360)
                    new_asteroid.velocity_x = random.random() * 10 + self.velocity_x
                    new_asteroid.velocity_y = -random.random() * 30 + self.velocity_y
                    # new_asteroid.velocity_y = self.velocity_y
                    new_asteroid.scale = self.scale * 0.5
                    self.new_objects.append(new_asteroid)
