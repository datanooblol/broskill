import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from errors import InvalidPatternError, NoMatchError


def get_args():
    parser = argparse.ArgumentParser(
        description="List files matching a glob pattern under the current directory, using Path.rglob (e.g. '*.md', 'skills/**/*.py')."
    )
    parser.add_argument('--path', type=str, required=True, help="glob pattern for Path.rglob, e.g. '*.md'")
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
        files = [p for p in root.rglob(pattern) if p.is_file()]
    except (NotImplementedError, ValueError) as e:
        raise InvalidPatternError(pattern, str(e)) from e

    if not files:
        raise NoMatchError(pattern, str(root))

    for f in files:
        print(f)


if __name__ == '__main__':
    main()
