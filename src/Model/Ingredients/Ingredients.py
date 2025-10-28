from __future__ import annotations

from typing import List, Optional, Callable, Union, Set


class Ingredient:
        """Ingredient value object.

        This class implements a non-intrusive Composite-style API for ingredient
        composition. The intention is to represent that an ingredient may be a
        simple/base ingredient (no components) or a composite ingredient (it
        contains other ingredients as components). We keep the representation
        backward-compatible by allowing `components` to store either raw ids
        (int/str) or `Ingredient` instances. The model does not import or depend
        on repository code; instead helper methods accept an optional
        `resolver(id) -> Ingredient` callable to convert ids into objects when
        needed.

        Key behaviors provided:
        - `to_json(depth, resolver)` lets callers control whether components are
            expanded (depth>0) or left as shallow ids (depth=0, default). This
            avoids recursive/expensive serialization by default.
        - `get_components(resolver)` resolves and returns child Ingredient
            objects when possible (ignores unresolved ids).
        - `add_component` / `remove_component` mutate the components list (they
            accept either ids or Ingredient instances).
        - `flatten(resolver)` returns a depth-first flat list of child
            Ingredient objects, using `resolver` to resolve ids. Useful for
            traversals in use-cases without coupling the model to storage.
        - `detect_cycle(resolver)` performs DFS to detect cycles in the
            composition graph reachable from this node (important to avoid
            infinite recursion when composing ingredients).

        Design notes / migration guidance:
        - Backwards compatibility: existing code that created `Ingredient(...,
            components=[...])` with ids will continue to work. To traverse or
            expand components, call the helpers and pass the repository's
            `get_by_id` as the resolver.
        - If an application later prefers in-memory nested objects, the
            repository may instantiate `Ingredient` objects and assign object
            instances into `components` (the helpers work the same way).
        - The model intentionally avoids raising on unresolved ids; callers
            choose how to handle missing references.
        """

    def __init__(
        self,
        id,
        name,
        categories: Optional[List[str]] = None,
        substitutes: Optional[List[str]] = None,
        components: Optional[List[Union[int, str, "Ingredient"]]] = None,
        recipe_count: int = 0,
    ):
        self.id = id
        self.name = name
        self.categories = list(categories or [])
        self.substitutes = list(substitutes or [])
        # components can be ids (int/str) or Ingredient objects
        self.components = list(components or [])
        self.recipe_count = int(recipe_count)

    def to_json(self, depth: int = 0, resolver: Optional[Callable[[Union[int, str]], "Ingredient"]] = None) -> dict:
        """Serialize the ingredient.

        - depth=0 (default) -> shallow: components left as provided (ids or objects' ids)
        - depth>0 -> try to expand components recursively up to depth levels.
        If a component is an id and `resolver` is provided, resolver(id) will be
        called to obtain the Ingredient object to serialize.
        """
        data = {
            "id": self.id,
            "name": self.name,
            "categories": self.categories,
            "substitutes": self.substitutes,
            "components": [],
            "recipe_count": self.recipe_count,
        }

        if depth <= 0:
            # preserve raw components (ids or Ingredient objects -> use id)
            comps = []
            for c in self.components:
                if hasattr(c, "id"):
                    comps.append(c.id)
                else:
                    comps.append(c)
            data["components"] = comps
            return data

        serialized = []
        for c in self.components:
            if hasattr(c, "to_json"):
                # c is an Ingredient instance
                serialized.append(c.to_json(depth=depth - 1, resolver=resolver))
            else:
                # c is an id -> try resolver
                if resolver:
                    try:
                        obj = resolver(c)
                    except Exception:
                        obj = None
                    if obj is not None:
                        serialized.append(obj.to_json(depth=depth - 1, resolver=resolver))
                    else:
                        serialized.append(c)
                else:
                    serialized.append(c)

        data["components"] = serialized
        return data

    def __str__(self) -> str:
        return self.name

    def has_substitutes(self) -> bool:
        return len(self.substitutes) > 0

    def is_base_ingredient(self) -> bool:
        return len(self.components) == 0

    # Composite helpers
    def get_components(self, resolver: Optional[Callable[[Union[int, str]], "Ingredient"]] = None) -> List["Ingredient"]:
        """Return component Ingredient objects when possible.

        If components are stored as ids, `resolver` will be used to obtain
        Ingredient objects. Unresolved ids are ignored.
        """
        out: List[Ingredient] = []
        for c in self.components:
            if hasattr(c, "to_json"):
                out.append(c)
            else:
                if resolver:
                    try:
                        obj = resolver(c)
                    except Exception:
                        obj = None
                    if obj is not None:
                        out.append(obj)
        return out

    def add_component(self, component: Union[int, str, "Ingredient"]) -> None:
        """Add a component (id or Ingredient). Does not resolve cycles by itself."""
        self.components.append(component)

    def remove_component(self, component: Union[int, str, "Ingredient"]) -> None:
        target = component.id if hasattr(component, "id") else component
        new = []
        for c in self.components:
            cid = c.id if hasattr(c, "id") else c
            if cid != target:
                new.append(c)
        self.components = new

    def flatten(self, resolver: Optional[Callable[[Union[int, str]], "Ingredient"]] = None, max_depth: int = 50) -> List["Ingredient"]:
        """Return a flat list of component Ingredient objects (depth-first).
        Uses `resolver` for id -> Ingredient resolution. Skips unresolved ids.
        """
        out: List[Ingredient] = []
        seen: Set[Union[int, str]] = set()

        def _id_of(x: Union[int, str, Ingredient]) -> Union[int, str]:
            return x.id if hasattr(x, "id") else x

        def _walk(node: "Ingredient", depth: int):
            if depth <= 0:
                return
            for c in node.components:
                if hasattr(c, "to_json"):
                    child = c
                    cid = child.id
                else:
                    cid = c
                    child = resolver(cid) if resolver else None
                if child is None:
                    continue
                if cid in seen:
                    continue
                seen.add(cid)
                out.append(child)
                _walk(child, depth - 1)

        _walk(self, max_depth)
        return out

    def detect_cycle(self, resolver: Optional[Callable[[Union[int, str]], "Ingredient"]] = None) -> bool:
        """Detect cycles in the composition graph reachable from this node."""
        visiting: Set[Union[int, str]] = set()
        visited: Set[Union[int, str]] = set()

        def _id_of(x: Union[int, str, Ingredient]) -> Union[int, str]:
            return x.id if hasattr(x, "id") else x

        def _walk(node: "Ingredient") -> bool:
            nid = _id_of(node)
            if nid in visiting:
                return True
            if nid in visited:
                return False
            visiting.add(nid)
            for c in node.components:
                child = c if hasattr(c, "to_json") else (resolver(c) if resolver else None)
                if child is None:
                    continue
                if _walk(child):
                    return True
            visiting.remove(nid)
            visited.add(nid)
            return False

        return _walk(self)
