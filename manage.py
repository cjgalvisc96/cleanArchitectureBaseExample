import os
import signal
import subprocess
import time
from typing import List

import click
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

from config.config import settings


def docker_compose_file() -> None:
    return os.path.join(
        settings.DOCKER_FOLDER,
        settings.DOCKER_COMPOSE_FILE_NAME,
    )


def docker_compose_cmdline(*, commands_string=None) -> List[str]:
    compose_file = docker_compose_file()

    if not os.path.isfile(compose_file):
        raise ValueError(f"The file {compose_file} does not exist")

    command_line = [
        "docker-compose",
        "-p",
        settings.ENVIRONMENT,
        "-f",
        compose_file,
    ]

    if commands_string:
        command_line.extend(commands_string.split(" "))

    return command_line


def run_sql(*, statements: List[str]) -> None:
    conn = psycopg2.connect(
        dbname=settings.POSTGRES_DB,
        user=settings.POSTGRES_USER,
        password=settings.POSTGRES_PASSWORD,
        host=settings.POSTGRES_HOST,
        port=settings.POSTGRES_PORT,
    )

    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cursor = conn.cursor()
    for statement in statements:
        cursor.execute(statement)

    cursor.close()
    conn.close()


def wait_for_logs(*, cmdline: str, message: str) -> None:
    logs = subprocess.check_output(cmdline)
    while message not in logs.decode(settings.ENCODING_FORMAT):
        time.sleep(1)
        logs = subprocess.check_output(cmdline)


@click.group()
def cli():
    pass


@cli.command(context_settings={"ignore_unknown_options": True})
@click.argument("subcommand", nargs=-1, type=click.Path())
def compose(subcommand: str) -> None:
    cmdline = docker_compose_cmdline(commands_string=None) + list(subcommand)

    try:
        p = subprocess.Popen(cmdline)
        p.wait()
    except KeyboardInterrupt:
        p.send_signal(signal.SIGINT)
        p.wait()


@cli.command()
def init_postgres_db() -> None:
    try:
        run_sql(statements=[f"CREATE DATABASE {settings.APPLICATION_DB}"])
    except psycopg2.errors.DuplicateDatabase:
        print(
            (
                f"The database {settings.APPLICATION_DB} already",
                "exists and will not be recreated",
            )
        )


@cli.command()
@click.argument("args", nargs=-1)
def test(args: List[str]) -> None:
    cmdline = docker_compose_cmdline(commands_string="up -d")
    subprocess.call(cmdline)

    cmdline = docker_compose_cmdline(commands_string="logs postgres")
    wait_for_logs(cmdline=cmdline, message="ready to accept connections")

    run_sql(statements=[f"CREATE DATABASE {settings.APPLICATION_DB}"])

    cmdline = [
        "pytest",
        "-svv",
        "--cov=.",
    ]
    cmdline.extend(args)
    subprocess.call(cmdline)

    cmdline = docker_compose_cmdline(commands_string="down")
    subprocess.call(cmdline)


if __name__ == "__main__":
    cli()
