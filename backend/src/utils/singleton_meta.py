class SingletonMeta(type):
    """Minimal singleton metaclass.

    - `__call__` creates the single instance on first construction and returns it afterwards.
    - `get_instance(*args, **kwargs)` returns the instance, creating it if necessary.
    - `clear()` resets the stored instance to None.
    """

    def __call__(cls, *args, **kwargs):
        if not getattr(cls, "_instance", None):
            cls._instance = super().__call__(*args, **kwargs)
        return cls._instance

    def get_instance(cls, *args, **kwargs):
        """Return the existing instance or create it with the provided args if missing."""
        if not getattr(cls, "_instance", None):
            cls._instance = super(SingletonMeta, cls).__call__(*args, **kwargs)
        return cls._instance

    def clear(cls):
        """Reset the stored instance so a new one will be created on next call."""
        cls._instance = None
