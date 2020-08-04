
class SettingsError(Exception):
    #Error in settings data
    pass

class NullSettingsException(SettingsError):
    #Empty settings value exception
    pass

class UnknownAlgorithmException(SettingsError):
    #Unknown algorithm was specified in settings
    pass 

class BadSettingsTypeException(SettingsError):
    #Unknown algorithm was specified in settings
    pass 

