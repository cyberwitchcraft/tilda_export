#! /usr/bin/env python3

import sys
from parser.parsers import Parser, ValidationError

import click


@click.command()
@click.option(
    '-i', '--input-file', default='htaccess', help='Path to Apache config file'
)
@click.option(
    '-o',
    '--output-file',
    default='nginx.conf',
    help='Path to generated Nginx config file',
)
def apache2nginx(input_file: str, output_file: str) -> None:
    parser = Parser()

    with open(input_file, 'r', encoding='utf-8') as file:
        for i, line in enumerate(file.readlines()):
            try:
                parser.parse_line(line)
            except ValidationError:
                click.echo(f'failed to parse line {i}: {line}')
                sys.exit(1)

    with open(output_file, 'w', encoding='utf-8') as file:
        file.write(parser.config())


if __name__ == '__main__':
    apache2nginx()  # pylint: disable=no-value-for-parameter
