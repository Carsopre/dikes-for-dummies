# Chapter 07. Creating documentation
We will create now very simple documentation. What we will do is to generate technical documentation from our `docstrings`, our changelog, and some simple usage instructions

## Mkdocs
 For this chapter we will only be using [Mkdocs](https://www.mkdocs.org/). As described in their page, Mkdocs creates static HTML pages that can be published anywhere. This can also be integrated in a GitHub workflow

### Installing the dependencies.
```console
 poetry add mkdocs --group dev
 poetry add mkdocs-material --group dev
 poetry add mkdocstrings-python --group dev
```

### Defining a theme.

 We will need a configuration file `mkdocs.yml` describing the way of building our documentation and its [theme](https://www.mkdocs.org/user-guide/choosing-your-theme/).

```yaml
site_name: Dikes for dummies documentation
theme:
  name: material
  language: en
  icon:
    logo: fontawesome/solid/house-tsunami
  palette:
    - scheme: dummies
      toggle:
        icon: material/lightbulb-outline
        name: Switch to dark mode
    - scheme: slate
      toggle:
        icon: material/lightbulb
        name: Switch to light mode
  features:
    - navigation.instant
    - navigation.tracking
    - navigation.tabs
    - navigation.sections
    - navigation.expand
    - navigation.top
plugins:
  - search
  - autorefs
  - mkdocstrings:
      default_handler: python
      handlers:
        python:
          rendering:
            show_root_toc_entry: false
            show_source: true
            show_signature_annotations: true
            heading_level: 3
            show_category_heading: false
            group_by_category: false
          selection:
            inherited_members: false

      custom_templates: templates
watch:
    - dikesfordummies/
markdown_extensions:
  - pymdownx.highlight
  - pymdownx.superfences
  - admonition
  - toc:
      permalink: true
repo_url: https://github.com/Carsopre/dikes-for-dummies
repo_name: carsopre/dikes-for-dummies
extra:
  social:
    - icon: fontawesome/brands/github
      link: https://github.com/Carsopre/dikes-for-dummies
      name: Source code
copyright: Copyright &copy; 2022 Carsopre
```

### Building and serving

It is required to build the documentation in order to serve it

```console
 poetry run mkdocs build
 poetry run mkdocs serve
```
 > Your local machine should now work as a localhost for the documentation pages.

### Adding user's documentation.

In \docs we need to create a landing page named `index.md`. Within this directory we can now create as many documentation as we want either spread in files across the \docs root or in different subdirectories.

Note that if you already configured commitizen you should have also a `changelog.md` file in the docs root. Otherwise, try the following:
`cz changelog`
> Keep in mind only those commits following the `commitizen` rules will be shown.

### Adding technical documentation.

Creating a technical reference it's easier done than said. Just mirror your solution tree-directory and create one *.md page per module.
For instance, if we have:
```properties
\dikesfordummies
    \dike
        dike_input.py
        dike_profile.py
        dike_profile_builder.py
```
And we want to show their docstrings, we will create the following document  `\docs\reference\dike.md` containing:

``
# Dike models for the Dikes for Dummies package
Technical documentation for the classes and methods within the /dike module.

## Dike Profile
::: dikesfordummies.dike.dike_profile

## Dike Profile Builder
::: dikesfordummies.dike.dike_profile_builder

## Dike Input
::: dikesfordummies.dike.dike_input
``


## GitHub Pages

If your project is public and documentation built with MkDocs, there is no reason why you should not want to do this, as it's easy and fast.

### Workflow
Create a new workflow in `.github\workflows\` with the settings required to install and run your tool

```yaml
name: docs
on:
  push:
    branches:
      - master
jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-python@v2
        with:
          python-version: ['3.10']

      - name: Run image
        uses: abatilo/actions-poetry@v2.0.0
        with:
          poetry-version: 1.1.8
      - name: Cache Poetry virtualenv
        uses: actions/cache@v1
        id: cache
        with:
          path: ~/.virtualenvs
          key: venv-${{ matrix.os }}-${{ matrix.python-version }}-${{ hashFiles('**/poetry.lock') }}
          restore-keys: |
            venv-${{ matrix.os }}-${{ matrix.python-version }}-

      - name: Set Poetry config
        run: |
          poetry config virtualenvs.in-project false
          poetry config virtualenvs.path ~/.virtualenvs

      - name: Install Dependencies
        run: poetry install
        if: steps.cache.outputs.cache-hit != 'true'

      - run: poetry run mkdocs gh-deploy --force
```

### Settings
We need to enable the feature in GitHub:
`settings -> Pages -> Build and Deployment`
* Source `deploy from a branch`
* Branch `gh-pages -> / (root)` (you may require to do a first build).

If everything went well you should be able to access your built documentation in https://{your-organization}.github.io/{your-repo-name}/
