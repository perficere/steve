class Singleton(type):
    def __call__(cls, *args, **kwargs):
        cls._instance = (
            cls._instance
            if hasattr(cls, "_instance")
            else super().__call__(*args, **kwargs)
        )

        return cls._instance
