from typing import Set, Iterable, Any

from tcod.context import Context
from tcod.console import Console
from tcod.map import compute_fov

from entity import Entity
from game_map import GameMap
from input_handlers import EventHandler
from procgen import generate_default_dungeon

class Engine:
    def __init__(self, event_handler: EventHandler, player: Entity):
        self.event_handler = event_handler
        self.player = player
        self.map_width = 80
        self.map_height = 50
        self.game_map = None

        self.build_map()

    def build_map(self):
        game_map = generate_default_dungeon(
            map_width=self.map_width,
            map_height=self.map_height,
            player=self.player
        )
        self.set_game_map(game_map)
        self.update_fov()

    def set_game_map(self, new_game_map: GameMap):
        self.game_map = new_game_map

    def handle_events(self, events: Iterable[Any]) -> None:
        for event in events:
            action = self.event_handler.dispatch(event)

            if action is None:
                continue

            action.perform(self, self.player)
            self.handle_enemy_turns()
            self.update_fov()  # Update the FOV before the players next action.

    def handle_enemy_turns(self) -> None:
        for entity in self.game_map.entities - {self.player}:
            print(f'The {entity.name} wonders when it will get to take a real turn.')

    def update_fov(self) -> None:
        """Recompute the visible area based on the players point of view."""
        self.game_map.visible[:] = compute_fov(
            self.game_map.tiles["transparent"],
            (self.player.x, self.player.y),
            radius=8,
        )
        # If a tile is "visible" it should be added to "explored".
        self.game_map.explored |= self.game_map.visible

    def render(self, console: Console, context: Context) -> None:
        self.game_map.render(console)

        context.present(console)

        console.clear
