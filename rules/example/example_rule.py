"""
Rule example.
"""
# pylint: disable=import-error
from argparse import Namespace
from libs import rule


class Example(rule.Rule):
    """
    A child rule class.
    """

    def __init__(self, name):
        super().__init__(name)

        self.description = "This is an example test case."

    def _execute(self, repo_path: str, options: dict):
        self.logger.info("Starting an example test case")
        self.logger.info(f"My target: {repo_path}")
        self.logger.info(f"My options: {options}")


# pylint: disable=unused-argument
def setup(plugin, name: str, args: Namespace):
    """
    Mandatory function, rule class has to be equal to rule class name within this module.
    Initialize a rule.

    :param args: script arguments.
    :param plugin: RulesLoader object.
    :param name: rule name.
    """
    plugin.register_rule(name=name, rule_class=Example(name))
