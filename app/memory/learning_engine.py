class LearningEngine:

    @staticmethod
    def learn(state):

        successful_pattern = {
            "objective": state["objective"],
            "solution": state["generated_code"]
        }

        return successful_pattern