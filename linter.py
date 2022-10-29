#!/usr/bin/env python3
"""
@Date: 10.2022
@License: Apache License 2.0

###
Description
###
linter.py - is a Python script that uses a PluginBase approach to execute custom rules as individual plugins.
"""
import sys
import os
import argparse
from pprint import pformat

from loguru import logger

from libs.defaults import DEFAULTS
from libs import rules_loader, config_loader


def main():
    """
    The main entrypoint.

    :return: None
    """
    parser = argparse.ArgumentParser(description="")
    parser.add_argument(
        "-p",
        "--repo-path",
        type=str,
        default=os.environ.get("LINT_TARGET_REPO_PATH"),
        help="Path to the repo which to be checked",
    )
    parser.add_argument(
        "-g",
        "--groups",
        type=str,
        default=os.environ.get("LINT_ENABLED_GROUPS", ""),
        help="Active rule groups for a run",
    )
    parser.add_argument(
        "-e",
        "--excluded-rules",
        type=str,
        default=os.environ.get("LINT_EXCLUDED_RULES", ""),
        help="Excludes rules from a run",
    )
    parser.add_argument(
        "--verbose",
        default="INFO",
        action="store_const",
        const="DEBUG",
        help="Debug verbose output",
    )
    args = parser.parse_args()

    logger.configure(handlers=[DEFAULTS.get("LOGURU_CONFIG")[args.verbose]])
    logger.debug(f"Provided arguments: \n {pformat(args.__dict__)}")
    logger.debug(f"Loaded defaults: \n {pformat(DEFAULTS)}")

    if not args.repo_path:
        logger.error(
            "Path to the target repo is empty. "
            "Use -p/--repo-path argument or LINT_TARGET_REPO_PATH env variable."
        )
        sys.exit(1)

    groups_config = config_loader.load(args=args)
    rules_objs = rules_loader.load(args=args)

    enabled_groups = [
        group
        for group in groups_config["groups"]
        if group["name"] in groups_config["enabled_groups"]
    ]
    logger.info(f"Linter groups will be used in run: {enabled_groups}")

    enabled_rules = []
    for group in enabled_groups:
        for rule in group["rules"]:
            rule_name = f"{group['name']}_{rule}"
            if rule_name not in groups_config["excluded_rules"]:
                enabled_rules.append(rule_name)
    logger.info(f"Linter rules will be applied in run: {enabled_rules}")

    run_passed = True
    for rule in enabled_rules:
        try:
            group_options = groups_config["options"].get(rule.split("_")[0], {})
            passed = rules_objs[rule].run(
                repo_path=args.repo_path, options=group_options
            )
            if passed == "FAIL":
                run_passed = False
        except KeyError:
            logger.error(f"Looks like rule {rule} is missed in rules folder.")

    if run_passed:
        sys.exit(0)
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()
