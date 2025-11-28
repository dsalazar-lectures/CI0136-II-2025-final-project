from flask import Blueprint, jsonify, request
from src.Application.Ingredients.IngredientUseCase import ingredient_service

ingredients_bp = Blueprint("ingredients", __name__)


@ingredients_bp.route("/ingredients", methods=["GET"])
def get_all_ingredients():
    # Check if simplified format is requested
    simple = request.args.get("simple", "false").lower() == "true"
    ingredients = ingredient_service.get_all_ingredients()
    if simple:
        return jsonify(
            [
                {"id": ingredient.id, "name": ingredient.name}
                for ingredient in ingredients
            ]
        )
    return jsonify([ingredient.to_json() for ingredient in ingredients])


@ingredients_bp.route("/ingredients/<int:ingredient_id>", methods=["GET"])
def get_ingredient_by_id(ingredient_id):
    """Get a specific ingredient by its ID."""
    ingredient = ingredient_service.get_ingredient_by_id(ingredient_id)
    if not ingredient:
        return jsonify({"error": "Ingrediente no encontrado"}), 404
    return jsonify(ingredient.to_json())


@ingredients_bp.route("/ingredients/create", methods=["POST"])
def create_new_ingredient():
    """Create a new ingredient"""
    name = request.json.get("name")
    if not name:
        return jsonify({"error": "Ingredient name is required"}), 404
    categories = request.json.get("categories")
    substitutes = request.json.get("substitutes")
    components = request.json.get("components")

    ingredient_service.create_ingredient(name, categories, substitutes, components)

    return jsonify({"message": "Ingredient created successfully"}), 201


@ingredients_bp.route("/ingredients/update", methods=["POST"])
def update_ingredient():
    """Update one or more fields of an ingredient"""
    id = request.json.get("id")
    ingredient = ingredient_service.get_ingredient_by_id(id)
    if ingredient is None:
        return jsonify({"message": "Ingredient not found"}), 404

    data = request.json

    for field in ["categories", "substitutes", "components"]:
        if field in data and not isinstance(data[field], list):
            return jsonify({"error": f"{field} must be a list"}), 400

    if "components" in request.json:
        result = ingredient_service.update_components(id, data["components"])
        if result == "Error: base ingredient":
            return (
                jsonify(
                    {
                        "error": "selected ingredient is base ingredient and has no components"
                    }
                ),
                400,
            )

    if "categories" in request.json:
        ingredient_service.update_categories(id, data["categories"])

    if "substitutes" in request.json:
        ingredient_service.update_substitutes(id, data["substitutes"])

    return jsonify({"message": "Ingredient updated successfully"}), 200


@ingredients_bp.route("/ingredients/delete", methods=["POST"])
def delete_ingredient():
    """Delete an ingredient"""
    # User permissions need to be validated here
    id = request.json.get("id")

    result = ingredient_service.delete_ingredient(id)

    if result == "ID is not valid":
        return jsonify({"error": "Ingredient not found"}), 404

    return jsonify({"message": "Ingredient deleted successfully"}), 200


@ingredients_bp.route("/ingredients/search", methods=["POST"])
def search_ingredients_body():
    """Search for ingredients by name OR ID OR category"""
    data = _get_request_data()
    if isinstance(data, tuple):
        return data

    simple = _get_simple_flag(data)

    # Verify that only one search criterion is provided
    search_criteria = [key for key in ["names", "ids", "categories"] if key in data]
    if len(search_criteria) == 0:
        return (
            jsonify(
                {
                    "error": "Se requiere un criterio de búsqueda (names, ids, o categories)"
                }
            ),
            400,
        )
    if len(search_criteria) > 1:
        return (
            jsonify({"error": "Solo se permite un criterio de búsqueda a la vez"}),
            400,
        )

    criterion = search_criteria[0]
    if criterion == "names":
        names = _parse_names(data)
        if isinstance(names, tuple):
            return names
        if len(names) == 1:
            return _handle_single_name(names[0], simple)
        return _handle_multiple_names(names, simple)

    elif criterion == "ids":
        ids = _parse_ids(data)
        if isinstance(ids, tuple):
            return ids
        return _handle_multiple_ids(ids, simple)

    else:  # categories
        categories = _parse_categories(data)
        if isinstance(categories, tuple):
            return categories
        return _handle_categories(categories, simple)


