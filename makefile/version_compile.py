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
