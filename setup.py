#!/usr/bin/python3

from distutils.core import setup

setup(
    name="hubclient",
    version="0.2",
    author="Jeremy Davis",
    author_email="jeremy@turnkeylinux.org",
    url="https://github.com/turnkeylinux/hubclient",
    packages=["hubclient_lib"],
    scripts=["hubclient-get-messages", "hubclient-register-finalize",
             "hubclient-status"]
)
