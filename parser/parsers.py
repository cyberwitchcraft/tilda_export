from typing import List


class ValidationError(Exception):
	pass

STATIC_CONFIG = """
server {
	listen 80;
	server_name ${DOMAIN} www.${DOMAIN};
	root /opt/tilda-archive;
	index page26167577.html;
	error_page 404 /page26167932.html;
	error_page 403 /page26167932.html;

	access_log /var/log/nginx/sites/tilda-archive.access;
	error_log /var/log/nginx/sites/tilda-archive.error;

	listen 443 ssl; # managed by Certbot
	ssl_certificate /etc/letsencrypt/live/${DOMAIN}/fullchain.pem; # managed by Certbot
	ssl_certificate_key /etc/letsencrypt/live/${DOMAIN}/privkey.pem; # managed by Certbot
	include /etc/letsencrypt/options-ssl-nginx.conf; # managed by Certbot
	ssl_dhparam /etc/letsencrypt/ssl-dhparams.pem; # managed by Certbot
"""

class Parser:
    skip_next_lines: int
    _config: str

    def __init__(self) -> None:
        self.skip_next_lines = 0
        self._config = STATIC_CONFIG + "\n"

    def config(self) -> str:
        return self._config + "}\n"

    def parseLine(self, config_line: str) -> None:
        if self.skip_next_lines > 0:
            self.skip_next_lines -= 1
            return

        args = config_line.split()

        result: str = ''

        if len(args) < 2:
            self._config += result
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
            self._config += result
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
        self._config += result


def validate(args: List[str], min_len: int = 2) -> None:
    if len(args) < min_len:
        raise ValidationError


def parseErrorDocument(args: List[str]) -> str:
    validate(args)
    return f'\terror_page {args[0]} {args[1].strip()};\n\n'


def parseDirectoryIndex(args: List[str]) -> str:
    validate(args, min_len=1)
    return f'\tindex {args[0]};\n\n'


def parseDeny(_: List[str]) -> str:
    return '\tdeny all;\n\n'


def parseSatisfy(_: List[str]) -> str:
    return '\tsatisfy any;\n\n'


def parseRewriteCond(_: List[str]) -> str:
    return """\tlocation / {
    	rewrite ^(.*)$ https://$http_host/$1 redirect;
    	if ($request_filename ~ /robots.txt){
    		rewrite ^(.*)$ /robots_$http_host.txt break;
    	}
	}\n
"""


def parseRewriteRule(args: List[str]) -> str:
    validate(args)
    return f"""
	location = {args[0]} {{
		rewrite ^(.*)$ {args[1]};
	}}\n
"""
