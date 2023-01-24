def evaluate_criteria(criteria: str, **context: int) -> bool:
    if not criteria:
        return False

    for key, value in context.items():
        criteria = criteria.replace(key, str(value))

    if "and" in criteria:
        return all(
            evaluate_criteria(c)
            for c in criteria.split("and")
        )

    if "or" in criteria:
        return any(
            evaluate_criteria(c)
            for c in criteria.split("or")
        )

    criteria = criteria.replace(" ", "")

    if ">" in criteria:
        left, right = criteria.split(">")
        return int(left) > int(right)
    if "<" in criteria:
        left, right = criteria.split("<")
        return int(left) < int(right)
    if "=" in criteria:
        left, right = criteria.split("=")
        return int(left) == int(right)

    return bool(int(criteria))
