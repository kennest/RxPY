from rx.core import Observable, ObservableBase


def interval(period) -> ObservableBase:
    """Returns an observable sequence that produces a value after each
    period.

    Example:
    1 - res = rx.Observable.interval(1000)

    Keyword arguments:
    period -- Period for producing the values in the resulting sequence
        (specified as an integer denoting milliseconds).

    Returns an observable sequence that produces a value after each period.
    """

    return Observable.timer(period, period)
