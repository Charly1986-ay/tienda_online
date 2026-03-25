from fastapi import HTTPException


class UserNotFoundException(HTTPException):
    """Excepción cuando un usuario no es encontrado en la base de datos."""
    def __init__(self, detail: str = "Usuario no encontrado"):
        super().__init__(status_code=404, detail=detail)  

class UserNameException(HTTPException):
    """Excepción cuando un usuario ya fue creado."""
    def __init__(self, detail: str = "El nombre del usuario se encuentra ocupado"):
        super().__init__(status_code=401, detail=detail)  

class UserInactiveException(HTTPException):
    """Excepción cuando un usuario esta inactivo."""
    def __init__(self, detail: str = "Usuario inactivo"):
        super().__init__(status_code=400, detail=detail)  

class CredentialsException(HTTPException):
    """Excepción cuando un usuario no puede validar las credenciales."""
    def __init__(self, detail: str = "Credenciales no verificadas", headers = {"X-Error-Code": "INVALID_CREDENTIALS"}):
        super().__init__(status_code=401, detail=detail, headers=headers)   

class UserEmailExistsException (HTTPException):
    """Excepción cuando el email existe en la base de datos."""
    def __init__(self, detail: str = "Email ya existe"):
        super().__init__(status_code=409, detail=detail)
        
class UserPasswordNotStrong(HTTPException):
    """Excepción cuadno el usuario introduce una contraseña débil"""
    def __init__(self, detail:str = "Por favor, introduce una contraseña fuerte."):
        super().__init__(status_code=422, detail=detail)

class UserDniNotValid(HTTPException):
    """Excepción cuadno el usuario introduce formato de dni no válido"""
    def __init__(self, detail:str = "Por favor, proporciona un DNI válido."):
        super().__init__(status_code=422, detail=detail)

class RoleNotFoundException(HTTPException):
    """Excepción cuando un rol no es encontrado en la base de datos."""
    def __init__(self, detail: str = "Rol no encontrado"):
        super().__init__(status_code=404, detail=detail) 


class DatabaseErrorException(HTTPException):
    def __init__(self, message="Error relacionado con la base de datos", status_code=500):
        super().__init__(status_code=status_code, detail=message)

class UnexpectedErrorException(HTTPException):
    def __init__(self, message="Ocurrió un error inesperado", status_code=500):
        super().__init__(status_code=status_code, detail=message)


class ProductNotFoundException(HTTPException):
    """Excepción cuando un producto no es encontrado en la base de datos."""
    def __init__(self, detail: str = "Producto no encontrado"):
        super().__init__(status_code=404, detail=detail)

class ProductExistException(HTTPException):
    """Excepción cuando un producto ya existe en la base de datos"""
    def __init__(self, detail: str = "Ya existe un producto con ese nombre"):
        super().__init__(status_code=409, detail=detail)

class ProductStockException(HTTPException):
    """Excepción cuando un producto no tiene unidades suficientes"""
    def __init__(self, detail: str = "No hay unidades suficientes"):
        super().__init__(status_code=409, detail=detail)
        
class CategoryNotFoundException(HTTPException):
    """Excepción cuando una categoría no es encontrada en la base de datos."""
    def __init__(self, detail: str = "Categoría no encontrada"):
        super().__init__(status_code=404, detail=detail)

class CategoryBadRequestException(HTTPException):
    """Excepción cuando ya existe la categoría en la base de datos."""
    def __init__(self, detail: str = "La Categoría ya existe"):
        super().__init__(status_code=404, detail=detail)