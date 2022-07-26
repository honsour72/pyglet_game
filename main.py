import pyglet
from game import asteroid, load, player


game_window = pyglet.window.Window(800, 600)
main_batch = pyglet.graphics.Batch()
score_label = pyglet.text.Label(text="Score: 0", x=10, y=575, batch=main_batch)
level_label = pyglet.text.Label(text="Version 5: It's a Game!",
                                x=400, y=575, anchor_x='center', batch=main_batch)
game_over_label = pyglet.text.Label(text="GAME OVER",
                                    x=400, y=-300, anchor_x='center',
                                    batch=main_batch, font_size=48)
counter = pyglet.window.FPSDisplay(window=game_window)

player_ship = None
player_lives = []
score = 0
num_asteroids = 3
game_objects = []

# We need to pop off as many event stack frames as we pushed on
# every time we reset the level.
event_stack_size = 0


def start_game():
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
    player_lives = load.player_lives(num_lives, main_batch)

    # Make some asteroids so we have something to shoot at
    # asteroids = load.asteroids(num_asteroids, player_ship.position, main_batch)
    asteroids = load.asteroids(words_amount=5, batch=main_batch)

    # Store all objects that update each frame in a list
    game_objects = [player_ship] + asteroids

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
    global score


def set_words(dt):
    global game_objects
    amount = random.randint(1, 10)
    words = load.asteroids(amount, batch=main_batch)
    game_objects.extend(words)


if __name__ == '__main__':
    start_game()
    pyglet.clock.schedule_interval(update_game, 1 / 120.0)
    pyglet.clock.schedule_interval(set_words, 10)
    pyglet.app.run()
