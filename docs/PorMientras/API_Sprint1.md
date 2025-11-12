API de Recetas (Recipes)

## Información General

Este documento describe los procedimientos estándar de operación para interactuar con los endpoints de la API de Recetas. La API permite gestionar recetas, incluyendo operaciones de creación, lectura, actualización, eliminación y filtrado.

**Base URL**: `/recipes`

---

## Tabla de Contenidos

1. [Autenticación](#autenticación)
2. [Endpoints](#endpoints)
   - [GET /recipes](#1-get-recipes)
   - [GET /recipes/{recipe_id}](#2-get-recipesrecipe_id)
   - [GET /recipes/{ingredient}](#3-get-recipesingredient)
   - [POST /addrecipe](#4-post-addrecipe)
   - [DELETE /recipes/{recipe_id}](#5-delete-recipesrecipe_id)
   - [PUT /recipes/{recipe_id}](#6-put-recipesrecipe_id)
   - [POST /recipes/filter](#7-post-recipesfilter)
3. [Códigos de Respuesta](#códigos-de-respuesta)
4. [Ejemplos de Uso](#ejemplos-de-uso)

---

## Autenticación

Algunos endpoints requieren autenticación mediante token Bearer. Para estos endpoints, debe incluir el siguiente header en la solicitud:

```
Authorization: Bearer <token>
```

**Endpoints que requieren autenticación:**
- POST /addrecipe
- DELETE /recipes/{recipe_id}
- PUT /recipes/{recipe_id}

---

## Endpoints

### 1. GET /recipes

**Descripción**: Obtiene todas las recetas disponibles en el sistema.

**Autenticación**: No requerida

**Método HTTP**: `GET`

**URL**: `/recipes`

**Parámetros**: Ninguno

**Request Body**: No aplica

**Respuesta Exitosa (200)**:
```json
[
  "Receta 1 - Descripción",
  "Receta 2 - Descripción",
  "Receta 3 - Descripción"
]
```
---

### 2. GET /recipes/{recipe_id}

**Descripción**: Obtiene los detalles de una receta específica por su ID.

**Autenticación**: No requerida

**Método HTTP**: `GET`

**URL**: `/recipes/{recipe_id}`

**Parámetros de URL**:
- `recipe_id` (integer, requerido): ID único de la receta

**Request Body**: No aplica

**Respuesta Exitosa (200)**:
```json
{
  "id": 1,
  "name": "Pasta Carbonara",
  "categories": ["Italiana", "Pasta"],
  "ingredients": ["Pasta", "Huevos", "Panceta", "Queso parmesano"],
  "duration": 30,
  "instructions": "Paso 1... Paso 2...",
  "portions": 4,
  "rating": 4.5,
  "author": "usuario123"
}
```

**Respuesta de Error (404)**:
```json
{
  "error": "Receta no encontrada"
}
```
---

### 3. GET /recipes/{ingredient}

**Descripción**: Busca recetas que contengan un ingrediente específico.

**Autenticación**: No requerida

**Método HTTP**: `GET`

**URL**: `/recipes/{ingredient}`

**Parámetros de URL**:
- `ingredient` (string, requerido): Nombre del ingrediente a buscar

**Request Body**: No aplica

**Respuesta Exitosa (200)**:
```json
[
  "Receta 1 con ingrediente X",
  "Receta 2 con ingrediente X"
]
```

**Respuesta cuando no hay resultados (404)**:
```json
{
  "message": "No se encontraron recetas con 'tomate'"
}
```

---

### 4. POST /addrecipe

**Descripción**: Crea una nueva receta en el sistema.

**Autenticación**: **Requerida** (Bearer Token)

**Método HTTP**: `POST`

**URL**: `/addrecipe`

**Headers Requeridos**:
```
Content-Type: application/json
Authorization: Bearer <token>
```

**Request Body** (JSON):
```json
{
  "name": "Nombre de la receta",
  "categories": ["Categoría1", "Categoría2"],
  "ingredients": ["Ingrediente1", "Ingrediente2", "Ingrediente3"],
  "duration": 45,
  "instructions": "Descripción detallada de los pasos a seguir...",
  "portions": 4
}
```

**Campos del Request Body**:
- `name` (string, requerido): Nombre de la receta
- `categories` (array, requerido): Lista de categorías de la receta
- `ingredients` (array, requerido): Lista de ingredientes necesarios
- `duration` (integer, requerido): Tiempo de preparación en minutos
- `instructions` (string, requerido): Instrucciones paso a paso
- `portions` (integer, requerido): Número de porciones que rinde la receta

**Respuesta Exitosa (201)**:
```json
{
  "message": "Receta creada exitosamente",
  "recipe": {
    "id": 10,
    "name": "Nombre de la receta",
    "categories": ["Categoría1", "Categoría2"],
    "ingredients": ["Ingrediente1", "Ingrediente2"],
    "duration": 45,
    "instructions": "Descripción detallada...",
    "portions": 4,
    "rating": 0,
    "author": "usuario123"
  }
}
```

**Respuestas de Error**:

**400 - Datos incompletos**:
```json
{
  "error": "Se necesita información adicional sobre la receta"
}
```

**401 - No autenticado**:
```json
{
  "error": "Proporcione un token valido en Authorization: Bearer <token>"
}
```
---

### 5. DELETE /recipes/{recipe_id}

**Descripción**: Elimina una receta específica del sistema. Solo el autor de la receta puede eliminarla.

**Autenticación**: **Requerida** (Bearer Token)

**Método HTTP**: `DELETE`

**URL**: `/recipes/{recipe_id}`

**Parámetros de URL**:
- `recipe_id` (integer, requerido): ID de la receta a eliminar

**Headers Requeridos**:
```
Authorization: Bearer <token>
```

**Request Body**: No aplica

**Respuesta Exitosa (200)**:
```json
{
  "message": "Receta eliminada",
  "recipe": "Nombre de la receta eliminada"
}
```

**Respuestas de Error**:

**401 - No autenticado**:
```json
{
  "error": "Proporcione un token valido en Authorization: Bearer <token>"
}
```

**403 - No autorizado**:
```json
{
  "error": "No autorizado para eliminar esta receta"
}
```

**404 - Receta no encontrada**:
```json
{
  "error": "Receta no encontrada"
}
```

---

### 6. PUT /recipes/{recipe_id}

**Descripción**: Actualiza los datos de una receta existente. Solo el autor de la receta puede actualizarla.

**Autenticación**: **Requerida** (Bearer Token)

**Método HTTP**: `PUT`

**URL**: `/recipes/{recipe_id}`

**Parámetros de URL**:
- `recipe_id` (integer, requerido): ID de la receta a actualizar

**Headers Requeridos**:
```
Content-Type: application/json
Authorization: Bearer <token>
```

**Request Body** (JSON):

Puede incluir uno o más de los siguientes campos. Solo se actualizarán los campos proporcionados:

```json
{
  "name": "Nuevo nombre de la receta",
  "categories": ["Nueva categoría"],
  "ingredients": ["Nuevo ingrediente1", "Nuevo ingrediente2"],
  "duration": 60,
  "instructions": "Nuevas instrucciones...",
  "portions": 6
}
```

**Campos Permitidos para Actualización**:
- `name` (string, opcional): Nuevo nombre de la receta
- `categories` (array, opcional): Nueva lista de categorías
- `ingredients` (array, opcional): Nueva lista de ingredientes
- `duration` (integer, opcional): Nuevo tiempo de preparación
- `instructions` (string, opcional): Nuevas instrucciones
- `portions` (integer, opcional): Nuevo número de porciones

**Nota**: Cualquier campo que no esté en la lista anterior será ignorado por seguridad.

**Respuesta Exitosa (200)**:
```json
{
  "id": 5,
  "name": "Nuevo nombre de la receta",
  "categories": ["Nueva categoría"],
  "ingredients": ["Nuevo ingrediente1", "Nuevo ingrediente2"],
  "duration": 60,
  "instructions": "Nuevas instrucciones...",
  "portions": 6,
  "rating": 4.2,
  "author": "usuario123"
}
```

**Respuestas de Error**:

**400 - Datos inválidos**:
```json
{
  "error": "Datos de actualización inválidos"
}
```

**401 - No autenticado**:
```json
{
  "error": "Proporcione un token valido en Authorization: Bearer <token>"
}
```

**403 - No autorizado**:
```json
{
  "error": "No autorizado para editar esta receta"
}
```

**404 - Receta no encontrada**:
```json
{
  "error": "Receta no encontrada"
}
```


---

### 7. POST /recipes/filter

**Descripción**: Filtra recetas según criterios específicos. Permite búsquedas avanzadas combinando múltiples parámetros.

**Autenticación**: No requerida

**Método HTTP**: `POST`

**URL**: `/recipes/filter`

**Headers Requeridos**:
```
Content-Type: application/json
```

**Request Body** (JSON):

Todos los campos son opcionales. Puede combinar múltiples criterios:

```json
{
  "name": "pasta",
  "categories": ["Italiana"],
  "ingredients": ["tomate"],
  "duration": 30,
  "rating": 4.0
}
```

**Campos de Filtrado Disponibles**:
- `name` (string, opcional): Busca recetas cuyo nombre contenga este texto
- `categories` (array, opcional): Filtra por categorías específicas
- `ingredients` (array, opcional): Filtra recetas que contengan estos ingredientes
- `duration` (integer, opcional): Filtra recetas con duración menor o igual a este valor (en minutos)
- `rating` (float, opcional): Filtra recetas con calificación mayor o igual a este valor

**Respuesta Exitosa con Resultados (200)**:
```json
{
  "count": 2,
  "recipes": [
    {
      "id": 1,
      "name": "Pasta Carbonara",
      "categories": ["Italiana", "Pasta"],
      "ingredients": ["Pasta", "Huevos", "Panceta"],
      "duration": 30,
      "instructions": "...",
      "portions": 4,
      "rating": 4.5,
      "author": "usuario1"
    },
    {
      "id": 3,
      "name": "Pasta Alfredo",
      "categories": ["Italiana", "Pasta"],
      "ingredients": ["Pasta", "Crema", "Queso"],
      "duration": 25,
      "instructions": "...",
      "portions": 3,
      "rating": 4.2,
      "author": "usuario2"
    }
  ]
}
```

**Respuesta Sin Resultados (200)**:
```json
{
  "message": "No se encontraron recetas con los filtros aplicados",
  "recipes": []
}
```

**Respuestas de Error**:

**400 - Duration inválido**:
```json
{
  "error": "Duration debe ser un número"
}
```

**400 - Rating inválido**:
```json
{
  "error": "Rating debe ser un número"
}
```

---

## Códigos de Respuesta

| Código | Significado | Descripción |
|--------|-------------|-------------|
| 200 | OK | La solicitud se procesó correctamente |
| 201 | Created | El recurso se creó exitosamente |
| 400 | Bad Request | Los datos enviados son inválidos o incompletos |
| 401 | Unauthorized | No se proporcionó autenticación o el token es inválido |
| 403 | Forbidden | El usuario no tiene permisos para realizar esta acción |
| 404 | Not Found | El recurso solicitado no existe |

---
