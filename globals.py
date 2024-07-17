class GlobalComponents:
    COMPONENTS = {}
    
    @classmethod
    def set(cls, key: str, component: any):
        cls.COMPONENTS[key] = component 
        
    @classmethod
    def get(cls, key: str):
        return cls.COMPONENTS[key] if key in cls.COMPONENTS else None
    
class GlobalValues:
    VALUES = {}
    @classmethod
    def set(cls, key: str, value: any):
        cls.VALUES[key] = value 
        
    @classmethod
    def get(cls, key: str):
        return cls.VALUES[key] if key in cls.VALUES else None
    