from setuptools import setup

setup(
    name="mongosync_api",
    version="0.1.0",
    py_modules=["mongosync_api"],
    install_requires=["Click", "urllib3"],
    entry_points={
        "console_scripts": [
            "mongosync_api = mongosync_api:cli",
        ],
    },
)
