class KnowledgeBase:
    """ A simple knowledge base that stores facts and their probabilities """
    def __init__(self):
        self.facts = dict()

    def tell(self, new_fact, new_probability):
        """ Add a fact to the knowledge base """
        # Add a fact to the knowledge base
        self.facts[new_fact] = new_probability

    def ask(self, query):
        """ Query the knowledge base """
        # Query the knowledge base
        return self.facts.get(query, "Fact not found")


class ProbabilisticReasoner:
    """ A simple probabilistic reasoner that uses a knowledge base to infer facts """
    def __init__(self, knowledge_base):
        self.kb = knowledge_base

    def infer(self, query):
        """ Infer a fact from the knowledge base """

        prob = self.kb.ask(query)
        if prob != "Fact not found":
            truth_value = query in self.kb.facts
            return truth_value, prob
        return None, None



# Initialize KnowledgeBase and Reasoner
kb = KnowledgeBase()
reasoner = ProbabilisticReasoner(kb)

# Adding facts to the KnowledgeBase
kb.tell("rain", 0.6)
kb.tell("not rain", 0.4)

fact, probability = reasoner.infer("rain")
print(f"The fact '{fact}' has a probability of {probability}")