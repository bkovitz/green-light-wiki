class CgiEnvironment:

    def __init__(self, dict):
        self.dict = dict


    def get(self, name):
        result = self.dict.get(name, "")

        if len(result) == 0 and name == "QUERY_STRING":
            result = self.dict.get("QUERY_STRING_UNESCAPED", "")

        return result
