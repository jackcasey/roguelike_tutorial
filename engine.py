from __future__ import annotations

from typing import TYPE_CHECKING

from tcod.context import Context
from tcod.console import Console
from tcod.map import compute_fov

from input_handlers import MainGameEventHandler
from message_log import MessageLog
from procgen import generate_default_dungeon
from render_functions import render_bar, render_names_at_mouse_location

if TYPE_CHECKING:
    from entity import Actor
    from game_map import GameMap
    from input_handlers import EventHandler

class Engine:
    def __init__(self, player: Actor):
        self.event_handler: EventHandler = MainGameEventHandler(self)
        self.message_log =  MessageLog()
        self.mouse_location = (0, 0)
        self.player = player
        self.map_width = 80
        self.map_height = 43
        self.game_map: GameMap = None

        self.build_map()

    def build_map(self):
        game_map = generate_default_dungeon(
            map_width=self.map_width,
            map_height=self.map_height,
            engine=self
        )
        self.set_game_map(game_map)
        self.update_fov()

    def on_action(self):
        self.handle_enemy_turns()
        self.update_fov()

    def set_game_map(self, new_game_map: GameMap):
        self.game_map = new_game_map
        self.game_map.engine = self

    def handle_enemy_turns(self) -> None:
        for entity in set(self.game_map.actors) - {self.player}:
            if entity.ai:
                entity.ai.perform()

    def update_fov(self) -> None:
        """Recompute the visible area based on the players point of view."""
        self.game_map.visible[:] = compute_fov(
            self.game_map.tiles["transparent"],
            (self.player.x, self.player.y),
            radius=8,
        )
        # If a tile is "visible" it should be added to "explored".
        self.game_map.explored |= self.game_map.visible

    def render(self, console: Console) -> None:
        self.game_map.render(console)

        self.message_log.render(console=console, x=21, y=45, width=40, height=5)

        render_bar(
            console=console,
            current_value=self.player.fighter.hp,
            maximum_value=self.player.fighter.max_hp,
            total_width=20,
        )

        render_names_at_mouse_location(console=console, x=21, y=44, engine=self)
