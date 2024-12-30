class OpponentModel:

    
    def __init__(self):
        self.model = {}  # Stores frequency of issue-value pairs

    def update_model(self, bid):
        # Iterate over issues and values in the bid
        for issue, value in bid:
            if issue not in self.model:
                self.model[issue] = {}
            if value not in self.model[issue]:
                self.model[issue][value] = 1
            else:
                self.model[issue][value] += 1  # Increment frequency

        self.normalize_model()

    def normalize_model(self):
        # Normalize frequencies to probabilities
        for issue in self.model:
            total = sum(self.model[issue].values())
            for value in self.model[issue]:
                self.model[issue][value] /= total

    def evaluate_bid(self, bid):
        # Calculate the utility of a bid based on normalized frequencies
        utility = 0
        for issue, value in bid:
            utility += self.model.get(issue, {}).get(value, 0)
        return utility
