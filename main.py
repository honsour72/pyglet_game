from game import letter, config, player
from random import randint
import pyglet


# parameters of game window
game_window = pyglet.window.Window(800, 600)
main_batch = pyglet.graphics.Batch()
score_label = pyglet.text.Label(text="Score: 0", x=10, y=575, batch=main_batch)
# both labels are fixed in the game window but out of border
game_over_label = pyglet.text.Label(text="GAME OVER", x=400, y=-300, anchor_x='center', batch=main_batch, font_size=48)
you_win_label = pyglet.text.Label(text="YOU WIN!", x=400, y=-300, anchor_x='center', batch=main_batch, font_size=48)

# parameters of game
player_ship = None
num_lives = 3
player_lives = []
score = 0
game_objects = []
event_stack_size = 0


def start_game(only_player=False) -> None:
    """
    Initialize yhe game
    Set player, and letters if not only_player flag otherwise set player only
    Iterate game objects and push all handlers
    :param only_player: bool, if true it restarts game with one player only
    :return: Nothing
    """
    global score, event_stack_size, player_lives, player_ship, game_objects
    score_label.text = "Score: " + str(score)

    while event_stack_size > 0:
        game_window.pop_handlers()
        event_stack_size -= 1

    # remove one player ship from health bar when it dies
    for life in player_lives:
        life.delete()

    player_ship = player.Player(x=400, y=300, batch=main_batch)
    player_lives = config.player_lives(num_lives, main_batch)

    if not only_player:
        words = config.get_words(words_amount=5, batch=main_batch)
        game_objects = [player_ship] + words
    else:
        game_objects.append(player_ship)

    for obj in game_objects:
        for handler in obj.event_handlers:
            game_window.push_handlers(handler)
            event_stack_size += 1


@game_window.event
def on_draw():
    game_window.clear()
    main_batch.draw()


def update_game(dt) -> None:
    """
    This func will:
    1) Update game and all game objects
    2) Collide objects with other objects
    3) Instance and count new letters
    4) Remove dead objects
    5) Redraw score if it needed
    6) Check win/lose condition
    7) Show win/lose label if it needed
    ... in 1/120 (0.008) sec
    :param dt: pyglet required parameter. For more info see:
    :return: None
    """
    global score, num_lives

    player_dead = False
    victory = False

    # pyglet required double-circled construction
    for i in range(len(game_objects)):
        for j in range(i + 1, len(game_objects)):

            obj_1 = game_objects[i]
            obj_2 = game_objects[j]

            if not obj_1.dead and not obj_2.dead:
                if obj_1.collides_with(obj_2):
                    obj_1.handle_collision_with(obj_2)
                    obj_2.handle_collision_with(obj_1)

    to_add = []
    letters_remaining = 0

    # update all game objects
    for obj in game_objects:
        obj.update(dt)

        to_add.extend(obj.new_objects)
        obj.new_objects = []

        # count letters
        if isinstance(obj, letter.Letter):
            letters_remaining += 1

    # win conditions
    if score == 200 or letters_remaining == 0:
        victory = True

    # this construction removes dead objects
    for to_remove in [obj for obj in game_objects if obj.dead]:
        if to_remove == player_ship:
            player_dead = True

        # add new mini-letters if they have been created by dead letter
        to_add.extend(to_remove.new_objects)

        # delete dead object from game window AND remove it from game_objects list
        to_remove.delete()
        game_objects.remove(to_remove)

        # update score label
        if isinstance(to_remove, letter.Letter):
            score += 1
            score_label.text = "Score: " + str(score)

    # add all new mini-letters produced by dead letter in game_objects list
    game_objects.extend(to_add)

    # Check for win/lose conditions
    if player_dead:
        # restart game if player still have lives
        if len(player_lives) > 0:
            num_lives -= 1
            start_game(True)
        else:
            # show game_over label in the center of game window
            game_over_label.y = 300
    elif victory:
        # unset letter-generate function
        pyglet.clock.unschedule(add_words)
        for obj in game_objects:  # remove all objects
            obj.delete()
        game_objects.clear()  # clear game_objects list
        # show you_win label in the center of game window
        you_win_label.y = 300


def add_words(dt) -> None:
    """
    Generate random words and add it to the game window by extending game_objects list
    :param dt: pyglet required parameter. For more info see:
    :return: None
    """
    global game_objects
    amount = randint(1, 10)
    words = config.get_words(amount, batch=main_batch)
    game_objects.extend(words)


if __name__ == '__main__':
    start_game()
    pyglet.clock.schedule_interval(update_game, 1 / 120.0)
    pyglet.clock.schedule_interval(add_words, 10)
    pyglet.app.run()
