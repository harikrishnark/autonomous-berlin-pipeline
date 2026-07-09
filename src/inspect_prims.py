import isaacsim.core.api
attrs = [x for x in dir(isaacsim.core.api) if 'prim' in x.lower() or 'xform' in x.lower()]
print("isaacsim.core.api attrs:", attrs)

# Also try isaacsim.core.prims
try:
    import isaacsim.core.prims
    print("isaacsim.core.prims:", dir(isaacsim.core.prims))
except Exception as e:
    print("isaacsim.core.prims error:", e)

# Try pxr
try:
    from pxr import UsdGeom, Gf
    print("pxr available")
except Exception as e:
    print("pxr error:", e)
