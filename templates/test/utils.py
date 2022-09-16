import datetime


def _to_timestamp(v) -> float:
    if isinstance(v, str):
        return datetime.datetime.fromisoformat(v).timestamp()
    elif isinstance(v, (int, float)):
        return float(v)
    else:
        raise TypeError(f'Invalid time type - {v!r}.')


def trepr(v) -> str:
    _local_timezone = datetime.datetime.now(datetime.timezone.utc).astimezone().tzinfo
    return datetime.datetime.fromtimestamp(_to_timestamp(v), _local_timezone).isoformat()


def wtf(a, b) -> str:
    return f'wtf: {a} + {b} = {a + b}'
