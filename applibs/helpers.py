from ulid import ULID

def generate_new_ulid() -> str:
    """
    Generates a lexicographically sortable ULID string.
    """
    return str(ULID())

def clean_mobile_no(mobile_no: str) -> str:
    mobile_no = mobile_no.strip()

    if str(mobile_no).startswith("+88"):
        mobile_no = mobile_no[3:]
    elif str(mobile_no).startswith("88"):
        mobile_no = mobile_no[2:]

    mobile_no = str(mobile_no).replace("-", "")
    return mobile_no