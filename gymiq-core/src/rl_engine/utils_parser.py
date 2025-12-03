def parse_frequency(freq_str: str) -> int:
    if not isinstance(freq_str, str):
        return 0
    for token in freq_str.split():
        if token.isdigit():
            return int(token)
    return 0
