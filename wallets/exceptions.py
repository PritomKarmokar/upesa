
class DuplicateUserWalletException(Exception):
    """Raised when a user already exists for the given mobile number."""
    pass

class DuplicateWalletException(Exception):
    """Raised when a wallet already exists for the given wallet user."""
    pass

class InvalidCredentials(Exception):
    """Raised when the provided credentials are invalid."""
    pass

class AccountLocked(Exception):
    """Raised when the account is locked."""
    pass

class AccountNotActive(Exception):
    """Raised when the account is not active."""
    pass