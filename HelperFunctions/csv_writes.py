# Ansys Libraries
from ansys.stk.core.stkdesktop import STKDesktop
from ansys.stk.core.stkengine import STKEngine
from ansys.stk.core.stkobjects import (
    STKObjectType,
    SensorPattern,
    AccessConstraintType,
    ConstraintLighting,
    DataProviderGroup
)

# Other Libraries
import csv

EXPAND_TO_ELEMENTS = True
MAX_DEPTH = 10

def _label_of(x) -> str:
    """
    Best-effort extraction of a human-readable name from an STK API object.

    Input:
    - STK API object (e.g. Satellite, Facility, Sensor, DataProvider, etc.)

    Output:
    - name: The name of the object, or a string representation of the object if no name is available.
    """
    name = getattr(x, "name", None)
    return str(name) if name else str(x)

def _try_get_group(dp):
    """
    Return a data provider's nested sub-items as a list, or None if it
    isn't a group / has no sub-items. Tries direct attribute access first,
    falling back to an explicit DataProviderGroup cast.

    Input:
    - dp: An STK DataProvider object

    Output:
    - group_list: A list of sub-items (DataProvider objects), or None if no sub-items exist.
    """
    try:
        group = dp.group
        if group is not None:
            group_list = list(group)
            if group_list:
                return group_list
    except Exception:
        pass
 
    try:
        group = DataProviderGroup(dp).group
        group_list = list(group)
        if group_list:
            return group_list
    except Exception:
        pass
 
    return None

def _try_get_elements(dp):
    """
    Return a leaf data provider's output elements (columns), or None.
    
    Input:
    - dp: An STK DataProvider object

    Output:
    - elements_list: A list of output elements (DataProviderElement objects), or None if no elements exist.
    """
    try:
        elements = dp.elements
        if elements is not None:
            elements_list = list(elements)
            if elements_list:
                return elements_list
    except Exception:
        pass
    return None

def resolve_items(dp, prefix="", depth=0, max_depth=MAX_DEPTH, expand_to_elements=EXPAND_TO_ELEMENTS):
    """
    Recursively resolve the 'items' contained within a data provider.
 
    Always recurses fully through nested groups; only the final leaf decides
    whether to expand into its .elements or fall back to its own name, based
    on expand_to_elements. Returns a flat list of string labels.

    Input:
    - dp: An STK DataProvider object
    - prefix: A string prefix to prepend to each label (used for recursion)
    - depth: Current recursion depth (used for recursion)
    - max_depth: The maximum recursion depth allowed
    - expand_to_elements: A boolean indicating whether to expand leaf nodes into their elements
    """
    if depth > max_depth:
        return [f"{prefix} > (max depth reached)" if prefix else "(max depth reached)"]
 
    group_items = _try_get_group(dp)
    if group_items:
        items = []
        for sub in group_items:
            sub_label = _label_of(sub)
            new_prefix = f"{prefix} > {sub_label}" if prefix else sub_label
            items.extend(resolve_items(sub, new_prefix, depth + 1, max_depth, expand_to_elements))
        return items
    
    # Leaf provider (no further grouping) -----------------------------------
    if expand_to_elements:
        elements = _try_get_elements(dp)
        if elements:
            labels = [_label_of(el) for el in elements]
            return [f"{prefix} > {label}" if prefix else label for label in labels]
 
    own_name = _label_of(dp)
    return [f"{prefix} > {own_name}" if prefix else own_name]

def inventory_object(stk_object, label="object"):
    """
    Build {data_provider_name: [item_label, ...]} for every top-level data
    provider on an STK object. Never raises -- errors are logged inline so
    one bad provider doesn't stop the whole inventory.
    
    Input:
    - stk_object: An STK object (e.g., Satellite, Facility, Sensor)
    - label: A string label for the object (used for logging)

    Output:
    - inventory: A dictionary mapping data provider names to lists of item labels.
    """
    inventory = {}
    try:
        providers = list(stk_object.data_providers)
    except Exception as e:
        print(f"{label}: could not read data_providers ({type(e).__name__}: {e})")
        return inventory
 
    total = len(providers)
    print(f"{label}: {total} top-level data providers found")
    for i, dp in enumerate(providers, start=1):
        name = _label_of(dp)
        print(f"  [{i}/{total}] {name}")
        try:
            items = resolve_items(dp)
        except Exception as e:
            items = [f"<error: {type(e).__name__}: {e}>"]
        inventory[name] = items
    return inventory
 
 
def write_provider_item_csv(inventory, filepath):
    """
    Write one CSV: columns = data provider names, rows = items within
    each provider (ragged, blank-padded to the tallest column).
    
    Input:
    - inventory: A dictionary mapping data provider names to lists of item labels.
    - filepath: The path to the output CSV file.
    """
    provider_names = list(inventory.keys())
    items_by_column = [inventory[name] for name in provider_names]
    max_rows = max((len(items) for items in items_by_column), default=0)
 
    with open(filepath, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.writer(f)
        writer.writerow(provider_names)
        for row_idx in range(max_rows):
            row = [items[row_idx] if row_idx < len(items) else "" for items in items_by_column]
            writer.writerow(row)
    print(f"Wrote {filepath}  ({len(provider_names)} providers, {max_rows} rows)")
 
 
def write_object_summary_csv(object_inventories, filepath):
    """
    Write one CSV: rows = data provider names (union across all objects),
    columns = object labels, cells = item count for that provider/object
    (blank if the object doesn't expose that provider).
    
    Input:
    - object_inventories: A dictionary mapping object labels to their inventories (which are dictionaries of provider names to item lists).
    - filepath: The path to the output CSV file.
    """
    object_labels = list(object_inventories.keys())
 
    all_providers = []
    seen = set()
    for inv in object_inventories.values():
        for provider_name in inv:
            if provider_name not in seen:
                seen.add(provider_name)
                all_providers.append(provider_name)
 
    with open(filepath, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.writer(f)
        writer.writerow(["Data Provider"] + object_labels)
        for provider_name in all_providers:
            row = [provider_name]
            for label in object_labels:
                inv = object_inventories[label]
                row.append(len(inv[provider_name]) if provider_name in inv else "")
            writer.writerow(row)
    print(f"Wrote {filepath}  ({len(all_providers)} providers x {len(object_labels)} objects)")