import json
import os

from constants import COMPANY_URL_INITIAL


def get_key(filepath="credentials.json"):
    if os.path.isfile(filepath):
        credentials = json.load(open(filepath, "r"))
        return credentials["username"], credentials["password"]
    else:
        raise Exception(f"{filepath} doesnt exist")


def get_company_name(input_string):
    if COMPANY_URL_INITIAL in input_string:
        name = input_string.rsplit(COMPANY_URL_INITIAL)
        name = name[1].replace("/", "")
        return name
    return input_string
