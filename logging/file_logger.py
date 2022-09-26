import json
import sys
from functools import wraps


def file_logger(function=None, filename="default.json"):
    """
    Logs output of a function to a named file.
    :param function:
    :return:
    """

    def _log_json(function):
        @wraps(function)
        def json_logger(*args, **kwargs):
            """
            Logs result to file as json
            :param filename:
            :return:
            """
            try:
                result = function(*args, **kwargs)
            except:
                print(f"Unable to log output, function crashed.\nException: {sys.exc_info()[0]}")
                return
            if result:
                try:
                    with open(filename, "w") as f:
                        json.dump(result, f)
                except:
                    print(
                        f"Unable to log output, output was not JSON.\nOutput: {result}\nException: {sys.exc_info()[0]}"
                    )
            else:
                print("Function returned None, result not logged")

        return json_logger

    # TODO switch on file extension to choose logging method to return (currently assumes json)
    if function:
        return _log_json(function)
    return _log_json
