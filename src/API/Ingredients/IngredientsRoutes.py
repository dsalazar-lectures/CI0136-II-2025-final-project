from flask import Blueprint, jsonify, request
from src.Application.Ingredients.IngredientUseCase import ingredient_service

ingredients_bp = Blueprint("ingredients", __name__)


@ingredients_bp.route("/ingredients", methods=["GET"])
def get_all_ingredients():
     # Check if simplified format is requested
    simple = request.args.get('simple', 'false').lower() == 'true'
    ingredients = ingredient_service.get_all_ingredients()
    if simple:
        return jsonify([{
            'id': ingredient.id,
            'name': ingredient.name
        } for ingredient in ingredients])
    return jsonify([ingredient.to_json() for ingredient in ingredients])


@ingredients_bp.route("/ingredients/<int:ingredient_id>", methods=["GET"])
def get_ingredient_by_id(ingredient_id):
    """Get a specific ingredient by its ID."""
    ingredient = ingredient_service.get_ingredient_by_id(ingredient_id)
    if not ingredient:
        return jsonify({"error": "Ingrediente no encontrado"}), 404
    return jsonify(ingredient.to_json())

@ingredients_bp.route("/ingredients/search", methods=["POST"])
def search_ingredients_body():
    """Buscar ingredientes por nombres O ids O categorías (solo un criterio a la vez)."""
    data = _get_request_data()
    if isinstance(data, tuple):
        return data

    simple = _get_simple_flag(data)
    
    # Verificar que solo venga un criterio de búsqueda
    search_criteria = [key for key in ['names', 'ids', 'categories'] if key in data]
    if len(search_criteria) == 0:
        return jsonify({
            "error": "Se requiere un criterio de búsqueda (names, ids, o categories)"
        }), 400
    if len(search_criteria) > 1:
        return jsonify({
            "error": "Solo se permite un criterio de búsqueda a la vez"
        }), 400

    criterion = search_criteria[0]
    if criterion == 'names':
        names = _parse_names(data)
        if isinstance(names, tuple):
            return names
        return _handle_multiple_names(names, simple)
    
    elif criterion == 'ids':
        ids = _parse_ids(data)
        if isinstance(ids, tuple):
            return ids
        return jsonify(_handle_multiple_ids(ids, simple))
    
    else:  # categories
        categories = _parse_categories(data)
        if isinstance(categories, tuple):
            return categories
        return jsonify({"results": _handle_categories(categories, simple)})

def _get_request_data():
    """Obtiene y valida el cuerpo JSON."""
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "Cuerpo JSON requerido"}), 400
    return data

def _get_simple_flag(data):
    """Obtiene el parámetro 'simple' desde query o body."""
    simple_q = request.args.get('simple')
    if simple_q is not None:
        return simple_q.lower() == 'true'
    return bool(data.get('simple')) if 'simple' in data else False

def _parse_names(data):
    """Normaliza el campo 'names' (lista o string con comas)."""
    raw = data.get('names')
    if raw is None:
        return jsonify({"error": "Campo 'names' requerido en el body"}), 400

    if isinstance(raw, str):
        items = [n.strip() for n in raw.split(',')]
    elif isinstance(raw, list):
        items = [str(n).strip() for n in raw]
    else:
        return jsonify({"error": "Campo 'names' debe ser lista o string"}), 400

    names = [n for n in items if n]
    if not names:
        return jsonify({"error": "No se encontraron nombres válidos"}), 400

    return names

def _handle_single_name(name, simple):
    """Busca un solo ingrediente y devuelve resultado o 404."""
    ingredient = ingredient_service.get_ingredient_by_name(name)
    if ingredient is None:
        return jsonify({"error": "Ingrediente no encontrado"}), 404
    return jsonify(
        {'id': ingredient.id, 'name': ingredient.name} if simple else ingredient.to_json()
    )

def _handle_multiple_names(names, simple):
    """Busca múltiples ingredientes y devuelve resultados + faltantes."""
    results = []
    not_found = []

    for name in names:
        ingredient = ingredient_service.get_ingredient_by_name(name)
        if ingredient:
            results.append({'id': ingredient.id, 'name': ingredient.name} if simple else ingredient.to_json())
        else:
            not_found.append(name)

    return jsonify({"results": results, "not_found": not_found})

def _parse_ids(data):
    """Normaliza el campo 'ids' (lista o string con comas)."""
    raw = data.get('ids')
    if not raw:
        return []

    try:
        if isinstance(raw, str):
            items = [int(id.strip()) for id in raw.split(',')]
        elif isinstance(raw, list):
            items = [int(id) for id in raw]
        else:
            return jsonify({"error": "Campo 'ids' debe ser lista o string"}), 400

        return [id for id in items if id > 0]
    except ValueError:
        return jsonify({"error": "Los IDs deben ser números enteros"}), 400
    
def _parse_categories(data):
    """Normaliza el campo 'categories' (lista o string con comas)."""
    raw = data.get('categories')
    if not raw:
        return []

    if isinstance(raw, str):
        items = [cat.strip() for cat in raw.split(',')]
    elif isinstance(raw, list):
        items = [str(cat).strip() for cat in raw]
    else:
        return jsonify({"error": "Campo 'categories' debe ser lista o string"}), 400

    return [cat for cat in items if cat]

def _handle_multiple_ids(ids, simple):
    """Busca múltiples ingredientes por ID."""
    results = []
    not_found = []

    for id in ids:
        ingredient = ingredient_service.get_ingredient_by_id(id)
        if ingredient:
            results.append(
                {'id': ingredient.id, 'name': ingredient.name} if simple else ingredient.to_json()
            )
        else:
            not_found.append(id)

    return {"results": results, "not_found": not_found}

def _handle_categories(categories, simple):
    """Busca ingredientes por categorías."""
    results = []
    for category in categories:
        ingredients = ingredient_service.get_ingredients_by_category(category)
        for ingredient in ingredients:
            results.append(
                {'id': ingredient.id, 'name': ingredient.name} if simple else ingredient.to_json()
            )
    return results