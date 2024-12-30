from agents.group7.group7agent import Group7Agent
from nenv import *
from nenv.Preference import Preference
from nenv.Bid import Bid
from nenv.Action import Action

def test_group7_agent():
    #Just for test purposes givind some random issues and values 
    # mock_preference = Preference({
    #     "issueA": {"valueA": 0.2, "valueB": 0.4, "valueC": 0.6, "valueD": 0.8, "valueE": 1.0},
    #     "issueB": {"valueA": 0.2, "valueB": 0.4, "valueC": 0.6, "valueD": 0.8, "valueE": 1.0},
    #     "issueC": {"valueA": 0.2, "valueB": 0.4, "valueC": 0.6, "valueD": 0.8, "valueE": 1.0}
    # })

    mock_preference = Preference("c:/Users/pc/Documents/GitHub/NegoLog/test_data/mock_preference.json")
    
    
    session_time = 100

    estimators = []

    agent = Group7Agent(mock_preference, session_time, estimators)

   # Same for the thing that we made for our preferences we are doing it for opponent as well

    opponent_bids = [
        {"issueA": "valueE", "issueB": "valueD", "issueC": "valueC"},
        {"issueA": "valueD", "issueB": "valueB", "issueC": "valueA"},
        {"issueA": "valueC", "issueB": "valueC", "issueC": "valueE"}
    ]

   
    print("Testing")
    agreement_reached = False
    for t, bid_dict in enumerate(opponent_bids):
        time = t / len(opponent_bids)  # Normalize time (0 to 1)
        bid = Bid(bid_dict)  # Create a Bid object
        print(f"\nTime: {time:.2f}, Opponent Bid: {bid_dict}")

        # Agent processes opponent's offer
        agent.receive_offer(bid, time)

        # Agent decides to accept or counteroffer
        action = agent.act(time)
        if isinstance(action, Accept):  # Check if the action is of type 'Accept'
            print("Agent Action: Accepted the Offer")
            agreement_reached = True
            break  # Stop negotiation as agreement is reached
        elif isinstance(action, Offer):  # Check if the action is of type 'Offer'
            # print("Agent Action (Offer):", str(action))
            print("")
        else:
            print("Agent Action: Unknown action type")
    if agreement_reached:
        print("\nAgreement Reached with Bid:", bid_dict)
    else:
        print("\nNo Agreement Reached")
# Run the test
if __name__ == "__main__":
    test_group7_agent()
