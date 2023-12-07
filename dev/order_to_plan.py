### GOAL: Going from an order to a planner

import spacy

class OrderToFoods:
    def __init__(self):
        self.nlp = spacy.load("en_core_web_sm")
    def extract_food_items(self, text):
        doc = self.nlp(text)

        # Define a list of relevant POS (Part-of-Speech) tags for food items
        food_pos_tags = ["NOUN", "PROPN"]

        # Extract food items based on POS tags
        food_items = [token.text for token in doc if token.pos_ in food_pos_tags]

        return food_items

    def find_modifier(self, sentence):
        doc = self.nlp(sentence)

        neg_words = ["without", "no", "none", "hold"]

        for token in doc:
            if token.text.lower() in neg_words: 
                # Check if the word has a dependent (what it modifies)
                if token.dep_ == "prep" and token.head.dep_ == "ROOT":
                    # If it's a preposition modifying the root, find its dependent
                    modifier = [child.text for child in token.children]
                    return modifier
                elif token.dep_ == "advcl" and token.head.dep_ == "ROOT":
                    # If it's an adverbial clause modifying the root, find its dependent
                    modifier = [child.text for child in token.children]
                    return modifier
                elif token.dep_ == "neg":
                    # If it's a negation word, find its dependent
                    modifier = [child.text for child in token.children]
                    return modifier

        return set()
    def execute(self, order):
        return set(self.extract_food_items(order)) - set(self.find_modifier(order))

# food_opts = ["chicken", "sandwich"]

def get_order(food_opts):
    order = (input("What would you like to order? ")).lower()
    nlp = OrderToFoods()
    plan = []

    proposed_foods = nlp.execute(order)

    is_sandwich = "sandwich" in order
    for food in food_opts:
        if food in proposed_foods:
            plan.append(food)
    
    # if it is a sandwich, add the bread as well
    if is_sandwich:
        plan.insert(0, "bread")
        plan.insert(len(plan), "bread")

    return plan

# print(get_order())
