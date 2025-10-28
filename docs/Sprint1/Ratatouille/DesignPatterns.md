# Repository Pattern

## Función
El patrón de diseño Repository provee una abstracción entre el acceso a los datos y los detalles de la lógica detrás. Para este proyecto se creó un repositorio en función del manejo de datos de los usuarios.

#### Interfaz base

```python

    class IUserRepository(ABC):
    @abstractmethod
    def user_exists(self, username, email):
        pass

    @abstractmethod
    def create_user(self, user_dto):
        pass

    @abstractmethod
    def get_user_by_username(self, username):
        pass

```
#### Implementación concreta
```python
    class UserRepository(IUserRepository):
        def __init__(self, csv_file_path="users.csv"):
            self.user_csv = UserCSV(csv_file_path)
            
        def user_exists(self, username, email):
            return self.user_csv.user_exists(username, email)

```
## Beneficios

1. Abstracción de datos: 
    - Oculta los detalles de la persistencia.
    - La capa de aplicación interactúa solo con la interfaz.
2. Mantenibilidad:
    - Facilita cambios en el almacenamiento de datos.
    - Permite migrar de CSV a una base de datos sin afectar la lógica.
3.  Testabilidad:
    - Permite crear mocks fácilmente para pruebas.
4. Separación de responsabilidades(SRP):
    - La clase `UserRepository` se enfoca en operaciones de persistencia.

## Implementación

```python

    class UserApplicationService:
        def __init__(
            self,
            user_repository: IUserRepository,
        ):
            self.user_repository = user_repository

        def register_user(self, data):
            .
            .
            .
            exists = self.user_repository.user_exists(data["username"], data["email"])

```

## Guía de Extensión 

### Para crear nuevo repositorio:
```python
class INewEntityRepository(ABC):
    @abstractmethod
    def entity_exists(self, id: str) -> bool:
        pass
    
    @abstractmethod
    def create_entity(self, entity_dto: EntityDTO) -> bool:
        pass

class NewEntityRepository(INewEntityRepository):
    def __init__(self, storage_path="entities.csv"):
        self.storage = Storage(storage_path)
```

# DTO (Data Transfer Object)

## Función
Un DTO es un objeto simple que transporta datos entre capas (por ejemplo, entre la capa de aplicación y la capa de presentación o persistencia). En este proyecto `UserDTO` actúa como contrato ligero para los datos de usuario evitando exponer entidades de dominio o estructuras de persistencia.

## Responsabilidades típicas de `UserDTO`
- Contener solo los campos necesarios.
- Convertirse a/desde formatos serializables.
- Proveer métodos auxiliares de mapeo (por ejemplo `to_dict`).

## Beneficios
- Desacopla la capa de presentación/HTTP de las entidades internas.
- Facilita la serialización y la validación simple.
- Mejora testabilidad al usar objetos simples en pruebas.
- Evita fugas de implementación (por ejemplo, campos internos de la entidad o referencias a la base de datos).

## Implementación
```python
class UserDTO:
    def __init__(self, username: str, email: str, full_name: str = None):
        self.username = username
        self.email = email
        self.full_name = full_name

    def to_dict(self) -> dict:
        return {"username": self.username, "email": self.email, "full_name": self.full_name}
```

## Uso concreto en el proyecto
- En los endpoints: parsear JSON de la petición a `UserDTO` y pasarlo al servicio de aplicación.
- En la capa de aplicación: recibir `UserDTO`, ejecutar validaciones y transformar a entidad si es necesario.
- En la persistencia: mapear datos desde la entidad a `UserDTO` para respuesta o logging.

## Guía de Extensión

### Template para nuevos DTOs:
```python
@dataclass
class NewEntityDTO:
    id: str
    name: str
    created_at: datetime = field(default_factory=datetime.now)
    
    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "created_at": self.created_at.isoformat()
        }
```

# Service Layer Pattern

## Función
El Service Layer Pattern actúa como intermediario entre los controladores (API) y la capa de dominio/repositorio, encapsulando la lógica de negocio principal.

## Estructura implementada
### Servicio principal
#### UserApplicationService
```python
    class UserApplicationService:
    def __init__(
        self,
        user_repository: IUserRepository,
        validation_service: IValidationService,
        encryption_service: IEncryptionService,
        token_service: ITokenService,
    ):
        self.validation_service = validation_service
        self.user_repository = user_repository
        self.encryption_service = encryption_service
        self.token_service = token_service

```
### Servicios secundarios
- `ValidationService`: Validación del formato de los datos del usuario.
- `EncryptionService`: Encriptación de contraseña.
- `TokenService`: Gestión de JWT.

## Beneficios
- Separación de responsabilidades: Servicios divididos por asuntos especificos. Esto facilita el mantenimiento y el testing.
- Desacoplamiento: Los servicios son totalmente  independientes entre sí.
- Escalabilidad: Nuevos servicios pueden agregarse sin afectar la lógica original.
- Reutilización: Los servicios pueden utilizarse 
en diversas partes del código fácilmente.

## Guía de Extensión 

### Template para nuevos servicios:
```python
class NewEntityService:
    def __init__(
        self,
        repository: INewEntityRepository,
        validation_service: IValidationService
    ):
        self.repository = repository
        self.validation_service = validation_service
    
    def process_entity(self, entity_dto: NewEntityDTO) -> bool:
        if not self.validation_service.validate(entity_dto):
            return False
        return self.repository.create_entity(entity_dto)
```