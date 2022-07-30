from game import letter, config, player
from random import randint
import pyglet


game_window = pyglet.window.Window(800, 600)
main_batch = pyglet.graphics.Batch()
score_label = pyglet.text.Label(text="Score: 0", x=10, y=575, batch=main_batch)
game_over_label = pyglet.text.Label(text="GAME OVER", x=400, y=-300, anchor_x='center', batch=main_batch, font_size=48)
you_win_label = pyglet.text.Label(text="YOU WIN!", x=400, y=-300, anchor_x='center', batch=main_batch, font_size=48)

player_ship = None
player_lives = []
score = 0
num_lives = 3
game_objects = []
event_stack_size = 0


def start_game(only_player=False):
    global score, event_stack_size, player_lives, player_ship, game_objects
    score_label.text = "Score: " + str(score)

    while event_stack_size > 0:
        game_window.pop_handlers()
        event_stack_size -= 1

    for life in player_lives:
        life.delete()

    player_ship = player.Player(x=400, y=300, batch=main_batch)
    player_lives = config.player_lives(num_lives, main_batch)

    if not only_player:
        asteroids = config.get_words(words_amount=5, batch=main_batch)
        game_objects = [player_ship] + asteroids
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


def update_game(dt):
    global score, num_lives

    player_dead = False
    victory = False

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

    for obj in game_objects:
        obj.update(dt)

        to_add.extend(obj.new_objects)
        obj.new_objects = []

        if isinstance(obj, letter.Letter):
            letters_remaining += 1

    if score == 200 or letters_remaining == 0:
        victory = True

    for to_remove in [obj for obj in game_objects if obj.dead]:
        if to_remove == player_ship:
            player_dead = True
        to_add.extend(to_remove.new_objects)

        to_remove.delete()

        game_objects.remove(to_remove)

        if isinstance(to_remove, letter.Letter):
            score += 1
            score_label.text = "Score: " + str(score)

    game_objects.extend(to_add)

    # Check for win/lose conditions <-- вот тут и была ошибка
    if player_dead:
        if len(player_lives) > 0:
            num_lives -= 1
            start_game(True)
        else:
            game_over_label.y = 300
    elif victory:
        pyglet.clock.unschedule(set_words)
        for obj in game_objects:
            obj.delete()
        game_objects.clear()
        you_win_label.y = 300


def set_words(dt):
    global game_objects
    amount = randint(1, 10)
    words = config.get_words(amount, batch=main_batch)
    game_objects.extend(words)


if __name__ == '__main__':
    start_game()
    pyglet.clock.schedule_interval(update_game, 1 / 120.0)
    pyglet.clock.schedule_interval(set_words, 10)
    pyglet.app.run()
