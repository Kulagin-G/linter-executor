"""
Config loader module.
"""
from argparse import Namespace
import os
import yaml

PWD = os.path.abspath((os.path.dirname(__file__)))


def load(args: Namespace) -> dict:
    """
    Loading config file and generating active groups map.

    :param: args: script arguments.
    :return: <dict>
    """
    with open(PWD + "/../config/config.yaml", "r", encoding="utf-8") as f_conf:
        config = yaml.safe_load(f_conf)

    if overwrite_active_groups := args.groups:
        config["enabled_groups"] = overwrite_active_groups.split(",")

    if config["enabled_groups"][0].lower() == "all":
        all_groups = []
        # pylint: disable=expression-not-assigned
        [all_groups.append(group["name"]) for group in config["groups"]]
        config["enabled_groups"] = all_groups

    if excluded_rules := args.excluded_rules:
        config["excluded_rules"] = excluded_rules.split(",")

    return config
