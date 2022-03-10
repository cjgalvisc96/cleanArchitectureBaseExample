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


def get_docker_compose_command(*, commands_string=None) -> List[str]:
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


def execute_sql_command(*, statements: List[str]) -> None:
    def get_postgres_connection() -> psycopg2.connect:
        postgres_connection = psycopg2.connect(
            dbname=settings.POSTGRES_DB,
            user=settings.POSTGRES_USER,
            password=settings.POSTGRES_PASSWORD,
            host=settings.POSTGRES_HOSTNAME,
            port=settings.POSTGRES_PORT,
        )
        return postgres_connection

    def execute_statements(*, connection: psycopg2.connect) -> None:
        """
        ISOLATION_LEVEL_AUTOCOMMIT = For allow to commads like "CREATE DATABASE" execute()
        without use commit()
        """
        connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = connection.cursor()
        for statement in statements:
            cursor.execute(statement)

        cursor.close()
        connection.close()

    connection = get_postgres_connection()
    execute_statements(connection=connection)


@click.group()
def cli():
    pass


@cli.command(context_settings={"ignore_unknown_options": True})
@click.argument("subcommand", nargs=-1, type=click.Path())
def compose(subcommand):
    cmdline = get_docker_compose_command() + list(subcommand)

    try:
        p = subprocess.Popen(cmdline)
        p.wait()
    except KeyboardInterrupt:
        p.send_signal(signal.SIGINT)
        p.wait()


@cli.command()
def init_postgres():
    try:
        execute_sql_command([f"CREATE DATABASE {settings.APPLICATION_DB}"])
    except psycopg2.errors.DuplicateDatabase:
        print(
            (
                f"The database {settings.APPLICATION_DB} already",
                "exists and will not be recreated",
            )
        )


@cli.command()
@click.argument("args", nargs=-1)
def runtests(args: List[str]) -> None:
    def down_docker() -> None:
        docker_compose_command = get_docker_compose_command(
            commands_string="down"
        )
        subprocess.call(docker_compose_command)

    def up_docker() -> None:
        docker_compose_command = get_docker_compose_command(
            commands_string="up -d"
        )
        subprocess.call(docker_compose_command)

    def wait_for_logs(*, cmdline: str, message: str) -> None:
        logs = subprocess.check_output(cmdline)
        while message not in logs.decode(settings.ENCODING_FORMAT):
            time.sleep(1)
            logs = subprocess.check_output(cmdline)

    def prepare_postgres_container_for_connections() -> None:
        docker_compose_command = get_docker_compose_command(
            commands_string="logs postgres"
        )
        wait_for_logs(
            cmdline=docker_compose_command,
            message="ready to accept connections",
        )

    def create_postgres_db() -> None:
        statement = f"CREATE DATABASE {settings.APPLICATION_DB}"
        execute_sql_command(statements=[statement])

    def execute_tests() -> None:
        cmdline = [
            "pytest",
            "-svv",
            "--cov=.",
        ]
        cmdline.extend(args)
        subprocess.call(cmdline)

    down_docker()  # to avoid errors in DB creation
    up_docker()
    prepare_postgres_container_for_connections()
    create_postgres_db()
    execute_tests()
    down_docker()


if __name__ == "__main__":
    cli()
