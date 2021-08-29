# Flags
DEBUG_CAMERA = False
DEBUG_COLLISION = False
DEBUG_PERF = True

TEST_COLLISIONS = True

# Window settings
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720

# Options
SHOW_PREDICTION = True

# UI settings
TITLE_SIZE_PROPORTION = 5/10
# TODO

from enum import Enum, auto

class GameState(Enum):
	ENDING = auto()
	RUNNING = auto()
	PAUSED = auto()

class EditorState(Enum):
	NOTHING = auto()
	EDITING = auto()
	ADDING = auto()

class GameEntity(Enum):
	PLANET = auto()
	WORMHOLE = auto()
