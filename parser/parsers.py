from typing import List


class ValidationError(Exception):
    pass


class Parser:
    skip_next_lines: int
    config: str

    def __init__(self) -> None:
        self.skip_next_lines = 0
        self.config = ''

    def parseLine(self, config_line: str) -> None:
        if self.skip_next_lines > 0:
            self.skip_next_lines -= 1
            return

        args = config_line.split()

        result: str = ''

        if len(args) < 2:
            self.config += result
            return

        directive = args[0]
        argv = args[1:]

        # Skip unused directives
        if directive in [
            'AuthType',
            'AuthName',
            'AuthUserFile',
            'require',
            'Order',
            'RewriteEngine',
        ]:
            self.config += result
            return

        match directive:
            case 'ErrorDocument':
                result = parseErrorDocument(argv)
            case 'DirectoryIndex':
                result = parseDirectoryIndex(argv)
            case 'Deny':
                result = parseDeny(argv)
            case 'Satisfy':
                result = parseSatisfy(argv)
            case 'RewriteCond':
                self.skip_next_lines += 5
                result = parseRewriteCond(argv)
            case 'RewriteRule':
                result = parseRewriteRule(argv)
            case _:
                print('unknown directive: ' + directive)
                result = ''
        self.config += result


def validate(args: List[str], min_len: int = 2) -> None:
    if len(args) < min_len:
        raise ValidationError


def parseErrorDocument(args: List[str]) -> str:
    validate(args)
    return f'error_page {args[0]} {args[1].strip()};\n\n'


def parseDirectoryIndex(args: List[str]) -> str:
    validate(args, min_len=1)
    return f'index {args[0]};\n\n'


def parseDeny(_: List[str]) -> str:
    return 'deny all;\n\n'


def parseSatisfy(_: List[str]) -> str:
    return 'satisfy any;\n\n'


def parseRewriteCond(_: List[str]) -> str:
    return """location / {
    rewrite ^(.*)$ https://$http_host/$1 redirect;
    if ($request_filename ~ /robots.txt){
        rewrite ^(.*)$ /robots_$http_host.txt break;
    }
}\n
"""


def parseRewriteRule(args: List[str]) -> str:
    validate(args)
    return f"""location = {args[0]} {{
    rewrite ^(.*)$ {args[1]};
}}\n
"""
