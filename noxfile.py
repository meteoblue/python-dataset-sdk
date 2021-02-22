import nox


@nox.session(reuse_venv=True)
def lint(session):
    lint_tools = ["flake8", "black", "isort"]
    targets = ["meteoblue_dataset_sdk", "tests", "noxfile.py"]
    session.install(*lint_tools)
    session.run("isort", *targets)
    session.run("black", *targets)
    session.run("flake8", *targets)


@nox.session()
def tests(session):
    session.install("-r", "./requirements.txt")
    session.run("pytest", "-v")
