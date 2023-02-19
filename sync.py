#!/usr/bin/env python3
import os
import sys
import argparse
from pathlib import Path
from Sync import *
from Sync.dict import dict_
from Sync.file import write_json


def parse_parameters():
    root_folder = Path(__file__).resolve().parent.parent

    parser = argparse.ArgumentParser()
    parser.add_argument("-r",
                        dest="root_folder",
                        metavar="root folder",
                        type=str,
                        default=root_folder.as_posix(),
                        help="default: {0}".format('%(default)s'))
    parser.add_argument("-i",
                        "--init",
                        action="store_true",
                        help="initialize a new config.json")
    parser.add_argument("-p",
                        "--push",
                        action="store_true",
                        help="push to repository")
    return parser


def print_header(string):
    print("\033[01;36m")
    for x in range(0, len(string) + 6):
        print("=", end="")
    print("\n== %s ==" % string)
    for x in range(0, len(string) + 6):
        print("=", end="")
    print("\n\033[0m", end="")


def print_info(tag, msg, *, end: str = "\n"):
    print("\033[01;34m== {0}\033[0m".format(tag), end="")
    print("\033[01;32m -> \033[0m", end="")
    print("\033[01;31m{0}\033[0m".format(msg), end=end)


def input_n(tag, msg):
    print_info(tag, msg, end="")
    return input()


def input_f(tag, msg) -> str:
    while True:
        value = input_n(tag, msg)

        if value == "q":
            sys.exit(0)

        if value != "":
            return value


def input_v(tag, msg, values: list) -> str:
    while True:
        value = input_n(tag, msg)

        if value == "q":
            sys.exit(0)

        if value in values:
            return value

        try:
            index = int(value) - 1
            if index in range(len(values)):
                return values[index]
        except ValueError:
            continue


def input_int(tag, msg) -> int:
    while True:
        value = input_n(tag, msg)

        if value == "q":
            sys.exit(0)

        try:
            value = int(value)
            return value
        except ValueError:
            continue


def input_bool(tag, msg) -> bool:
    value = input_v(tag, msg, ["y", "n"])
    if value == "y":
        return True
    else:
        return False


def init_new_config(root_folder: Path):
    config = dict_(
        repo_name="",
        repo_url="",
        repo_branch="",
        sync_mode="",
        max_num_module="",
        show_log="",
        log_dir=""
    )

    print_header("Initialize a new config.json")

    config.repo_name = input_f("repo_name", "[str]: ")
    config.repo_url = input_f("repo_url", "[str]: ")

    config.sync_mode = input_v("sync_mode", "[git/rsync]: ", ["git", "rsync"])
    if config.sync_mode == "git":
        config.repo_branch = input_f("repo_branch", "[str]: ")

    config.max_num_module = input_int("max_num_module", "[int]: ")

    config.show_log = input_bool("show_log", "[y/n]: ")
    if config.show_log:
        config.log_dir = input_n("log_dir", "[str]: ")

    save = input_bool(f"save to config.json", "[y/n/q]: ")
    if save:
        config_json = root_folder.joinpath("config", "config.json")
        os.makedirs(config_json.parent, exist_ok=True)
        write_json(config.dict, config_json)


def main():
    parser = parse_parameters()
    args = parser.parse_args()

    root_folder = Path(args.root_folder)
    if args.init:
        init_new_config(root_folder)
        sys.exit(0)

    config = Config(root_folder)
    hosts = Hosts(root_folder, log_folder=config.log_dir, show_log=config.show_log)
    repo = Repo(root_folder,
                name=config.repo_name, modules=hosts.modules, repo_url=config.repo_url,
                max_num_module=config.max_num_module,
                log_folder=config.log_dir, show_log=config.show_log)
    repo.pull()
    repo.write_modules_json()
    repo.clear_removed_modules()

    if args.push:
        if config.sync_mode == "git":
            repo.push_git(config.repo_branch)


if __name__ == "__main__":
    main()
