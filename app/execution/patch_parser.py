import json

class PatchParser:

    @staticmethod
    def parse(response_text):

        try:

            return json.loads(response_text)

        except Exception as e:

            return {
                "error": str(e)
            }