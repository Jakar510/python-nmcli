import re

anti_spacer = re.compile(r'(\s+)')


def row_parser(stdout: str, headers: list or tuple) -> dict:
    l = []
    for row in stdout.strip().split('\n'):
        if any(header in row for header in headers): continue
        l.append(row.split())
    d = { }
    for row in l:
        key, value = row
        d[key] = value
    return d



def single_parser(stdout: str) -> dict:
    return dict(hostname=stdout.strip())


def header_single_row_parser(stdout: str) -> dict:
    l = []
    for row in stdout.strip().split('\n'):
        l.append(row.split())
    return dict(zip(l[0], l[1]))