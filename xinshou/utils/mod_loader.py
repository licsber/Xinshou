import importlib
import os


class ModLoader:
    def get_mod_paths(self, mods_path):
        for filename in os.listdir(mods_path):
            if not filename.endswith('.py'):
                continue

            filepath = os.path.join(mods_path, filename)
            mod_path = filepath.replace('/', '.').replace('.py', '')
            yield mod_path

    def load_mods(self, mods_path):
        mods = {}
        mod_paths = self.get_mod_paths(mods_path)
        for mod_path in mod_paths:
            mod = importlib.import_module(mod_path)
            for i in dir(mod):
                if not i.endswith('Processor'):
                    continue

                processor = getattr(mod, i)()
                keyword = processor.get_keyword()
                mods[keyword] = processor

        return mods
