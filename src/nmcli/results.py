
from .constants import NMCLI_FIELDS



class Result(object):
    data = None
    def __init__(self, data: list or dict, ret_code: int, stdout: str, stderr: str):
        self.return_code = ret_code
        self.stdout = stdout
        self.stderr = stderr

        if isinstance(data, list):
            pass

        elif isinstance(data, dict):
            pass

    def ToDict(self):
        return {
                'return_code': self.return_code,
                'stdout': self.stdout,
                'stderr': self.stderr,
                'data': self.data
                }

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} : {self.ToDict()}>"
    def __str__(self) -> str:
        return f"<{self.__class__.__name__} : {self.ToDict()}>"

    def __contains__(self, *args):
        print(args)

    def __getitem__(self, *args):
        print(args)