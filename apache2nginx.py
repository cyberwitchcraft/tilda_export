#! /usr/bin/env python3

import click

from parser.parsers import parseDeny, parseDirectoryIndex, parseErrorDocument, parseRewriteCond, parseRewriteRule, parseSatisfy

skip_next_lines: int = 0


@click.command()
@click.option("-i", "--input-file", default="htaccess", help="Path to Apache config file")
@click.option("-o", "--output-file", default="nginx.conf", help="Path to generated Nginx config file")
def apache2nginx(input_file: str, output_file: str):
    config: str = ""

    with open(input_file, "r") as file:
        for line in file.readlines():
            config += parseLine(line)

    with open(output_file, "w") as file:
        file.write(config)


def parseLine(config_line: str) -> str:
    global skip_next_lines
    if skip_next_lines > 0:
        skip_next_lines -= 1
        return ""

    args = config_line.split()

    if len(args) < 2:
        return ""

    directive = args[0]
    argv = args[1:]

    # Skip unused directives
    if directive in ["AuthType", "AuthName", "AuthUserFile", "require", "Order", "RewriteEngine"]:
        return ""

    match directive:
        case "ErrorDocument":
            return parseErrorDocument(argv)
        case "DirectoryIndex":
            return parseDirectoryIndex(argv)
        case "Deny":
            return parseDeny(argv)
        case "Satisfy":
            return parseSatisfy(argv)
        case "RewriteCond":
            skip_next_lines += 5
            return parseRewriteCond(argv)
        case "RewriteRule":
            return parseRewriteRule(argv)
        case _:
            print("unknown directive: " + directive)
            return ""


if __name__ == "__main__":
    apache2nginx()
