import re
from typing import List, Optional


class ValidationError(Exception):
    pass


STATIC_CONFIG = """server {
	listen 80;
	server_name ${DOMAIN} www.${DOMAIN};
	root /opt/tilda-archive;

	access_log /var/log/nginx/sites/tilda-archive.access;
	error_log /var/log/nginx/sites/tilda-archive.error;

	listen 443 ssl; # managed by Certbot
	ssl_certificate /etc/letsencrypt/live/${DOMAIN}/fullchain.pem; # managed by Certbot
	ssl_certificate_key /etc/letsencrypt/live/${DOMAIN}/privkey.pem; # managed by Certbot
	include /etc/letsencrypt/options-ssl-nginx.conf; # managed by Certbot
	ssl_dhparam /etc/letsencrypt/ssl-dhparams.pem; # managed by Certbot"""


class Parser:
    _config: str

    def __init__(self) -> None:
        self._config = STATIC_CONFIG + "\n"

    def config(self) -> str:
        return self._config + "}\n"

    def parse_line(self, config_line: str) -> None:
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
            'Deny',
            'Satisfy',
            'RewriteCond'
        ]:
            self._config += result
            return

        if directive == 'RewriteRule':
            result = parse_rewrite_rule(argv)
        else:
            result = ''
        self._config += result


def validate(args: List[str], min_len: int = 2) -> None:
    if len(args) < min_len:
        raise ValidationError


def parse_rewrite_rule(args: List[str]) -> Optional[str]:
    validate(args)

    if "HTTP_HOST" in args[1]:
        return ''

    return f"""
    location = {args[0]} {{
        rewrite ^(.*)$ {args[1]};
    }}
"""
