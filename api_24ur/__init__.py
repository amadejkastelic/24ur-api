def monkey_path_m3u8downloader_configlogger():
    import sys
    import types
    from importlib import abc as importlib_abc
    from importlib import machinery as importlib_machinery

    class DummyModule(types.ModuleType):
        def __getattr__(self, name):
            raise AttributeError(f"Module '{self.__name__}' has no attribute '{name}'")

    class BlockingLoader(importlib_abc.Loader):
        def load_module(self, name):
            module = DummyModule(name)
            sys.modules[name] = module
            return module

    class BlockingFinder(importlib_abc.MetaPathFinder):
        def find_spec(self, fullname, path, target=None):
            if fullname == 'm3u8downloader.configlogger':
                print(f"Blocking import of: {fullname}")
                return importlib_machinery.ModuleSpec(fullname, BlockingLoader())
            return None

    # Insert the custom finder into sys.meta_path
    sys.meta_path.insert(0, BlockingFinder())


monkey_path_m3u8downloader_configlogger()
