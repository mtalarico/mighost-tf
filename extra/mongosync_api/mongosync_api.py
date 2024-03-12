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
        for i, host in enumerate(self.hosts):
            payload = {"source": "cluster0", "destination": "cluster1"}
            if self.support_older_versions:
                payload["supportOlderVersions"] = True
            url = f"http://{host}:{self.port}/api/v1/start"
            print(f"Sending /start to host {i} ({host}:{self.port})")
            if self.verbose:
                print(f"POST to {url} with payload {json.dumps(payload)}")
            # resp = http.request(method="POST", url=url, fields=payload)
            # print(resp.data)

    def progress(self):
        for i, host in enumerate(self.hosts):
            headers = {"Content-Type": "application/json"}
            url = f"http://{host}:{self.port}/api/v1/progress"
            print(f"Sending /progress to host {i} ({host}:{self.port})")
            if self.verbose:
                print(f"GET to {url} with headers {json.dumps(headers)}")
            # resp = http.request(method="GET", url=url, headers=headers)
            # print(resp.data)

    def commit(self):
        self._post_empty("commit")

    def pause(self):
        self._post_empty("pause")

    def resume(self):
        self._post_empty("resume")

    def reverse(self):
        self._post_empty("reverse")

    def _post_empty(self, endpoint):
        for i, host in enumerate(self.hosts):
            payload = {}
            url = f"http://{host}:{self.port}/api/v1/{endpoint}"
            print(f"Sending /{endpoint} to host {i} ({host}:{self.port})")
            if self.verbose:
                print(f"POST to {url} with payload {json.dumps(payload)}")
            # resp = http.request(method="POST", url=url, fields=payload)
            # print(resp.data)


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
