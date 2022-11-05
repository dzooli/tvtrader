def asdict(obj: object) -> dict:
    """Convert the object to a dict.

    Args:
        obj (object): Input object

    Raises:
        AttributeError: When the object is None or it has no __slots__

    Returns:
        dict: Dictionary of the attributes based on the __slots__ excluding __weakref__
    """
    if obj is None:
        raise AttributeError(f"{str(obj)} is not a valid object")
    try:
        attrs = getattr(obj, "__slots__")
    except AttributeError as ex:
        raise ex
    return {attrname: getattr(obj, attrname)
            for attrname in obj.__slots__ if attrname != "__weakref__"}
