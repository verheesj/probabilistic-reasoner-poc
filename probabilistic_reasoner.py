class KnowledgeBase:
    """ A simple knowledge base that stores facts and their probabilities """
    def __init__(self):
        self.facts = dict()
        self.facts_lifetime = {}

    def tell(self, new_fact, new_probability):
        """ Add a fact to the knowledge base """
        # Add a fact to the knowledge base
        self.facts[new_fact] = new_probability

    def tell_lifetime(self, fact, value, start_time, end_time):
        # Store a fact with a specified lifetime
        self.facts_lifetime[fact] = (value, start_time, end_time)

    def ask_alive(self, fact, time):
        # Retrieve a fact that's still "alive" at a given time
        if fact in self.facts_lifetime:
            value, start_time, end_time = self.facts_lifetime[fact]
            if start_time <= time <= end_time:
                return value
        return "Fact not found or not alive"
    
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

    def infer_before(self, a, b, time):
        """ Infer a fact from the knowledge base using a temporal relationship """
        # If "A before B" is true, and it's after the end time of A and before the end time of B, infer B
        a_lifetime = self.kb.ask_alive(a)
        b_lifetime = self.kb.ask_alive(b)
        if a_lifetime != "Fact not found or not alive" and b_lifetime != "Fact not found or not alive":
            _, _, a_end = a_lifetime
            _, _, b_end = b_lifetime
            if a_end < time < b_end:
                self.kb.tell(b, 1)
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

    def handle_biconditional(self, a, b):
        # If "A iff B" is true, infer "A => B" and "B => A" are true
        biconditional_prob = self.kb.ask(f"{a} iff {b}")
        if biconditional_prob != "Fact not found" and biconditional_prob > 0.5:
            self.kb.tell(f"{a} implies {b}", 1)
            self.kb.tell(f"{b} implies {a}", 1)
            return True
        return False

    def handle_contradiction(self, a):
        # If "A" is true, then "not A" is false
        a_prob = self.kb.ask(a)
        if a_prob != "Fact not found" and a_prob > 0.5:
            self.kb.tell(f"not {a}", 0)
            return True
        return False

    def bayesian_update(self, fact, evidence, prior, likelihood):
        # Use Bayes' theorem to update the probability of a fact given some evidence
        # P(A|B) = P(B|A)*P(A) / P(B)
        evidence_prob = self.kb.ask(evidence)
        if evidence_prob == "Fact not found":
            print(f"No information about {evidence}")
            return False

        posterior = (likelihood * prior) / evidence_prob
        self.kb.tell(fact, posterior)
        return True

    def deductive_reasoning(self, a, b=None, c=None):
        # Try all forms of deduction on a
        if self.modus_ponens(a, b):
            return True
        if self.disjunctive_syllogism(a, b):
            return True
        if self.infer_implication_chain(a, b, c):
            return True
        if self.hypothetical_syllogism(a, b, c):
            return True
        if self.handle_biconditional(a, b):
            return True
        if self.handle_contradiction(a):
            return True
        return False

    def inductive_reasoning(self, a):
        # If "A" is true in several specific instances, infer "A" is generally true
        instances_true = 0
        total_instances = 0
        for instance in self.kb.facts:
            if a in instance:
                total_instances += 1
                if self.kb.ask(instance) > 0.5:
                    instances_true += 1
        if total_instances > 0 and instances_true / total_instances > 0.5:
            self.kb.tell(a, 1)
            return True
        return False

    def abductive_reasoning(self, a, b):
        # If "A => B" is true and "B" is true, infer "A" is plausible
        b_prob = self.kb.ask(b)
        implies_prob = self.kb.ask(f"{a} implies {b}")
        if b_prob != "Fact not found" and implies_prob != "Fact not found" and b_prob > 0.5 and implies_prob > 0.5:
            self.kb.tell(a, 0.5)  # Set to 0.5 as it's only a plausible explanation
            return True
        return False


# Initialize KnowledgeBase and Reasoner
kb = KnowledgeBase()
reasoner = ProbabilisticReasoner(kb)

# Add facts with lifetimes to KnowledgeBase
kb.tell_lifetime("rain", 1, 0, 10)
kb.tell_lifetime("wet ground", 1, 5, 15)

# Use temporal reasoning
reasoner.infer_before("rain", "wet ground", 12)

# The fact 'wet ground' should now be inferred in the KnowledgeBase
print(kb.ask("wet ground"))
