#ユーティリティクラスや仮数をまとめるモジュールです
class DotDict(dict):
    """辞書をドットアクセスできるようにするラッパー"""
    def __getattr__(self, item):
        try:
            value = self[item]
        except KeyError:
            raise AttributeError(f"No such attribute: {item}")

        if isinstance(value, dict):
            return DotDict(value)
        if isinstance(value, list):
            return [DotDict(v) if isinstance(v, dict) else v for v in value]
        return value

    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__

    def get(self, item, default=None):
        value = dict.get(self, item, default)
        if isinstance(value, dict):
            return DotDict(value)
        if isinstance(value, list):
            return [DotDict(v) if isinstance(v, dict) else v for v in value]
        return value
