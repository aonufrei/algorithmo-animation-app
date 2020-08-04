
class SettingsError(Exception):
    #Error in settings data
    pass

class NullSettingsException(SettingsError):
    #Empty settings value exception
    pass

class UnknownAlgorithmSettingsException(SettingsError):
    
