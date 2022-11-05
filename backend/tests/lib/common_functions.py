def asdict(obj: object) -> dict:
    if obj is None:
        return None
    return {attrname: getattr(obj, attrname)
            for attrname in obj.__slots__ if attrname is not "__weakref__"}
