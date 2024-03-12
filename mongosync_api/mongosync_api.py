import json
import urllib3
import click

http = urllib3.PoolManager()


class MongosyncAPI:
    def __init__(self, file_path, port, support_older_versions, verbose):
        try:
            with open(file_path) as f:
                ips = json.load(f)
            self.hosts = ips["ec2_ips"]["value"]
            self.port = port
            self.support_older_versions = support_older_versions
            self.verbose = verbose
        except IOError as e:
            print(f"Issue opening file: {file_path}\n{e}")
            exit(1)

    def start(self):
        payload = {"source": "cluster0", "destination": "cluster1"}
        if self.support_older_versions:
            payload["supportOlderVersions"] = True
        self._post("start", payload)

    def progress(self):
        headers = {"Content-Type": "application/json"}
        self._get("progress", headers)

    def commit(self):
        self._post("commit", {})

    def pause(self):
        self._post("pause", {})

    def resume(self):
        self._post("resume", {})

    def reverse(self):
        self._post("reverse", {})

    def _post(self, endpoint, payload):
        for i, host in enumerate(self.hosts):
            url = f"http://{host}:{self.port}/api/v1/{endpoint}"
            print(f"Sending /{endpoint} to host {i} ({host}:{self.port})")
            if self.verbose:
                print(f"POST to {url} with payload {json.dumps(payload)}")
            resp = http.request(method="POST", url=url, fields=payload)
            print(resp.data.decode("utf-8"))
            print()

    def _get(self, endpoint, headers):
        for i, host in enumerate(self.hosts):
            url = f"http://{host}:{self.port}/api/v1/{endpoint}"
            print(f"Sending /{endpoint} to host {i} ({host}:{self.port})")
            if self.verbose:
                print(f"GET to {url} with headers {json.dumps(headers)}")
            resp = http.request(method="GET", url=url, headers=headers)
            print(resp.data.decode("utf-8"))
            print()


@click.group()
@click.option(
    "--path",
    default="./ips.json",
    help="Path to .json file containing `terraform output -json` output ",
)
@click.option("--port", default=27182, help="Port that mongosyncs are running on")
@click.option(
    "--supportOlderVersions",
    default=False,
    help="Include older version support",
    is_flag=True,
)
@click.option(
    "--verbose", default=False, help="Print HTTP commands and responses", is_flag=True
)
@click.pass_context
def cli(ctx, path, port, supportolderversions, verbose):
    ctx.ensure_object(dict)
    ctx.obj["api"] = MongosyncAPI(path, port, supportolderversions, verbose)


@cli.command()
@click.pass_context
def start(ctx):
    ctx.obj["api"].start()


@cli.command()
@click.pass_context
def progress(ctx):
    ctx.obj["api"].progress()


@cli.command()
@click.pass_context
def commit(ctx):
    ctx.obj["api"].commit()


@cli.command()
@click.pass_context
def pause(ctx):
    ctx.obj["api"].pause()


@cli.command()
@click.pass_context
def resume(ctx):
    ctx.obj["api"].resume()


@cli.command()
@click.pass_context
def reverse(ctx):
    ctx.obj["api"].reverse()


if __name__ == "__main__":
    cli(obj={})
