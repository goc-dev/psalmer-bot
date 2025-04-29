class MarkdownV2:
    @staticmethod
    def escape_text(i_text: str) -> str:
        special_characters = r"_*[]()~`>#+-=|{}.!"
        for char in special_characters:
            i_text = i_text.replace(char, f"\\{char}")
        return i_text