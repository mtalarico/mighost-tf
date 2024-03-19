import json
import urllib3
import click

http = urllib3.PoolManager()


class MongosyncAPI:
    def __init__(self, file_path, port, verbose):
        try:
            with open(file_path) as f:
                ips = json.load(f)
            self.hosts = ips["ec2_ips"]["value"]
            self.port = port
            self.verbose = verbose
        except IOError as e:
            print(f"Issue opening file: {file_path}\n{e}")
            exit(1)

    def run_for_each_mig_host(self, func, options):
        for i, host in enumerate(self.hosts):
            func(host, options, i)

    def start(self, host,  options, host_num=0):
        payload = {"source": "cluster0", "destination": "cluster1"}
        if options['support_older_versions']:
            payload["supportOlderVersions"] = True
        if options['no_index']:
            payload["buildIndexes"] = "never"
        resp = self._post("start", host_num, host, payload)
        print(json.loads(resp.data), end="\n\n")

    def progress(self, host,  options, host_num=0):
        headers = {"Content-Type": "application/json"}
        resp = self._get("progress", host_num, host, headers)
        print(json.loads(resp.data), end="\n\n")

    def commit(self, host,  options, host_num=0):
        resp = self._post("commit", host_num, host, {})
        print(json.loads(resp.data), end="\n\n")

    def pause(self, host,  options, host_num=0):
        resp = self._post("pause", host_num, host, {})
        print(json.loads(resp.data), end="\n\n")

    def resume(self, host,  options, host_num=0):
        resp = self._post("resume", host_num, host, {})
        print(json.loads(resp.data), end="\n\n")

    def reverse(self, host,  options, host_num=0):
        resp = self._post("reverse", host_num, host, {})
        print(json.loads(resp.data), end="\n\n")


    def _post(self, endpoint, i, host, payload):
            url = f"http://{host}:{self.port}/api/v1/{endpoint}"
            print(f"Sending /{endpoint} to host {i} ({host}:{self.port})")
            if self.verbose:
                print(f"POST to {url} with payload {json.dumps(payload)}")
            resp = http.request(method="POST", url=url, body=json.dumps(payload))
            return resp

    def _get(self, endpoint, i, host, headers):
            url = f"http://{host}:{self.port}/api/v1/{endpoint}"
            print(f"Sending /{endpoint} to host {i} ({host}:{self.port})")
            if self.verbose:
                print(f"GET to {url} with headers {json.dumps(headers)}")
            resp = http.request(method="GET", url=url, headers=headers)
            return resp


@click.group()
@click.option(
    "--path",
    default="./ips.json",
    help="Path to .json file containing `terraform output -json` output ",
)
@click.option("--port", default=27182, help="Port that mongosyncs are running on")
@click.option(
    "--verbose", default=False, help="Print HTTP commands and responses", is_flag=True
)
@click.pass_context
def cli(ctx, path, port, verbose):
    ctx.ensure_object(dict)
    ctx.obj["api"] = MongosyncAPI(path, port, verbose)


@cli.command()
@click.option("--noindex", default=False, help="Do not build indexes during initial sync", is_flag=True)
@click.option(
    "--supportOlderVersions",
    default=False,
    help="Include older version support",
    is_flag=True,
)
@click.pass_context
def start(ctx, supportolderversions, noindex):
    ctx.obj["api"].run_for_each_mig_host(ctx.obj["api"].start, {"support_older_versions": supportolderversions, "no_index": noindex})


@cli.command()
@click.pass_context
def progress(ctx):
    ctx.obj["api"].run_for_each_mig_host(ctx.obj["api"].progress, {})


@cli.command()
@click.pass_context
def commit(ctx):
    ctx.obj["api"].run_for_each_mig_host(ctx.obj["api"].commit, {})


@cli.command()
@click.pass_context
def pause(ctx):
    ctx.obj["api"].run_for_each_mig_host(ctx.obj["api"].pause, {})


@cli.command()
@click.pass_context
def resume(ctx):
    ctx.obj["api"].run_for_each_mig_host(ctx.obj["api"].resume, {})


@cli.command()
@click.pass_context
def reverse(ctx):
    ctx.obj["api"].run_for_each_mig_host(ctx.obj["api"].reverse, {})


@cli.command()
@click.pass_context
def time(ctx):
    ctx.obj["api"].run_for_each_mig_host(ctx.obj["api"].time_initial_sync, {})


if __name__ == "__main__":
    cli(obj={})
