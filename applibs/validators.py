import re

MOBILE_REGEX = re.compile(r"^(?:\+?88)?01[1-9][0-9]{8}$")

def is_valid_mobile_no(mobile_no: str) -> bool:
    """
        Check mobile number is valid or not.

        @return: Boolean
    """
    if mobile_no:
        if MOBILE_REGEX.match(mobile_no):
            return True
        return False

    return False