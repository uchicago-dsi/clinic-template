# Clinic Cookiecutter

The goal of this repository is to be a central location for templating University of Chicago Data Clinic projects. When updating this repository the following principals should be followed:
- Low overhead on developers: This cookiecutter is meant to create templates that can be used to quickly spin up new project repositories. Adding additional steps post creation or an endless series of prompts will reduce its usefullness. 
- Up to date with best practices: The tools used here should adhere as closely as possible to modern and popular methods
- Justify decisions: Decisions should be justified so future collaborators can make informed decisions as conditions change

## Usage

1. Install cookiecutter. `pip install cookiecutter`
1. Select this template to create a repository in the current directory. `cookiecutter gh:ORG/REPO`
1. Follow the prompts in your terminal.


### Notes once complte
The file ``DataPolicy.md" contains the _default_ data and code sharing policies for the project.
Protect main and dev


## Linter

To check for style, we use `flake8`, `black`, and `isort`. These are all run using `pre-commit`. [pre-commit](https://pre-commit.com/) is a tool for managing git hook scripts that we can use to run code checkers before git actions (like run `flake8` before every commit). If it fails, the commit will be blocked and the user will be shown what needs to be changed. We configure our linters with [setup.cfg](https://docs.python.org/3/distutils/configfile.html)


## GitHub

To run checkers on pull requests to `main` and `dev`, we use the `.github/workflows/main.workflow.yml` file.

## Contributing

The root directory of this repository contains files related to the cookiecutter itself. All generated repositories will have `{{ cookiecutter.project_slug }}` as its root directory. To make additions that are dependent on user prompts, add the variable to the `cookiecutter.json` file and reference the variable withing the `{{ cookiecutter.project_slug }}` directory using Jinja templating. 

For more information on cookiecutter, visit its [git repository](https://github.com/cookiecutter/cookiecutter)