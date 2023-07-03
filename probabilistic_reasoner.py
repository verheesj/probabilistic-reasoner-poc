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
        
    def infer_rule(self, a, b):
        """ Infer a fact from the knowledge base using a rule """

        # If we know "A => B" and "A is True", then we can infer "B is True"

        a_prob = self.kb.ask(a)

        if a_prob != "Fact not found" and a_prob > 0.5:  # Let's say A is True if its probability > 0.5
            self.kb.tell(b, 1)  # Infer B is True and add to the knowledge base
            return True
    
        return False


    def resolve_ambiguity(self, fact):
        """ Resolve ambiguity in a fact """
        # If fact exists in knowledge base, no ambiguity
        if self.kb.ask(fact) != "Fact not found":
            return fact
        
        # If fact doesn't exist, check its opposite
        opposite_fact = 'not ' + fact if 'not ' not in fact else fact.replace('not ', '')
        if self.kb.ask(opposite_fact) != "Fact not found":
            return opposite_fact

        return "Fact not found"




# Initialize KnowledgeBase and Reasoner
kb = KnowledgeBase()
reasoner = ProbabilisticReasoner(kb)

# Adding facts to the KnowledgeBase
kb.tell("rain", 0.6)
kb.tell("not rain", 0.4)
kb.tell("umbrella if rain", 1)

# Infer new facts
success = reasoner.infer_rule("rain", "umbrella")
if success:
    print("New fact inferred: 'umbrella'")
