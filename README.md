## tilda_apache2nginx.py

Script to convert .htaccess files from tilda backups to nginx configs

```
Usage: apache2nginx.py [OPTIONS]

Options:
  -i, --input-file TEXT   Path to Apache config file
  -o, --output-file TEXT  Path to generated Nginx config file
  --help                  Show this message and exit.
```

### Development

For dependency management use Poetry.

Setup venv:
```
make venv
```

Format:
```
make format
```

Lint:
```
make lint
```

Test code:
```
make test
```