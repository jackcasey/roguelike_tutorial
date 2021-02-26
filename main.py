#!/usr/bin/env python3
import tcod
import copy

from engine import Engine
import entity_factories
from input_handlers import EventHandler

def main() -> None:
    screen_width = 80
    screen_height = 50

    tileset = tcod.tileset.load_tilesheet(
        "dejavu10x10_gs_tc.png", 32, 8, tcod.tileset.CHARMAP_TCOD
    )
    player = copy.deepcopy(entity_factories.player)

    engine = Engine(player=player)

    with tcod.context.new_terminal(
        screen_width,
        screen_height,
        tileset=tileset,
        title="Yet Another Roguelike Tutorial",
        vsync=True,
    ) as context:
        root_console = tcod.Console(screen_width, screen_height, order="F")

        while True:
            engine.render(console=root_console, context=context)
            engine.event_handler.handle_events()

if __name__ == "__main__":
    main()
