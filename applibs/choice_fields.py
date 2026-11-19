from django.db import models

class StatusType(models.TextChoices):
    ACTIVE = "active", "Active"
    INACTIVE = "inactive", "Inactive"
    SUSPENDED = "suspended", "Suspended"
    CLOSED = "closed", "Closed"

class WalletRoleType(models.TextChoices):
    CUSTOMER = "customer", "Customer"
    AGENT = "agent", "Agent"
    MERCHANT = "merchant", "Merchant"

class UserType(models.TextChoices):
    CUSTOMER = "customer", "Customer"
    AGENT = "agent", "Agent"
    MERCHANT = "merchant", "Merchant"

class WalletType(models.TextChoices):
    CUSTOMER = "customer", "Customer"
    AGENT_FLOAT = "agent_float", "Agent Float"
    MERCHANT = "merchant", "Merchant"

class CurrencyType(models.TextChoices):
    BDT = "BDT", "BDT"
    USD = "USD", "USD"