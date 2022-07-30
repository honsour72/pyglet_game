import pyglet
from game import letter, config, player
from random import randint

game_window = pyglet.window.Window(800, 600)
main_batch = pyglet.graphics.Batch()
score_label = pyglet.text.Label(text="Score: 0", x=10, y=575, batch=main_batch)
level_label = pyglet.text.Label(text="Version 5: It's a Game!",
                                x=400, y=575, anchor_x='center', batch=main_batch)
game_over_label = pyglet.text.Label(text="GAME OVER",
                                    x=400, y=-300, anchor_x='center',
                                    batch=main_batch, font_size=48)
you_win_label = pyglet.text.Label(text="CONGRATS, YOU WIN!",
                                  x=400, y=-300, anchor_x='center',
                                  batch=main_batch, font_size=48)
counter = pyglet.window.FPSDisplay(window=game_window)

player_ship = None
player_lives = []
score = 0
num_lives = 3
game_objects = []

# We need to pop off as many event stack frames as we pushed on
# every time we reset the level.
event_stack_size = 0


def start_game(only_player=False):
    global score, event_stack_size, player_lives, player_ship, game_objects
    score_label.text = "Score: " + str(score)

    while event_stack_size > 0:
        game_window.pop_handlers()
        event_stack_size -= 1

    for life in player_lives:
        life.delete()

    # Initialize the player sprite
    player_ship = player.Player(x=400, y=300, batch=main_batch)

    # Make three sprites to represent remaining lives
    player_lives = config.player_lives(num_lives, main_batch)

    # Make some asteroids so we have something to shoot at
    # asteroids = load.asteroids(num_asteroids, player_ship.position, main_batch)
    if not only_player:
        asteroids = config.asteroids(words_amount=5, batch=main_batch)
        game_objects = [player_ship] + asteroids
    else:
        game_objects.append(player_ship)

    # Add any specified event handlers to the event handler stack
    for obj in game_objects:
        for handler in obj.event_handlers:
            game_window.push_handlers(handler)
            event_stack_size += 1


@game_window.event
def on_draw():
    game_window.clear()
    main_batch.draw()
    counter.draw()


def update_game(dt):
    global score, num_lives

    player_dead = False
    victory = False

    # To avoid handling collisions twice, we employ nested loops of ranges.
    # This method also avoids the problem of colliding an object with itself.
    for i in range(len(game_objects)):
        for j in range(i + 1, len(game_objects)):

            obj_1 = game_objects[i]
            obj_2 = game_objects[j]

            # Make sure the objects haven't already been killed
            if not obj_1.dead and not obj_2.dead:
                if obj_1.collides_with(obj_2):
                    obj_1.handle_collision_with(obj_2)
                    obj_2.handle_collision_with(obj_1)

    # Let's not modify the list while traversing it
    to_add = []

    # Check for win condition
    asteroids_remaining = 0

    for obj in game_objects:
        obj.update(dt)

        to_add.extend(obj.new_objects)
        obj.new_objects = []

        # Check for win condition
        if isinstance(obj, letter.Letter):
            asteroids_remaining += 1

    # if asteroids_remaining == 0:
    if score == 20:
        # Don't act on victory until the end of the time step
        victory = True

    # Get rid of dead objects
    for to_remove in [obj for obj in game_objects if obj.dead]:
        if to_remove == player_ship:
            player_dead = True
        # If the dying object spawned any new objects, add those to the
        # game_objects list later
        to_add.extend(to_remove.new_objects)

        # Remove the object from any batches it is a member of
        to_remove.delete()

        # Remove the object from our list
        game_objects.remove(to_remove)

        # Bump the score if the object to remove is an asteroid
        if isinstance(to_remove, letter.Letter):
            score += 1
            score_label.text = "Score: " + str(score)

    # Add new objects to the list
    game_objects.extend(to_add)

    # Check for win/lose conditions <-- вот тут и была ошибка
    if player_dead:
        # We can just use the length of the player_lives list as the number of lives
        if len(player_lives) > 0:
            num_lives -= 1
            start_game(True)
        else:
            game_over_label.y = 300
    elif victory:
        pyglet.clock.unschedule(set_words)
        # player_ship.dead = True
        for obj in game_objects:

            obj.delete()
        # player_ship.delete()
        # player_ship.y = -200
        game_objects.clear()
        # score += 10
        # reset_level(len(player_lives))
    #
    # if score == 20:
    #     player_ship.delete()
        # for obj in game_objects:
        #     obj.delete()
        you_win_label.y = 300


def set_words(dt):
    global game_objects
    amount = randint(1, 10)
    words = config.asteroids(amount, batch=main_batch)
    game_objects.extend(words)


if __name__ == '__main__':
    start_game()
    pyglet.clock.schedule_interval(update_game, 1 / 120.0)
    pyglet.clock.schedule_interval(set_words, 10)
    pyglet.app.run()
