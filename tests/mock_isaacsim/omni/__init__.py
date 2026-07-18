class UsdContext:
    def get_stage(self):
        return Stage()

class Stage:
    def GetPrimAtPath(self, path):
        return Prim()

class Prim:
    pass

def usd_context():
    return UsdContext()

class Usd:
    @staticmethod
    def get_context():
        return usd_context()

usd = Usd()
