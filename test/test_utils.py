import utils

import numpy as np
import openproblems
import packaging.version

utils.warnings.ignore_warnings()


def test_temporary_version_missing():
    """Test temporary decorator behavior with missing version."""

    @openproblems.utils.temporary
    def test_fn():
        pass

    np.testing.assert_raises_regex(
        TypeError, "temporary() missing 1 required keyword argument: 'version'", test_fn
    )


def test_temporary_version_future():
    """Test temporary decorator behavior with version from the future."""
    version = packaging.version.parse(openproblems.__version__)
    temp_version = "{}.{}".format(version.major, version.minor + 1)

    @openproblems.utils.temporary(version=temp_version)
    def test_fn():
        pass

    np.testing.assert_raises_regex(
        RuntimeError,
        "Temporary function {}.{} is temporary and should not be used "
        "after version {} (current version: {})".format(
            test_fn.__module__, test_fn.__name__, temp_version, openproblems.__version__
        ),
        test_fn,
    )