def _get_request_data():
    """Retrieves and validates the JSON body."""
    data = request.get_json(silent=True)
    if data is None:
        return jsonify({"error": "Cuerpo JSON requerido"}), 400
    return data


def _get_simple_flag(data):
    """Query param ?simple=true overrides body.simple"""
    simple_q = request.args.get("simple")
    if simple_q is not None:
        return simple_q.lower() == "true"
    return bool(data.get("simple")) if "simple" in data else False


def _parse_names(data):
    raw = data.get("names")
    if raw is None:
        return jsonify({"error": "Campo 'names' requerido en el body"}), 400

    if isinstance(raw, str):
        items = [n.strip() for n in raw.split(",")]
    elif isinstance(raw, list):
        items = [str(n).strip() for n in raw]
    else:
        return jsonify({"error": "Campo 'names' debe ser lista o string"}), 400

    names = [n for n in items if n]
    if not names:
        return jsonify({"error": "No se encontraron nombres válidos"}), 400

    return names


def _handle_single_name(name, simple):
    ingredient = ingredient_service.get_ingredient_by_name(name)
    if ingredient is None:
        return jsonify({"error": "Ingrediente no encontrado"}), 404
    return jsonify(
        {"id": ingredient.id, "name": ingredient.name}
        if simple
        else ingredient.to_json()
    )


def _handle_multiple_names(names, simple):
    """Searches for multiple ingredients and returns results + missing items."""
    results = []
    not_found = []
    for name in names:
        ingredient = ingredient_service.get_ingredient_by_name(name)
        if ingredient:
            results.append(
                {"id": ingredient.id, "name": ingredient.name}
                if simple
                else ingredient.to_json()
            )
        else:
            not_found.append(name)
    return jsonify({"results": results, "not_found": not_found}), 200


def _parse_ids(data):
    raw = data.get("ids")
    if not raw:
        return []

    try:
        if isinstance(raw, str):
            items = [int(id.strip()) for id in raw.split(",")]
        elif isinstance(raw, list):
            items = [int(id) for id in raw]
        else:
            return jsonify({"error": "Campo 'ids' debe ser lista o string"}), 400

        return [id for id in items if id > 0]
    except ValueError:
        return jsonify({"error": "Los IDs deben ser números enteros"}), 400


def _parse_categories(data):
    raw = data.get("categories")
    if not raw:
        return []

    if isinstance(raw, str):
        items = [cat.strip() for cat in raw.split(",")]
    elif isinstance(raw, list):
        items = [str(cat).strip() for cat in raw]
    else:
        return jsonify({"error": "Campo 'categories' debe ser lista o string"}), 400

    return [cat for cat in items if cat]


def _handle_multiple_ids(ids, simple):
    results = []
    not_found = []
    for iid in ids:
        ingredient = ingredient_service.get_ingredient_by_id(iid)
        if ingredient:
            results.append(
                {"id": ingredient.id, "name": ingredient.name}
                if simple
                else ingredient.to_json()
            )
        else:
            not_found.append(iid)
    return jsonify({"results": results, "not_found": not_found}), 200


def _handle_categories(categories, simple):
    results = []
    for category in categories:
        ingredients = ingredient_service.get_ingredients_by_category(category)
        for ingredient in ingredients:
            results.append(
                {"id": ingredient.id, "name": ingredient.name}
                if simple
                else ingredient.to_json()
            )
    # remove duplicates by id
    unique = []
    seen = set()
    for r in results:
        iid = r["id"]
        if iid not in seen:
            seen.add(iid)
            unique.append(r)
    return jsonify({"results": unique}), 200
