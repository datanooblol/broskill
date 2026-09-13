class ReadFileSkillError(Exception):
    """Base error for skills/read-file's scripts."""


class InvalidPatternError(ReadFileSkillError):
    """The --path pattern itself is unusable (empty, absolute, escapes the project root)."""

    def __init__(self, pattern: str, reason: str):
        self.pattern = pattern
        self.reason = reason
        super().__init__(f"Invalid pattern '{pattern}': {reason}")


class NoMatchError(ReadFileSkillError):
    """The pattern matched zero files."""

    def __init__(self, pattern: str, root: str):
        self.pattern = pattern
        self.root = root
        super().__init__(f"No file matched '{pattern}' under {root}")


class MultipleMatchError(ReadFileSkillError):
    """The pattern matched more than one file where exactly one was expected."""

    def __init__(self, pattern: str, matches: list[str]):
        self.pattern = pattern
        self.matches = matches
        listed = "\n".join(matches)
        super().__init__(f"'{pattern}' matched {len(matches)} files, narrow the pattern:\n{listed}")


class FileTooLargeError(ReadFileSkillError):
    """The matched file is too large to read into context safely."""

    def __init__(self, path: str, size: int, limit: int):
        self.path = path
        self.size = size
        self.limit = limit
        super().__init__(f"'{path}' is {size} bytes, exceeds the {limit} byte read limit")


class UnreadableFileError(ReadFileSkillError):
    """The matched file exists but couldn't be read (permissions, binary/non-utf8 content, etc.)."""

    def __init__(self, path: str, reason: str):
        self.path = path
        self.reason = reason
        super().__init__(f"Could not read '{path}': {reason}")
