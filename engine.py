from typing import Set, Iterable, Any

from tcod.context import Context
from tcod.console import Console

from entity import Entity
from game_map import GameMap
from input_handlers import EventHandler
from procgen import generate_default_dungeon

class Engine:
    def __init__(self, entities: Set[Entity], event_handler: EventHandler, player: Entity):
        self.entities = entities
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

    def set_game_map(self, new_game_map: GameMap):
        self.game_map = new_game_map

    def handle_events(self, events: Iterable[Any]) -> None:
        for event in events:
            action = self.event_handler.dispatch(event)

            if action is None:
                continue

            action.perform(self, self.player)

    def render(self, console: Console, context: Context) -> None:
        self.game_map.render(console)

        for entity in self.entities:
            console.print(entity.x, entity.y, entity.char, fg=entity.color)

            context.present(console)

            console.clear
