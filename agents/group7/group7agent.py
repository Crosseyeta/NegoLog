from typing import Union
import nenv
from nenv import Action, Bid , Offer
from .opponent_model import OpponentModel  # Import opponent model

class Group7Agent(nenv.AbstractAgent):
    def __init__(self, preference, session_time, estimators):
        super().__init__(preference, session_time, estimators)
        self.opponent_model = OpponentModel()  # Initialize your opponent model
        self.last_received_bids = []   
        self.reservation_value = 0.4;

    @property
    def name(self) -> str:
        return "Group7"

    def initiate(self, opponent_name):
        # Initialize any additional variables here
        self.reservation_value = self.preference.reservation_value

    ## this agent uses these modeling
    #Bidding strategy = 
    #Opponent modeling =  Bayesian opponent modeling to make it fair.
    #Acceptance strategy = Depending on time sensitivity and also nash utility.As given in the below
    #

    def receive_offer(self, bid: Bid, t: float):
        # Update the opponent model with the received bid
        print(f"Received Bid: {bid}, Time: {t}")
        self.last_received_bids.append(bid)
        self.opponent_model.update_model(bid)
        

    def act(self, t: float) -> Action:
        # Reduce target utility over time
        target_utility = max(self.preference.reservation_value, 1 - t)

        if self.can_accept(target_utility):
            print(f"Accepted Opponent Bid: {self.last_received_bids[-1]}")
            return self.accept_action

        # Generate bid based on updated target utility
        bid = self.generate_bid(target_utility)
        print(f"Generated Bid: {bid}, Utility: {self.preference.get_utility(bid)}")

        return Offer(Action(bid))

    def calculate_nash_utility(self) -> float:
        #To calcualte nas utility for use in the acceptance strategy

        total_nash_utility = 0
        for bid in self.preference.bids:  # Use self.preference.bids instead of get_all_bids()
            agent_utility = self.preference.get_utility(bid)
            opponent_utility = self.opponent_model.evaluate_bid(bid)
            product_utility = agent_utility * opponent_utility
            total_nash_utility = max(total_nash_utility, product_utility)
        return total_nash_utility
        ## With this approache we can decide for the fairest decision


    def can_accept(self, target_utility: float) -> bool:
        ### Comparing the next bid with time sentivity considering
        ### Nash utility calculated 
        if len(self.last_received_bids) == 0:
            return False  #  This part is coming from abstract class.If there is no bid recevied return false

        
        last_bid_utility = self.preference.get_utility(self.last_received_bids[-1])

        # next potential bid from bidding strategy
        next_bid = self.generate_bid(target_utility)
        next_bid_utility = self.preference.get_utility(next_bid)

        # Get Nash utility (calculated based on our preferences and opponent model)
        nash_utility = self.calculate_nash_utility()

        # Early in negotiation: Require the opponent's offer to exceed the next bid
        if last_bid_utility >= next_bid_utility and last_bid_utility >= nash_utility:
            return True

        # Close to the deadline: Relax requirements to avoid negotiation failure
        if target_utility <= self.reservation_value:
            return last_bid_utility >= self.reservation_value

        return False
    

    def generate_bid(self, target_utility: float) -> Bid:
        best_bid = None
        max_score = -1
        for bid in self.preference.bids:
            your_utility = self.preference.get_utility(bid)
            opponent_utility = self.opponent_model.evaluate_bid(bid)

            # Filter bids based on target utility
            if your_utility >= target_utility:
                # Score formula combining agent and opponent utilities
                score = 0.6 * your_utility + 0.4 * opponent_utility  # Adjust weights as needed
                if score > max_score:
                    best_bid = bid
                    max_score = score

        return best_bid or self.preference.bids[-1]  # Fallback to the lowest utility bid
