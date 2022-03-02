import json
import os
import subprocess
import time
from typing import Any, Dict, List

import click
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

APPLICATION_CONFIG_PATH = "config"
DOCKER_PATH = "docker"


def setenv(*, variable: str, default: Any) -> None:
    os.environ[variable] = os.getenv(key=variable, default=default)


def app_config_file(*, config: str) -> str:
    return os.path.join(APPLICATION_CONFIG_PATH, f"{config}.json")


def docker_compose_file(*, config: str) -> str:
    return os.path.join(DOCKER_PATH, f"{config}.yml")


def read_json_configuration(*, config: str) -> Dict:
    with open(app_config_file(config=config)) as _file:
        config_data = json.load(_file)

    config_data = dict(
        (_config["name"], _config["value"]) for _config in config_data
    )

    return config_data


def configure_app(*, config: str) -> None:
    configuration = read_json_configuration(config=config)
    for key, value in configuration.items():
        setenv(variable=key, default=value)


@click.group()
def cli():
    pass


def docker_compose_cmdline(*, commands_string=None) -> None:
    config = os.getenv("APPLICATION_CONFIG")
    configure_app(config=config)
    compose_file = docker_compose_file(config=config)

    if not os.path.isfile(path=compose_file):
        raise ValueError(f"The file {compose_file } does not exist")

    command_line = ["docker-compose", "-p", config, "-f", compose_file]

    if commands_string:
        command_line.extend(commands_string.split(" "))

    return command_line


def run_sql(*, statements: List[str]) -> None:
    connection = psycopg2.connect(
        dbname=os.getenv("POSTGRES_DB"),
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD"),
        host=os.getenv("POSTGRES_HOSTNAME"),
        port=os.getenv("POSTGRES_PORT"),
    )

    connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cursor = connection.cursor()

    for statement in statements:
        cursor.execute(statement)

    cursor.close()
    connection.close()


def wait_for_logs(*, cmdline: str, meessage: str) -> None:
    logs = subprocess.check_output(cmdline)
    while meessage not in logs.decode("utf-8"):  # TODO: Make env
        time.sleep(1)
        logs = subprocess.check_output(cmdline)


@cli.command()
@click.argument("args", nargs=-1)
def test(args):
    os.environ["APPLICATION_CONFIG"] = "testing"  # TODO: make env
    configure_app(config=os.getenv(key="APPLICATION_CONFIG"))

    cmdline = docker_compose_cmdline(commands_string="up -d")
    subprocess.call(cmdline)

    cmdline = docker_compose_cmdline(commands_string="logs postgres")
    wait_for_logs(cmdline=cmdline, meessage="Ready to accept connections")

    run_sql(statements=[f"CREATE DATABASE {os.getenv(key='APPLICATION_DB')}"])

    cmdline = [
        "pytest",
        "-svv",
        "--cov=application",
        "--cov-report=term-missing",
    ]
    cmdline.extend(args)
    subprocess.call(cmdline)

    cmdline = docker_compose_cmdline(commands_string="down")
    subprocess.call(cmdline)


if __name__ == "__main__":
    cli()
