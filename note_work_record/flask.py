# flask

## blueblog

修改该函数的default 值，改为0.0.0.0 开放防火墙端口即可访问该博客

./env/lib/python3.6/site-packages/flask/cli.py:780:@click.option("--host", "-h", default="127.0.0.1", help="The interface to bind to.")


