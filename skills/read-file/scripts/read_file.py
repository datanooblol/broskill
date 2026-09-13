import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from errors import InvalidPatternError, NoMatchError, MultipleMatchError, FileTooLargeError, UnreadableFileError

MAX_READ_BYTES = 1_000_000


def get_args():
    parser = argparse.ArgumentParser(
        description="Read and print a single file's content. --path is resolved under the current directory with Path.rglob, so a bare filename or partial path works as long as it matches exactly one file."
    )
    parser.add_argument('--path', type=str, required=True, help="filename or path/pattern to resolve with rglob")
    return parser


def main():
    sys.stdout.reconfigure(encoding='utf-8')
    args = get_args().parse_args()
    pattern = args.path
    root = Path.cwd()

    if not pattern.strip():
        raise InvalidPatternError(pattern, "pattern is empty")
    if Path(pattern).is_absolute():
        raise InvalidPatternError(pattern, "must be relative to the current directory, not an absolute path")

    try:
        matches = [p for p in root.rglob(pattern) if p.is_file()]
    except (NotImplementedError, ValueError) as e:
        raise InvalidPatternError(pattern, str(e)) from e

    if not matches:
        raise NoMatchError(pattern, str(root))
    if len(matches) > 1:
        raise MultipleMatchError(pattern, [str(m) for m in matches])

    target = matches[0]
    size = target.stat().st_size
    if size > MAX_READ_BYTES:
        raise FileTooLargeError(str(target), size, MAX_READ_BYTES)

    try:
        content = target.read_text(encoding='utf-8')
    except UnicodeDecodeError as e:
        raise UnreadableFileError(str(target), "not valid UTF-8 text, likely a binary file") from e
    except PermissionError as e:
        raise UnreadableFileError(str(target), "permission denied") from e
    except OSError as e:
        raise UnreadableFileError(str(target), str(e)) from e

    print(content)


if __name__ == '__main__':
    main()
