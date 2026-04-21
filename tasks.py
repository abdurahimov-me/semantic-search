from invoke import task


@task(iterable=["file"])
def logs(c, file):
    files = file or ["gunicorn_error", "gunicorn_access"]
    paths = " ".join(f"app/logs/{f}.log" for f in files)
    c.run(f"tail -f {paths}", pty=True)


@task
def logs_django(c):
    files = ["gunicorn_error", "gunicorn_access"]
    paths = " ".join(f"app/logs/{f}.log" for f in files)
    c.run(f"tail -f {paths}", pty=True)


@task
def logs_daphne(c):
    files = ["daphne_error", "daphne_access"]
    paths = " ".join(f"app/logs/{f}.log" for f in files)
    c.run(f"tail -f {paths}", pty=True)


@task
def logs_grpc(c):
    files = ["grpc_error", "grpc_access"]
    paths = " ".join(f"app/logs/{f}.log" for f in files)
    c.run(f"tail -f {paths}", pty=True)
