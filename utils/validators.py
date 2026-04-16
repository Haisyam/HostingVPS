import re

DOMAIN_RE = re.compile(
    r"^(?=.{1,253}$)(?!-)(?:[a-zA-Z0-9-]{1,63}\.)+[A-Za-z]{2,63}$"
)


def is_valid_domain(domain: str) -> bool:
    return bool(DOMAIN_RE.match(domain.strip()))


def yes_no(value: str) -> bool:
    return value.strip().lower() in {"y", "yes", "1", "true"}
