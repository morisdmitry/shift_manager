import json


def response_bad(error, status: int) -> tuple:
    return (
        json.dumps({"error": getattr(error, "message", str(error))}),
        status,
        {"Content-Type": "application/json"},
    )


def response_ok(response: dict, status: int) -> tuple:
    return (
        json.dumps(response),
        status,
        {"Content-Type": "application/json"},
    )


def response_error(message: str, status: int) -> tuple:
    return (
        json.dumps({"error": message}),
        status,
        {"Content-Type": "application/json"},
    )
