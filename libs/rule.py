"""
Parent rule class.
"""
from loguru import logger
from libs.common import show_description


class Rule:
    """
    Parent rule class.
    """
    def __init__(self, name):
        self.passed = "PASS"
        self.logger = logger
        self.name = name
        self.description = "Example description that describes a case."

    def run(self, repo_path: str, options: dict) -> str:
        """
        Wrapper function to execute specific rule logic.

        :param repo_path: target_repo abs path.
        :param options: loaded config.yaml
        :return: <str>
        """
        logger.info("RUN: {}", self.name)
        show_description(description=self.description)

        self._execute(repo_path=repo_path, options=options)

        if self.passed == "PASS":
            logger.info("PASS: {}\n", self.name)
        elif self.passed == "WARN":
            logger.warning("PASS: {}\n", self.name)
        elif self.passed == "FAIL":
            logger.error("FAIL: {} failed\n", self.name)

        return self.passed

    # pylint: disable=unnecessary-pass
    def _execute(self, repo_path: str, options: dict):
        """
        The main rule method, entrypoint for all logic inside a module.

        :param repo_path: target repo name.
        :param options: options from a common config.yaml
        :return: None
        """
        pass
