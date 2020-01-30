#!/usr/bin/env python

import sys
import argparse

from jinja2 import Environment, FileSystemLoader
import os
import yaml
import datetime
import git


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--template_directory", help="Directory for templates")
    parser.add_argument(
        "-n", "--oot_name", help="GNU Radio OOT name to generate source package for"
    )
    parser.add_argument(
        "-w", "--work_directory", help="Directory to actually carry out the work"
    )
    parser.add_argument("-v", "--gr_version", help="GNU Radio version", default="3.8")
    return parser.parse_args()


def main():

    args = parse_args()

    # Load package variables from yml
    with open(
        os.path.join(
            os.path.abspath(os.path.dirname(__file__)),
            "recipes",
            f"{args.oot_name}.yml",
        ),
        "r",
    ) as of:
        pkg_vars = yaml.safe_load(of)

    pkg_vars["cgran_package_date"] = (
        datetime.datetime.now(datetime.timezone.utc)
        .astimezone()
        .strftime("%a, %d %b %Y %T %z")
    )
    pkg_vars["cgran_package_maintainer"] = "Andrej Rode <arode@gnuradio.org>"
    pkg_vars["cgran_debian_distribution"] = "eoan"
    print(pkg_vars)
    # Clone repository for GNU Radio version specified
    cloned_repo = git.Repo.clone_from(
        pkg_vars["package_src"],
        os.path.join(os.path.abspath(args.work_directory), args.oot_name),
        branch=pkg_vars["supported_versions"][args.gr_version],
    )
    pkg_vars["package_git_log"] = r"".join(
        list(c.message for c in cloned_repo.iter_commits(max_count=5))
    )
    pkg_vars["package_major_version"] = 0
    pkg_vars["package_minor_version"] = 0
    pkg_vars["package_patch_version"] = 0
    pkg_vars["package_git_hash"] = cloned_repo.head.object.hexsha[:7]
    pkg_vars["package_num_commits"] = len(list(cloned_repo.iter_commits()))
    print(pkg_vars)
    # Generate entries in the debian/ directory from config and repository information
    env = Environment(loader=FileSystemLoader(args.template_directory),)
    debian_path = os.path.join(args.work_directory, args.oot_name, "debian")
    os.makedirs(debian_path, exist_ok=True)
    for template_name, target_file in (
        ("control.j2", "control"),
        ("rules.j2", "rules"),
        ("copyright.j2", "copyright"),
        ("changelog.j2", "changelog"),
        (
            "libmodule_install.j2",
            f"libgnuradio-{args.oot_name.replace('gr-','')}.install",
        ),
        ("module_install.j2", f"{args.oot_name}.install"),
    ):
        template = env.get_template(template_name)
        output = template.render(**pkg_vars)
        with open(os.path.join(debian_path, target_file), "w") as of:
            of.write(output)

    template = env.get_template("libmodule_install.j2")
    output = template.render(**pkg_vars)

    return True


if __name__ == "__main__":
    sys.exit(not main())
