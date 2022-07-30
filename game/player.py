import math
import pyglet
from pyglet.window import key

from . import bullet, physicalobject, config


class Player(physicalobject.PhysicalObject):
    def __init__(self, *args, **kwargs):
        super(Player, self).__init__(img=config.player_image, *args, **kwargs)
        self.engine_sprite = pyglet.sprite.Sprite(img=config.engine_image, *args, **kwargs)
        self.engine_sprite.visible = False
        self.thrust = 300.0
        self.rotate_speed = 200.0
        self.bullet_speed = 700.0
        self.reacts_to_bullets = False
        self.key_handler = key.KeyStateHandler()
        self.event_handlers = [self, self.key_handler]

    def update(self, dt):
        super(Player, self).update(dt)
        if self.key_handler[key.LEFT]:
            # self.rotation -= self.rotate_speed * dt
            self.x -= 2
        if self.key_handler[key.RIGHT]:
            # self.rotation += self.rotate_speed * dt
            self.x += 2

        if self.key_handler[key.UP]:
            self.engine_sprite.rotation = self.rotation - 90
            self.engine_sprite.x = self.x
            self.engine_sprite.y = self.y
            self.engine_sprite.visible = True
            self.y += 2

        if not self.key_handler[key.UP]:
            self.engine_sprite.visible = False

        if self.key_handler[key.DOWN]:
            self.y -= 2

    def on_key_press(self, symbol, modifiers):
        if symbol == key.SPACE:
            self.image = config.player_fire
            self.fire()
            # self.image = resources.player_image
            pyglet.clock.schedule_once(self.unfire, 0.2)

    def unfire(self, dt):
        self.image = config.player_image

    def fire(self):
        angle_radians = math.radians(90)
        ship_radius = self.image.width / 2
        bullet_x = self.x + math.cos(angle_radians) * ship_radius
        bullet_y = self.y + math.sin(angle_radians) * ship_radius
        new_bullet = bullet.Bullet(bullet_x, bullet_y, batch=self.batch)
        bullet_vx = self.velocity_x + math.cos(angle_radians) * self.bullet_speed
        bullet_vy = self.velocity_y + math.sin(angle_radians) * self.bullet_speed
        new_bullet.velocity_x, new_bullet.velocity_y = bullet_vx, bullet_vy

        self.new_objects.append(new_bullet)
        config.bullet_sound.play()

    def delete(self):
        self.engine_sprite.delete()
        super(Player, self).delete()
