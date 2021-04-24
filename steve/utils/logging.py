from logging import getLogger


def log_return_value(level, template="{}"):
    def inner(func):
        def wrapper(*args, **kwargs):
            return_value = func(*args, **kwargs)

            try:
                logger = getLogger(__name__)
                logger_method = getattr(logger, level)
                formatted_message = template.format(return_value)
                logger_method(formatted_message)

            except Exception as e:
                logger.warning(
                    f"Unable to log return value of function '{func}'"
                    f" with level '{level}': {e}"
                )

            return return_value

        return wrapper

    return inner
