try:
    from louie import dispatcher  # pyright: ignore[reportMissingImports]
    from louie import robustapply  # pyright: ignore[reportMissingImports]
    from louie import saferef  # pyright: ignore[reportMissingImports]

    louie = 1
except ImportError:
    from pydispatch import dispatcher  # pyright: ignore[reportMissingImports]
    from pydispatch import robustapply  # pyright: ignore[reportMissingImports]
    from pydispatch import saferef  # pyright: ignore[reportMissingImports]

    saferef.safe_ref = saferef.safeRef
    robustapply.robust_apply = robustapply.robustApply
    louie = 0

import sys

if not hasattr(robustapply, "_robust_apply"):
    # patch robustapply.robust_apply to display exceptions, but to ignore them
    # this makes 'dispatcher.send' to continue on exceptions, which is
    # the behaviour we want ; it's not because a receiver doesn't handle a
    # signal properly that the whole chain should stop
    robustapply._robust_apply = robustapply.robust_apply

    def __my_robust_apply(*args, **kwargs):
        try:
            return robustapply._robust_apply(*args, **kwargs)
        except Exception:
            sys.excepthook(*sys.exc_info())

    if louie:
        robustapply.robust_apply = __my_robust_apply
    else:
        robustapply.robustApply = __my_robust_apply
    del louie
    del __my_robust_apply
