
class DuplicateUserWalletException(Exception):
    """Raised when a user already exists for the given mobile number."""
    pass


class DuplicateWalletException(Exception):
    """Raised when a wallet already exists for the given wallet user."""
    pass