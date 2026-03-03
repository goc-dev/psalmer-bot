# WARNING: don't use Python triple-quote escape'ing whithin messages

class Message:
    @staticmethod
    def version_info():
        return """
*Version*: `1.0.2026-0303-0831`
"""

    @staticmethod
    def hello_user(i_user_name:str):
        """Return a greeting message for the specifed user"""
        return f"""
Hello, *{i_user_name}*
Are you looking for any psalm/chords?
"""
    
    @staticmethod
    def help_info():
        return """
/start to get a *greeting*
/help to get a detailed *list of commands*
/psalm to *search* psalm/hymn by parameters
/list to list of *Hymnals*
"""

    @staticmethod
    def setting_info():
        return """
*Settings*: _not implemented yet_
"""