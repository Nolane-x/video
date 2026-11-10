"""Strict allow/deny policy for imported human-crew meshes."""

def is_unwanted_crew_mesh(object_name, data_name, material_names, dimensions):
    """Return True for accidental import helpers, not approved character parts."""
    names = f"{object_name or ''} {data_name or ''}".casefold()
    if "icosphere" in names:
        return True
    if not material_names and dimensions:
        try:
            extent = max(abs(float(value)) for value in dimensions)
        except (TypeError, ValueError):
            return True
        if extent >= 1.5:
            return True
    return False
