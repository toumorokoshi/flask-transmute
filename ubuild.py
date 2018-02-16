import os
import subprocess
from uranium import task_requires


def main(build):
    build.packages.install(".", develop=True)


def test(build):
    main(build)
    build.packages.install("pytest")
    build.packages.install("pytest-cov")
    build.executables.run([
        "py.test", "--cov", "flask_transmute",
        "flask_transmute/tests",
        "--cov-report", "term-missing"
    ] + build.options.args)


def publish(build):
    """ distribute the uranium package """
    build.packages.install("wheel")
    build.executables.run([
        "python", "setup.py",
        "sdist", "bdist_wheel", "--universal", "upload", "--release"
    ])


def build_docs(build):
    build.packages.install("Sphinx")
    return subprocess.call(
        ["make", "html"], cwd=os.path.join(build.root, "docs")
    )

@task_requires("main")
def run_example(build):
    """ run the example server. """
    build.packages.install("gunicorn")
    subprocess.call([
        "gunicorn", "flask_transmute.tests.example:app",
        "-c", os.path.join(build.root, "flask_transmute", "tests", "gunicorn_config.py")
    ])
