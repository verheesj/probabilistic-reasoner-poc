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
    
    def infer_conjunction(self, a, b):
        """ Infer a fact from the knowledge base using a conjunction """
        # If we know "A is True" and "B is True", then we can infer "A and B is True"
        a_prob = self.kb.ask(a)
        b_prob = self.kb.ask(b)
        if a_prob != "Fact not found" and b_prob != "Fact not found" and a_prob > 0.5 and b_prob > 0.5:
            self.kb.tell(f"{a} and {b}", 1)  # Infer "A and B is True" and add to the knowledge base
            return True
        return False

    def bayesian_inference(self, a, b, prior, likelihood):
        """ Infer a fact from the knowledge base using Bayesian inference """
        # Bayesian inference: P(A|B) = [P(B|A) * P(A)] / P(B)
        # Here we'll use "prior" as P(A), "likelihood" as P(B|A), and b_prob as P(B)
        b_prob = self.kb.ask(b)
        if b_prob != "Fact not found":
            posterior = (likelihood * prior) / b_prob
            self.kb.tell(f"{a} given {b}", posterior)
            return True
        return False

    def infer_disjunction(self, a, b):
        """ Infer a fact from the knowledge base using a disjunction """
        # If we know "A is True" or "B is True", then we can infer "A or B is True"
        a_prob = self.kb.ask(a)
        b_prob = self.kb.ask(b)
        if a_prob != "Fact not found" and a_prob > 0.5 or b_prob != "Fact not found" and b_prob > 0.5:
            self.kb.tell(f"{a} or {b}", 1)  # Infer "A or B is True" and add to the knowledge base
            return True
        return False

    def infer_negation(self, a):
        """ Infer a fact from the knowledge base using negation  """
        # If we know "A is True", then we can infer "not A is False"
        a_prob = self.kb.ask(a)
        if a_prob != "Fact not found" and a_prob > 0.5:
            self.kb.tell(f"not {a}", 0)  # Infer "not A is False" and add to the knowledge base
            return True
        return False

    def update_probability(self, fact, probability):
        """ Update the probability of a fact in the knowledge base """
        self.kb.tell(fact, probability)
    
    def modus_ponens(self, a, b):
        # If "A => B" is True and "A" is True, infer "B" is True
        a_prob = self.kb.ask(a)
        implies_prob = self.kb.ask(f"{a} implies {b}")
        if a_prob != "Fact not found" and implies_prob != "Fact not found" and a_prob > 0.5 and implies_prob > 0.5:
            self.kb.tell(b, 1)
            return True
        return False
    
    def disjunctive_syllogism(self, a, b):
        # If "A or B" is True and "A" is False, infer "B" is True
        or_prob = self.kb.ask(f"{a} or {b}")
        a_prob = self.kb.ask(a)
        if or_prob != "Fact not found" and a_prob != "Fact not found" and or_prob > 0.5 and a_prob <= 0.5:
            self.kb.tell(b, 1)
            return True
        return False

    def evaluate_expression(self, expression):
        # Split the expression into parts
        parts = expression.split(' ')
        
        # Evaluate each part
        for part in parts:
            if part != 'and' and part != 'or' and part != 'not':
                # If the part is a fact, replace it with its truth value
                prob = self.kb.ask(part)
                if prob != "Fact not found":
                    truth_value = True if prob > 0.5 else False
                    expression = expression.replace(part, str(truth_value))
        
        # Evaluate the resulting expression
        return eval(expression)

    def infer_implication_chain(self, a, b, c):
        # If "A => B" is true, "B => C" is true, and "A" is true, infer "C" is true.
        a_prob = self.kb.ask(a)
        implies_ab = self.kb.ask(f"{a} implies {b}")
        implies_bc = self.kb.ask(f"{b} implies {c}")
        if a_prob != "Fact not found" and implies_ab != "Fact not found" and implies_bc != "Fact not found" and a_prob > 0.5 and implies_ab > 0.5 and implies_bc > 0.5:
            self.kb.tell(c, 1)
            return True
        return False

    def hypothetical_syllogism(self, a, b, c):
        # If "A => B" is true and "B => C" is true, infer "A => C" is true
        implies_ab = self.kb.ask(f"{a} implies {b}")
        implies_bc = self.kb.ask(f"{b} implies {c}")
        if implies_ab != "Fact not found" and implies_bc != "Fact not found" and implies_ab > 0.5 and implies_bc > 0.5:
            self.kb.tell(f"{a} implies {c}", 1)
            return True
        return False

# Initialize KnowledgeBase and Reasoner
kb = KnowledgeBase()
reasoner = ProbabilisticReasoner(kb)

# Adding facts to the KnowledgeBase
kb.tell("rain", 0.6)
kb.tell("rain implies wet ground", 1)
kb.tell("wet ground implies umbrella", 1)

# Infer using implication chain
success = reasoner.infer_implication_chain("rain", "wet ground", "umbrella")
if success:
    print("New fact inferred: 'umbrella'")

# Infer using hypothetical syllogism
success = reasoner.hypothetical_syllogism("rain", "wet ground", "umbrella")
if success:
    print("New fact inferred: 'rain implies umbrella'")

