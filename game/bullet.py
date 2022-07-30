from . import physicalobject, config


class Bullet(physicalobject.PhysicalObject):
    def __init__(self, *args, **kwargs):
        super(Bullet, self).__init__(config.bullet_image, *args, **kwargs)
        self.is_bullet = True

    def die(self, dt):
        self.dead = True
