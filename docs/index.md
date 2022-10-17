# Dikes For Dummies
Dikes for dummies is a "fast" Python course that navigates the creation of a Minimal Viable Product (MVP) starting by the project creation until document publishment while having a look on Object Oriented principles and the building of your own test suite to increase your code quality.

## Requirements.

For simplicity reasons we recommend having the following installed in your computer:

- [Anaconda](https://www.anaconda.com/) latest version (Python >= 3.9).

  - It is suggested to include it in the system's Path to operate fully through console.

- [Visual Studio Code](https://code.visualstudio.com/). (Easy to install through Anaconda suite). 

  - Other IDEs like PyCharm are totally acceptable, however the debugging steps described in the chapters are aimed for VSCode.

## Following from a chapter.

During the walk-through the chapters, we will see snippets of code that can help the reader build on their own a solution that satisfies the [study case](.\study_case.md). Sometimes the snippets will not be enough, this is intended. However, if the reader gets lost they can check out the corresponding branch for each chapter.

To 'take-on' from any chapter branch, you just need to do the following:

```console
conda env create -f environment.yml
conda activate dikes-for-dummies_env
poetry install
```