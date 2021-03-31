class TimeError(Exception):
    pass

class RoleNotFoundError(Exception):
    def __init__(self, message):
        self.message = message

class RoleTooHighInHierarchyError(Exception):
    def __init__(self, role):
        self.role = role
