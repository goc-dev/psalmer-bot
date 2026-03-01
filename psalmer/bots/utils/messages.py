class Message:
    @staticmethod
    def hello_user(i_user_name:str):
        """Return a greeting message for the specifed user"""
        v_message = f"""
Hello, *{i_user_name}*!
Are you looking for any psalm/chords?
"""
        return v_message
    
    @staticmethod
    def help_info():
        return """
/start to get a greeting
/help to get a detailed list of commands
/psalm to search psalm/hymn by parameters
/list to list of Hymnals \(Song Books\)
"""