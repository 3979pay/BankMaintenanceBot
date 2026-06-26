import os

from banks import BANKS
from config import LOGO_FOLDER


def get_logo(bank):

    base = os.path.dirname(
        os.path.abspath(__file__)
    )

    base = os.path.dirname(base)

    for name, logo in BANKS:

        if name.lower() == bank.lower():

            path = os.path.join(
                base,
                LOGO_FOLDER,
                logo
            )

            if os.path.exists(path):
                return path

    return None