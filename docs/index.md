# Dikes For Dummies
Dikes for dummies is a "fast" Python course that navigates the creation of a Minimal Viable Product (MVP) starting by the project creation until document publishment while having a look on Object Oriented principles and the building of your own test suite to increase your code quality.

## Requirements.
For simplicity reasons we recommend having the following installed in your computer.

* [Anaconda](https://www.anaconda.com/) latest version (Python >= 3.9)
    * It is suggested to include it in the system's Path to operate fully through console.
* [Visual Studio Code](https://code.visualstudio.com/). (Easy to install through Anaconda suite). 
    * Other IDEs like PyCharm are totally acceptable, however the debugging steps described in the chapters are aimed for VSCode.

## Study case

During the walk-through the chapters, we will see snippets of code that can help the reader build on their own a solution that satisfies the [study case](docs\study_case.md). Sometimes the snippets will not be enough, this is totally intended. However, if the reader gets lost contact me for a branch of the source repository that will lead you from that chapter onwards.

To 'take-on' from any chapter branch, you just need to do the following:
```bash
conda env create -f environment.yml
conda activate dikes-for-dummies_env
poetry install
```

## Chapters and intended order:
1. [Project setup](docs\chapters\01_project_setup.md)
2. [Never trust the user](docs\chapters\02_never_trust_the_user.md)
3. [Object Oriented Programming](docs\chapters\03_objected_oriented_programming.md)
4. [The pythonic way](docs\chapters\04_the_pythonic_way.md)
5. [Testing 101](docs\chapters\05_testing_101.md)
6. [Creating interfaces](docs\chapters\06_creating_interfaces.md)
7. [Creating documentaiton](docs\chapters\07_creating_documentation.md)
8. [Building the tool](docs\chapters\08_building_the_tool.md)