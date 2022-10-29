"""
Module for a shared classes/functions across all rules.
"""
from concurrent.futures import ThreadPoolExecutor
from loguru import logger


def show_description(description: str) -> None:
    """
    Show linter rule description in output.

    :param description: Test case short description.
    :return: None
    """

    logger.info("".center(62, "#"))

    description_lines = description.split("\n")
    for line in description_lines:
        logger.info("#{}#", line.center(60, " "))
    logger.info("".center(62, "#"))


# pylint: disable=invalid-name
def do(function, **kwargs) -> list:
    """
    Concurrency request wrapper.

    :param function: function object.
    :param kwargs: iterator to iterate on.
    :return: <list>
    """
    results = []
    kwargs["add_meta"] = (
        False if not kwargs.get("add_meta", False) else kwargs["add_meta"]
    )
    kwargs["workers"] = 20 if not kwargs.get("workers", []) else kwargs["workers"]
    with ThreadPoolExecutor(max_workers=kwargs["workers"]) as executor:
        futures = [
            executor.submit(function, i, kwargs["add_meta"]) for i in kwargs["iterator"]
        ]
        for future in futures:
            try:
                results.append(future.result(timeout=90))
            # pylint: disable=invalid-name,broad-except
            except Exception as e:
                results.append(None)
                logger.warning(e)
    return results
