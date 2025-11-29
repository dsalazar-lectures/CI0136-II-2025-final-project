#  Application of SOLID Principle in the Recipes Module

## **Functionality Implementing the Principle**

The **Recipes** feature which includes creating, validating, storing, and exposing recipes through the API applies the Single Responsibility Principle (SRP) to ensure clean separation of concerns.

## **Name of the Principle**

**Single Responsibility Principle (SRP)**
The “S” in SOLID.

## **Principle Description**

The **Single Responsibility Principle** states that:

> *A class or module should have only one reason to change.*

This means each component in the system must focus on a single, well-defined responsibility.
Applying SRP improves modularity, reduces coupling, and allows each part of the system to evolve independently.

## **Motivation for Use**

The recipes feature involves several distinct concerns:

* Data validation
* Business logic
* File persistence
* HTTP request handling

Without SRP, these concerns could easily become mixed within the same class, generating tightly coupled and difficult-to-test code.

SRP was chosen because:

* It **supports modularity** and clean layering.
* It **enables easier mocking** of the repository during unit tests (preventing CSV creation).
* It **allows future teams to replace storage or extend functionality without breaking existing code**.
* It contributes to producing code that is **maintainable, extensible, and aligned with course design expectations**.

## **Implementation Explanation**

The recipes module was divided into four clearly separated components, each with a single responsibility:

### 1. **`RecipeSchema` Data Validation**

* Defines the structure of a recipe.
* Validates incoming fields before creation.
* Ensures data consistency.

**Reason to change:** recipe attributes or validation rules.

### 2. **`RecipeRepository` Data Persistence**

* Handles reading and writing recipes.
* Encapsulates CSV/JSON/file operations.

**Reason to change:** storage mechanism or file format.

This separation is what enables **mocking the repository in tests**, avoiding file creation.

### 3. **`RecipeService` Business Logic**

* Creates valid recipe objects using the schema.
* Applies business rules.
* Delegates persistence to the repository.

**Reason to change:** business rules or application logic.

### 4. **`RecipeAPI` HTTP Interface**

* Exposes endpoints for clients.
* Routes operations to the service.
* Formats API responses.

**Reason to change:** API structure or request/response behavior.

## **Guide for Future Extension**

Future teams can extend or reuse the SRP structure easily:

### To change the storage method

Create a new repository class (e.g., `RecipeRepositorySQL`) and inject it into the service.
No changes needed to service or API.

### To add new fields or validation rules

Update only `RecipeSchema`.

### To add new recipe-related operations

Extend `RecipeService` (e.g., filtering, sorting).
The repository and API remain unaffected.

### To expose new endpoints

Add routes in `RecipeAPI` while reusing the service and schema.

# Summary

Applying **SRP** to the recipes module ensures clean separation of responsibilities, improves maintainability, enables testing without side effects, and provides a structure that future teams can safely extend.