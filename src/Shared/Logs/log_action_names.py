from enum import Enum

class LogActionNames(Enum):
    DELETE_ACCOUNT = "DeleteAccount"
    RESTORE_PROFILE = "RestoreProfile"
    LOGIN = "Login"
    REGISTER = "Register"
    PASSWORD_CHANGE = "PasswordChange"
    CREATE_RECIPE = "CreateRecipe"
    DELETE_RECIPE = "DeleteRecipe"
    UPDATE_RECIPE = "UpdateRecipe"