import argparse
import json
import requests


def cmd_args() -> list[str]:
    parser = argparse.ArgumentParser(description="Looks up shifts command")
    unknownargs = parser.parse_known_args()[1]
    return unknownargs


def make_request(data: list):
    try:
        email = data[0]
        time_start = int(data[1])
        time_end = int(data[2])

        data = json.dumps({"email": email, "start": time_start, "end": time_end})

        response = requests.post(
            "http://localhost:4000/api/timeshits/",
            data=data,
            headers={"Content-Type": "application/json"},
        )
        return response.text
    except Exception as e:
        return getattr(e, "message", str(e))


def make_report(email):
    try:
        url = f"http://localhost:4000/api/timeshits/monthly/{email}"
        response = requests.get(url)
        return response.text
    except Exception as e:
        return getattr(e, "message", str(e))


def main():

    command: list = cmd_args()
    if command[0] != "shifts":
        return f"wrong command {command[0]}"

    if command[1] == "add":
        return make_request(command[2:])
    elif command[1] == "report":
        return make_report(command[-1])


if __name__ == "__main__":
    print(main())
