**Función / Ruta**: `generate_menus` — GET `/menu/<category>/<count>`  

**Qué hace**: devuelve exactamente `count` menús para la categoría solicitada. Cada elemento:  
  `{ "menu": "Menú #i", "recipe": <recipe.to_dict()> }` 
 
**Comportamiento clave**:
  - `count < 1` → 400 `{ "error": "count must be a positive integer" }`
  - Si no hay recetas en la categoría → `[]` (200)
  - Si `count > n_recipes` → las recetas se repiten cíclicamente (wrap‑around)
**Tests que lo cubren**: `tests/Unittests/Menu/test_generate_menus.py`  
  - Verifica caso cuando `count == número de recetas` y caso de repetición cuando `count > número de recetas`.

**Ejemplo**:  
  GET `/menu/category1/2` →  
  ```json
  [
    { "menu": "Menú #1", "recipe": { "id": 1, "name": "recipe1", "...": "..." } },
    { "menu": "Menú #2", "recipe": { "id": 2, "name": "recipe2", "...": "..." } }
  ]
  ```

**Comando para verificar tests**:
  ```bash
  python3 -m unittest tests.Unittests.Menu.test_generate_menus -v
  ```
