![GitHub tag (latest by date)](https://img.shields.io/github/v/tag/Carsopre/dikes-for-dummies)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)


# Dikes for dummies
This repository is a Python course that explores Object Oriented programming from a Product Development perspective.
We will be creating a very simple tool from scratch described in study case. The course will provide with tools, techniques and insides on how to apply Software Engineering concepts in the most effective way. Some code snippets will be provided so that the reader can find inspiration towards building a _Minimal Viable Product_.

Each chapter can be followed with its respective branch in the repository. Therefore it is not required to 'finish' each chapter to follow the next one.

## Installation.

```shell
conda env create -f environment.yml
poetry install
```

## Documentation

### As a website:
```shell
poetry run mkdocs build
poetry run mkdocs serve
```
> Your machine should be now serving at the localhost all the available documentation.

### As pdf
First, install poetry:
```shell
poetry install
```
Next, follow the required steps of `weasyprint` https://doc.courtbouillon.org/weasyprint/stable/first_steps.html#installation

If the installation of `weasyprint` was succesful, you can now run our custom script:
```shell
poetry run build-docs
```
> A pdf named `dikesfordummies_manual.pdf` should appear at the root of your directory.