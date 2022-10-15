# Chapter 01. Project setup
In this Chapter we will be setting up the project and our VScode settings.

## IDE's and recommended plugins.
Setting up the project starts by selecting an IDE. We will use VSCode out of personal satisfactory experience and the well integration of pluggins that help on debugging or code maintainance tasks.
The first thing to do with VSCode is to create our own configuration for the project. You can either do this via the interface or my preferred method by creating a `settings.json` file in the `.vscode` directory located in the root of the project such as follows:
```json
{
    "terminal.integrated.profiles.windows": {
        "conda": {
            "path": "C:\\Windows\\System32\\cmd.exe",
            "args": [
                "/K",
                "C:\\Anaconda3\\Scripts\\activate.bat",
                "C:\\Anaconda3"
            ]
        }
    },
    "terminal.integrated.defaultProfile.windows": "Command Prompt",
    "terminal.integrated.cwd": "${workspaceFolder}",
    "editor.minimap.enabled": false,
    "editor.formatOnSave": true,
    "python.formatting.provider": "black",
    "python.defaultInterpreterPath": "C:\\Anaconda3\\envs\\dikes-for-dummies_env\\python.exe",
    "python.terminal.activateEnvironment": true,
    "python.linting.mypyEnabled": false,
    "python.linting.enabled": true,
    "python.testing.cwd": "${workspaceFolder}",
    "python.testing.unittestEnabled": false,
    "python.testing.pytestEnabled": true,
    "python.testing.pytestArgs": [
        ""
    ],
    "autoDocstring.startOnNewLine": true,
    "autoDocstring.docstringFormat": "google",
    "[python]": {
        "editor.formatOnSave": true,
        "editor.codeActionsOnSave": {
            "source.organizeImports": true
        }
    },
    "python.sortImports.args": [
        "--profile=black"
    ],
}
```
As can be seen, we are declaring already the usage of certain python libraries such as `black` and `pytest`, plugins from VSCode such as `autoDocstring`, and an anaconda environment to contain our working environment dependencies on it.
It is also advised to include the `.vscode` directory in the .gitignore file.

Some recommended plugins (extensions) I usually have always on in VSCode:
- [Python](https://marketplace.visualstudio.com/items?itemName=ms-python.python). Basically the only plugging that is non-officially **required** to code in Python. It will help you with linting, debugging, code-formatting, refactor, etc.
- [autoDocstring](https://marketplace.visualstudio.com/items?itemName=njpwerner.autodocstring). A **must** for automatically generating docstring headers anywhere in your code.
- [Lorem ipsum](https://marketplace.visualstudio.com/items?itemName=Tyriar.lorem-ipsum). Very handy to generate texts for testing purposes.
- [Test Explorer UI](https://marketplace.visualstudio.com/items?itemName=hbenl.vscode-test-explorer) Better test ordering and in-code runner.

Of course there are many more, don't be shy and explore whatever fits best your needs.

## Adding dependencies.
One of the biggest issues in python packaging is keeping all the dependencies derived from your packages in order as some of them have strong version requirements with third party libraries.

To deal with this problem you can either always keep an eye on this yourself or instead take advantage of package handlers such as [poetry](https://python-poetry.org/). Poetry is capable of installing all of your required dependencies while keeping them to the optimal version between themselves. All its work will be usually declared in a `pyproject.toml` file that can be modified via poetry commands or manually.

However, poetry won't be able to install a package if this requires certain `wheels`. In short, a `wheel` is a pre-compiled library that cannot be natively installed in your system. 

A good example is [GDAL](https://gdal.org/).
To solve this problem the easiest solution when working on a Windows machine is to have a `conda environment` running on the background. Anaconda can install for us mentioned wheel which will allow poetry to add it to our package without further conflicts. Example:

```console
 conda install -c conda-forge gdal=3.0.2
 poetry add gdal
```
An example of a conda environment that requires wheels can be as follows:

```yaml
name: projectwithwheels_env
channels:
  - defaults
  - conda-forge
dependencies:
  - conda-forge::python>=3.8
  - conda-forge::rasterio
  - conda-forge::gdal
  - conda-forge::geos
  - conda-forge::fiona
  - pip
  - pip:
    - pytest
    - pytest-cov
    - teamcity-messages
    - poetry
```

Let's install the provided environment.yml file and start our poetry project.

```console
conda install env -f environment.yml
conda activate dikes-for-dummies_env
poetry init
```
When running `poetry init` the console will start an interactive mode in which we will be able to add dependencies both for packaging but also for development (think of code formatting libraries, testing or documentation libraries for the latter). Feel free to explore it a bit, the next step will contain a stable `*.toml` file.

Once we are done with adding dependencies we will create the `src` directory under a recognisable name (but can be src as well) in it we will add our first [`__init__.py`](https://stackoverflow.com/questions/448271/what-is-init-py-for) file with the current version of the tool:
```python
__version__ = "0.1.0"
```
This can be also done with [commitizen](https://commitizen-tools.github.io/commitizen/). This tool helps us versioning the project and keeping a neat changelog.

Now we can install our package to start working on it
```console
poetry install
```

## Documentation.
There are as many documentation packages as you  may imagine. But of course you want to use the most popular ones to ensure easy 'troubleshooting' when problems occur.
Some commonly used are:
- [Sphinx](https://www.sphinx-doc.org/en/master/). Easy to deploy and quite broadly used in pypi packages.
- [Mkdocs](https://www.mkdocs.org/). Easy to use as it follows very clear structures and documentation is written with markdown language.

Most of them are capable of reading your code docstrings and generating such technical documentation for developers. So in the end you should pick the one that adapts best to your workflows and knowledge.
At the same time, you may chose to generate documentation and publish it in pages such as [Read the docs](https://readthedocs.org/) or [GitHub Pages](https://pages.github.com/).

## Publishing / Delivering.
Last, the ultimate goal of creating a product is to deliver it. We have several options:
- Create a pypi package. Users can import our package through `pip` or `poetry`. Building the package and pushing it to pypi it's relatively easy with `poetry`.
- Create an .exe. With the help of packages such as `pyinstaller` we can easily achieve this.

All of the above are, however, not exclusive. We need to consider that our package will have different audiences that will use it in different manners:
- as sandbox (think of developers extending the project)
- as a library (pypi package or [directly from GitHub](https://stackoverflow.com/questions/20101834/pip-install-from-git-repo-branch/20101940#20101940)).
- as an endpoint tool (think of an exe with limited workflows):
    - CLI
    - API
    - GUI
    - Web server