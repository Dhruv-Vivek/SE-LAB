import re

# ASCII-only signed integer (rejects "1_0", " 5", Unicode digits, "", etc.)
_INT_RE = re.compile(r"[+-]?[0-9]+")


def _to_int(token):
    """Convert a token to int, or return None if it is not a clean integer."""
    if not isinstance(token, str):
        return None
    token = token.strip()
    if not _INT_RE.fullmatch(token):
        return None
    try:
        return int(token)
    except ValueError:  # e.g. absurdly long digit strings
        return None


def parse_request(text):
    """Parse 'FROM->TO' into (from_floor, to_floor). Returns None if invalid."""
    if not isinstance(text, str):
        return None
    parts = text.split('->')
    if len(parts) != 2:
        return None
    start, end = _to_int(parts[0]), _to_int(parts[1])
    if start is None or end is None:
        return None
    return start, end


def total_travel(floors_csv):
    """Total floors travelled for a CSV of stops. Returns None if invalid."""
    if not isinstance(floors_csv, str):
        return None
    floors = [_to_int(f) for f in floors_csv.split(',')]
    if any(f is None for f in floors):  # also catches '' and '1,,3'
        return None
    return sum(abs(floors[i + 1] - floors[i]) for i in range(len(floors) - 1))


def load_percent(text):
    """Parse 'X of Y' and return load as a whole percent. Returns None if invalid."""
    if not isinstance(text, str):
        return None
    parts = text.split(' of ')
    if len(parts) != 2:
        return None
    load, capacity = _to_int(parts[0]), _to_int(parts[1])
    if load is None or capacity is None:
        return None
    if load < 0 or capacity <= 0:  # no negative load, no divide-by-zero
        return None
    return load * 100 // capacity


def main():
    print("==== Running parse_request ====")
    user_input = input("Enter a request as FROM->TO (e.g. 5->9): ")
    result = parse_request(user_input)
    print("From and To:", result if result is not None else "Invalid input")

    print("\n==== Running total_travel ====")
    user_input = input("Enter floors visited as CSV (e.g. 1,5,3,9): ")
    result = total_travel(user_input)
    print("Floors Travelled:", result if result is not None else "Invalid input")

    print("\n==== Running load_percent ====")
    user_input = input("Enter load as 'X of Y' (e.g. 450 of 630): ")
    result = load_percent(user_input)
    print("Load Percent:", result if result is not None else "Invalid input")


if __name__ == "__main__":
    main()
