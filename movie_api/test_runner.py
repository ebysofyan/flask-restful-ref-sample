import sys

if len(sys.argv) > 1 and sys.argv[1] == "--pytest":
    # flake8: noqa
    import pytest

    sys.exit(pytest.main(sys.argv[2:]))
