# Chapter 08. Building the tool

Catching up? Just run the following command in your command line:
```
conda env create -f environment.yml
conda activate dikes-for-dummies_env
poetry install
```

You can follow the contents of this chapter now :)

## Intro
We come to our last step. We already cover the different types of audiences we may have. But let's revise it from [Chapter 06](./06_creating_interfaces.md#know-your-audience):

| Usage / Requirements | Endpoints | Built | 
| ---   | :---: | :---: |
| Sandbox | - | - |
| Library | - | - |
| CLI | x | (Not necessarily) |
| API | x | (Running as a service) |
| GUI | x | x |

We only require to really build an exe when having a stand alone GUI. However we will see two ways of delivering our tool here:
1. As a built package.
2. As an exe.

## Building and publishing our package.

Throughout the entire Dikes For Dummies workshop we have been using `Poetry`. If your dependencies are still holding up and your project is well structure you should not have too much troubles [building and publishing](https://python-poetry.org/docs/cli/#build) it. Let's check it.

```bash
poetry check
```
> All set!

```bash
poetry build & poetry publish
```
> You will be required to authenticate yourself in pypi

Notice that most likely a `dist` directory has been created in your root directory with the wheels to be published. After publishing our package we should be able to add it as a dependency on other projects!

```bash
poetry add dikes-for-dummies
```

## As an exe

This step will require (a bit) more of work. First we require the [`pyinstaller`](https://pyinstaller.org/en/stable/) package (`poetry add pyinstaller --group dev`).

### An ideal world
In theory, the following should be possible:

* Building only the CLI: `poetry run pyinstaller dikesfordummies\main.py`
* Building with GUI: `poetry run pyinstaller dikesfordummies\gui\main.py`

However, it is entirely possible that as more complex your repository starts to be, the more dependencies you need to specify yourself. This might result on you having to create your custom `main.spec`file and your own compilation script for `pyinstaller`. We will describe these steps in the next sections. For that, lets create both files in a `\makefile` dir in our root.

### __init__.py

Because we want our scripts to be findable and executable, we can create an `__init__.py` file that will also provide us some help:

```python
from pathlib import Path

import dikesfordummies

_makedir = Path(__file__).parent
_dfd_version = dikesfordummies.__version__
```

### main.spec

```python
# -*- mode: python -*-
from PyInstaller.utils.hooks import collect_data_files, collect_dynamic_libs
import glob, os
from pathlib import Path
from makefile import _makedir

_conda_env = os.environ['CONDA_PREFIX']

_root_dir = _makedir.parent
_dfd_src = _root_dir / "dikesfordummies"

a = Analysis([r"..\\dikesfordummies\\gui\\main.py"],
             pathex=['.', str(_dfd_src), _conda_env],
             hiddenimports=[],
             hookspath=None,
             runtime_hooks=None,
             datas=[],
             binaries= collect_dynamic_libs("rtree"),)
			 
for d in a.datas:
    if 'pyconfig' in d[0]: 
        a.datas.remove(d)
        break

print("Generate pyz and exe")
pyz = PYZ(a.pure)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='DikesForDummies.exe',
          debug=False,
          strip=False,
          upx=True,
          console=False,
		#   icon=f"",
		#   version=str(_makedir / 'version.txt')
        )

```

### Defining our custom compiler

```python
import datetime
import os
import shutil
import sys
from pathlib import Path

from makefile import _dfd_version, _makedir

# __version__ is automatically updated by commitizen, do not change manually.
# Run insted 'cz bump --changelog' and then 'git push --tags' and 'git push'.
_version_file = _makedir / "version.txt"
_main_spec = _makedir / "main.spec"


def read_revision():
    # date
    now = datetime.datetime.now()
    if _version_file.is_file():
        _version_file.unlink()

    _version_as_string = _dfd_version.replace(".", ",")
    _vs_version_info = f"{_version_as_string}, 0"
    with _version_file.open("w") as f:
        f.write(
            "VSVersionInfo(\n"
            + "ffi=FixedFileInfo(\n"
            + f"filevers=({_vs_version_info}),\n"
            + f"prodvers=({_vs_version_info}),\n"
            + "mask=0x3f,\n"
            + "flags=0x0,\n"
            + "OS=0x40004,\n"
            + "fileType=0x1,\n"
            + "subtype=0x0,\n"
            + "date=(0, 0)\n"
            + "),\n"
            + "kids=[\n"
            + "StringFileInfo(\n"
            + "[\n"
            + "StringTable(\n"
            + "u'040904B0',\n"
            + "[StringStruct(u'CompanyName', u'Dummies'),\n"
            + "StringStruct(u'FileDescription', u'DikesForDummies'),\n"
            +
            # "StringStruct(u'FileVersion', u'" + str(version) + "'),\n" +
            "StringStruct(u'InternalName', u'DikesForDummies'),\n"
            + "StringStruct(u'LegalCopyright', u'Dummies"
            + r" \xae "
            + str(now.year)
            + "'),\n"
            + "StringStruct(u'OriginalFilename', u'DikesForDummies.exe'),\n"
            + "StringStruct(u'ProductName', u'DikesForDummies"
            + r" \xae "
            + "Dummies'),\n"
            + f"StringStruct(u'ProductVersion', u'{_dfd_version}')])\n"
            + "]), \n"
            + "VarFileInfo([VarStruct(u'Translation', [1033, 1200])])\n"
            + "]\n"
            + ")"
        )


def compile_code():
    def _remove_if_exists(dir_name: str):
        _dir_to_remove = _makedir.parent / dir_name
        if (_dir_to_remove).is_dir():
            shutil.rmtree(_dir_to_remove)

    _remove_if_exists("dist")
    _remove_if_exists("build")
    _py_installer_exe = Path(sys.exec_prefix) / "Scripts" / "pyinstaller.exe"
    assert _py_installer_exe.is_file()
    os.system(f"{_py_installer_exe} --clean {_main_spec}")
    _version_file.unlink()


def run_compilation():
    read_revision()
    compile_code()


if __name__ == "__main__":
    run_compilation()

```

Let's run it!

```bash
poetry run python makefile\version_compile.py
```
> After some time you should fin in /dist your DikesForDummies.exe

### Extending our poetry config

We can create a 'shortcut' to our compilation script so that with a single `poetry run build-exe` call everthing is executed within our safe virtual environment.

```ini
[tool.poetry.scripts]
build-exe = "makefile.version_compile:run_compilation"
```


## Summary

We have finaly covered all steps required to build an MVP. There are many different ways to come to this final step, however, that is the nice challenge about python. Explore all its possibilities and don't be shy about asking or sharing your progress. 
Happy coding!