import nox

TARGETS = ["meteoblue_dataset_sdk", "tests", "noxfile.py"]


@nox.session(reuse_venv=True)
def lint(session):
    lint_tools = ["flake8", "isort"]
    session.install(*lint_tools)
    session.run("isort", *TARGETS)
    session.run("flake8", *TARGETS)


@nox.session(reuse_venv=True)
def lint_dev(session):
    lint_tools = ["flake8", "black", "isort"]
    session.install(*lint_tools)
    session.run("isort", "-f", *TARGETS)
    session.run("black", *TARGETS)
    session.run("flake8", *TARGETS)


@nox.session(reuse_venv=True)
def tests(session):
    session.install("-e", ".[dev]")
    session.run("pytest", "-v")
