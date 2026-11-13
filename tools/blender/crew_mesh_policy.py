"""Strict allow/deny policy for imported human-crew meshes.

The siege renderer duplicates every accepted mesh once per performer. An
unmaterialed helper primitive can therefore become a very large visible prop
six times over, so reject known Icosphere leftovers and unmaterialed oversized
meshes before duplication.
"""

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
