# Swing-bye-py

## TODO

Rendering

- [X] Fix background parallax on resize
- [X] Create Background class to hold all stars and background image
- [ ] Give each level a seed to keep the background consistant
- [X] Fix weird glitch with hiding / unhiding Graph (becomes blocky for some reason?)
- [ ] Planet / comet labels
- [X] Texture comets
- [X] FIX THE GODDAMN CAMERA (Y A T T A)
- [X] KE and PE graphs
- [ ] Find out why button text sometimes appears bellow the button

Code structure and stuff

- [ ] Correctly dispose of useless sprites / paths
- [ ] Combine WorldState and GameState

UI

- [ ] Make it not ugly
- [ ] Custom main menu w/ animations?
- [ ] Make options actually do something
- [ ] Make level selection work

Physics

- [X] Ship prediction
- [X] Orbit lines
- [X] KE and PE
- [X] optimize physics in c++

Game

- [ ] Make more levels
- [ ] Animations on level entry (e.g. zoom in, time autoscroll, cutscene????)
- [ ] Add the goal (black hole?) to the levels
- [ ] Integrate easter eggs
- [ ] Make ship hitbox smaller than sprite
- [X] Make functional level editor
- [X] Allow for exporting worlds from the editor
- [ ] Allow to add ship in editor

Structure

- [ ] use git submodules for the pybind11-smart_holder dependency
