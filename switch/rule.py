class Rule:

    def __init__(self, output, conditions):
        '''
        Parameters
        ----------
        output: int
            the value to output if this rule evaluates to true
        conditions: list
            list of conditions
        '''
        self.output = output
        self.conditions = {}
        for condition in conditions:
            self.conditions[condition.name] = condition

    def evaluate(self, data):
        '''
        Parameters
        ----------
        data: dict
            dictionary from condition name to data for the condition to evaluate

        Returns
        -------
        bool
            whether all conditions evaluate to true
        '''
        for condition in self.conditions:
            if condition not in data:
                return False

            if not self.conditions[condition].evaluate(data[condition]):
                return False

        return True

    def get_output(self):
        '''
        Returns
        -------
        int
            the value to output if this rule evaluates to true
        '''
        return self.output
        

class Condition:

    def __init__(self, name, operand, value):
        '''
        Parameters
        ----------
        name: str
            name of the condition
        operand: str
            one of =, <, >
        value:
            threshold constant
        '''
        self.name = name
        self.operand = operand
        self.value = value

    def evaluate(self, data):
        '''
        Parameters
        ----------
        data: int
            data to be evaluated against this condition
        
        Returns
        -------
        bool
            whether this condition evaluates to true
        '''
        if self.operand == '=':
            return data == self.value;
        elif self.operand == '>':
            return data > self.value;
        elif self.operand == '<':
            return data < self.value;
        else:
            return False