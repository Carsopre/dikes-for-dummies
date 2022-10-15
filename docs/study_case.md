# Study Case
We want to create a tool capable of calculating the geometry for a dike reinforcement. 

A dike reinforcement is a series of operations that take place on a previously defined dike. These operations will afect its structure, and therefore its geometry.

__The user will provide the following input:__

- Dike profile characteristic points (8 points, 4 polderside, 4 waterside).
- Reinforcement data:
    - Height
    - Width
    - Cost of material.

__The user wants to know:__

- The costs for all possible reinforcements with the data given.
- The geometries for all possible reinforcements with the data given.

## Minimal functional requirements.
- The tool can be used a python library.
- The tool outputs the data to a directory given by the user.

## Minimal non-functional requirements.
- The tool has 80% code coverage.
- The tool has no failing tests.
- The public methods are documented.

## Extra
- The tool accepts an ini file (or other) containing all required input data.
- The tool generates all output in one file.
- The tool has a CLI interface.
- The tool has a GUI interface.
- The tool can be run as a stand-alone exe.
- Both minimal functional and non-fuctional requirements should still be met.