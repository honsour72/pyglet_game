import math
import pyglet
from pyglet.window import key

from . import bullet, physicalobject, config


class Player(physicalobject.PhysicalObject):
    """
    Main player class
    """

    def __init__(self, *args, **kwargs):
        """
        Initialize player-base class
        :param args:
        :param kwargs:
        """
        super(Player, self).__init__(img=config.player_image, *args, **kwargs)
        self.engine_sprite = pyglet.sprite.Sprite(img=config.engine_image, *args, **kwargs)
        self.engine_sprite.visible = False
        self.bullet_speed = 700.0
        self.reacts_to_bullets = False
        self.key_handler = key.KeyStateHandler()
        self.event_handlers = [self, self.key_handler]

    def update(self, dt):
        """
        Handle key press every dt sec
        Change player positions via coordinates
        Show engine sprite if key up was pressed otherwise hide it
        :param dt: seconds
        :return: None
        """
        super(Player, self).update(dt)
        if self.key_handler[key.LEFT]:
            self.x -= 2
        if self.key_handler[key.RIGHT]:
            self.x += 2

        if self.key_handler[key.UP]:
            self.engine_sprite.rotation = self.rotation - 90  # flame should be turned down
            self.engine_sprite.x = self.x
            self.engine_sprite.y = self.y
            self.engine_sprite.visible = True
            self.y += 2

        if not self.key_handler[key.UP]:
            self.engine_sprite.visible = False

        if self.key_handler[key.DOWN]:
            self.y -= 2

    def on_key_press(self, symbol, modifiers):
        """
        Let player fire if space was pressed
        Swap image on 0.2 sec
        :param symbol: key from kb
        :param modifiers: required parameter
        :return: None
        """
        if symbol == key.SPACE:
            self.image = config.player_fire
            self.fire()
            pyglet.clock.schedule_once(self.change_image, 0.2)  # this task will execute in main loop after 0.2 sec

    def change_image(self, dt):
        """
        Changes player original image back
        And, yes it's hard crutch!
        :param dt: sec
        :return: None
        """
        self.image = config.player_image

    def fire(self):
        """
        Create a bullet objects via Bullet class
        Set basic bullet parameters
        Play bullet sound
        :return: None
        """
        angle_radians = math.radians(90)  # bullets should fly only up on game window
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
        """
        Remove player and engine sprite
        :return: None
        """
        self.engine_sprite.delete()
        super(Player, self).delete()
