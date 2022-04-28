from ast import arg
from typing import List

from parser.exceptions import ValidationError

def validate(args: List[str], min_len=2):
    if len(args) < min_len:
        raise ValidationError

def parseErrorDocument(args: List[str]) -> str:
    validate(args)
    return f"error_page {args[0]} {args[1].strip()};\n\n"

def parseDirectoryIndex(args: List[str]) -> str:
    validate(args, min_len=1)
    return f'index {args[0]};\n\n'

def parseDeny(args: List[str]) -> str:
    return "deny all;\n\n"

def parseSatisfy(args: List[str]) -> str:
    return "satisfy any;\n\n"

def parseRewriteCond(args: List[str]) -> str:
    return """location / {
    rewrite ^(.*)$ https://$http_host/$1 redirect;
    if ($request_filename ~ /robots.txt){
        rewrite ^(.*)$ /robots_$http_host.txt break;
    }
}\n
"""

def parseRewriteRule(args: List[str]) -> str:
    validate(args)
    return '''location = {0} {{
    rewrite ^(.*)$ {1};
}}\n
'''.format(*args)
