#!/usr/bin/env python

import sys
import argparse

from jinja2 import Environment, FileSystemLoader

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--template_directory", help="Directory for templates")
    return parser.parse_args()

def main():

    args = parse_args()
    env = Environment(
        loader=FileSystemLoader(args.template_directory),
    )
    pkg_vars = {
        "cgran_package_maintainer": "Andrej Rode <arode@gnuradio.org>",
        "package_name": "gr-foo",
        "package_full_name": "My GNU Radio Foo module",
        "package_homepage": "https://foo.bar",
        "package_description": "Foo Foo Foo",
        "package_major_version": "3",
        "package_minor_version": "0",
        "package_patch_version": "0",
        "package_dependencies": ["foo", "baz", "bar"]
    }
    template = env.get_template('control.j2')
    print(template.render(**pkg_vars
    ))
    return True


if __name__ == "__main__":
    sys.exit(not main())
