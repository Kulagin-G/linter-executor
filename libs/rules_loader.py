"""
Rules loader module.
"""
import os
from functools import partial
from argparse import Namespace
from pluginbase import PluginBase

PWD = os.path.abspath((os.path.dirname(__file__)))
get_path = partial(os.path.join, PWD)


class RulesLoader:
    """
    A main class to load and register linter rules.
    """

    def __init__(self, args: Namespace):
        self.args = args
        self.registered_rules = {}
        self.load_rules()

    def load_rules(self) -> None:
        """
        Load rules as individual plugins.

        :return: None
        """
        for rules_folder in next(os.walk(get_path("../rules/")))[1]:
            source = PluginBase(package="rules").make_plugin_source(
                searchpath=[get_path(f"../rules/{rules_folder}")], persist=True
            )

            for plugin_name in source.list_plugins():
                plugin = source.load_plugin(plugin_name)
                plugin.setup(self, name=f"{rules_folder}_{plugin_name}", args=self.args)

    def register_rule(self, name: str, rule_class):
        """
        A method a plugin can use to register a rule.

        :param rule_class: initialized plugin class.
        :param name: rule name.
        :return: None
        """
        self.registered_rules[name] = rule_class


def load(args: Namespace):
    """
    Register a rule.

    :return: None
    """
    return RulesLoader(args=args).registered_rules
