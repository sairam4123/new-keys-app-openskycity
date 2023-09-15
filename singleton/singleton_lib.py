
class SingletonMeta(type):
    _instances: dict = {}

    def __call__(cls, *args, **kwds):
        if not cls._instances.get(cls):
            cls._instances[cls] = super().__call__(*args, **kwds)
        return cls._instances[cls]

def singleton(class_=None):
    def wrapper(class__):
        cls = SingletonMeta(
            class__.__name__,
            class__.__bases__,
            dict(class__.__dict__),
        )
        cls.__metaclass__ = SingletonMeta # type: ignore
        cls.__wrapped__ = class_ # type: ignore
        return cls
    
    # allows us to use ()
    if class_ is None:
        return wrapper
    
    return wrapper(class_)

