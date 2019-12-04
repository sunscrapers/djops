import os
import pytest
import subprocess
import time
import logging

from cookiecutter import utils
from cookiecutter.main import cookiecutter


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("djops")


@pytest.fixture(scope="session", autouse=True)
def test_project(request):
    """
    This fixture provides a test project to test cases.
    It cookiecuts a project with the config below, runs the test and removes
    the project directory.
    """

    rendered_dir = "testproject"

    def remove_generated_project():
        if os.path.isdir(rendered_dir):
            utils.rmtree(rendered_dir)

    request.addfinalizer(remove_generated_project)

    cookiecutter(
        ".",
        no_input=True,
        extra_context={
            "project_name": "testproject",
            "production_server_name": "www.example.com",
        },
    )


def test_project_renders_to_dir():
    assert os.path.isdir("testproject")


def test_project_make_build_succeeds():
    docker_build_process = subprocess.Popen(
        "make build VERSION=0.0.0",
        shell=True,
        cwd="./testproject/",
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    for line in iter(docker_build_process.stdout.readline, b""):
        logger.info(line.decode().strip())

    for line in iter(docker_build_process.stderr.readline, b""):
        logger.warning(line.decode().strip())

    docker_build_process_return_code = docker_build_process.wait()
    assert (
        docker_build_process_return_code == 0
    ), "make build did not exit with code 0"


def test_project_make_test_succeeds():
    docker_run_process = subprocess.Popen(
        "make test",
        shell=True,
        cwd="./testproject/",
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    for line in iter(docker_run_process.stdout.readline, b""):
        logger.info(line.decode().strip())

    for line in iter(docker_run_process.stderr.readline, b""):
        logger.warning(line.decode().strip())

    docker_run_process_return_code = docker_run_process.wait()
    assert (
        docker_run_process_return_code == 0
    ), "make test did not exit with code 0"


@pytest.mark.timeout(60 * 5)
def test_project_make_up_reaches_healthy_state():
    logger.info("bringing testproject up")
    docker_run_process = subprocess.Popen(
        "make up",
        shell=True,
        cwd="./testproject/",
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    all_services_healthy = False
    while not all_services_healthy:
        time.sleep(15)
        logger.info("waiting for all services to reach healthy state")

        docker_ps_process = subprocess.Popen(
            "docker ps",
            shell=True,
            cwd="./testproject/",
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        stdout, stderr = docker_ps_process.communicate()
        stdout = stdout.decode()
        stderr = stderr.decode()

        logger.info(stdout)
        if stderr:
            logger.warning(stderr)

        assert (
            "unhealthy" not in stdout
        ), "at least one service reached unhealthy state"

        if "health: starting" not in stdout:
            all_services_healthy = True
            logger.info("all services reached healthy state")

    logger.info("terminating docker run process")
    docker_run_process.terminate()

    logger.info("bringing testproject down")
    docker_down_process = subprocess.Popen(
        "make down",
        shell=True,
        cwd="./testproject/",
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    for line in iter(docker_run_process.stdout.readline, b""):
        logger.info(line.decode().strip())

    for line in iter(docker_run_process.stderr.readline, b""):
        logger.warning(line.decode().strip())

    docker_down_process_return_code = docker_down_process.wait()
    assert (
        docker_down_process_return_code == 0
    ), "make down did not exit with code 0"
