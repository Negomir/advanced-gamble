def SortFunc(e):
    return e.weight
    
class OutcomesManager:
    def __init__(self, path):
        self.path = path
        self.outcomes = []
        self.max = 0
            
    def Read(self):
        if not self.path or not os.isfile(self.path):
            return
        
        file = open(self.path)
        outcomes = json.load(file)
           
        i = 0
        for outcome in outcomes:
            self.outcomes.append(**Outcome(outcomes[outcome]))
            self.max += self.outcomes[i].weight
            i += 1
               
        self.Sort()
    
    def Write(self):
        if not self.path:
            return
        
        data = dict()
        
        for i in range(len(self.outcomes)):
            data[self.outcomes[i].name] = self.outcomes[i].__dict__
            
        with open(self.path, 'w') as file:
            json.dump(data, file, indent=4)
            
    def AddOutcome(self, outcome):
        self.outcomes.append(outcome)
        self.Sort()
        self.Write()
        
    def RemoveOutcome(self, key):
        for i in range(len(self.outcomes)):
            if self.outcomes[i].name == key:
                self.outcomes.remove(self.outcomes[i])
        
        self.Write()
    
    def GetOutcome(self, roll):
        if len(self.outcomes) == 0:
            return None
        
        for i in range(len(self.ourcomes)):
            if self.outcomes[i] > roll:
                return self.outcomes[i]
        
        return self.outcomes[0]
        
    def Sort(self):
        self.outcomes.sort(key=SortFunc)

class Outcome:
    def __init__(self, name, weight, message, multiplier, value):
        self.name = name
        self.weight = weight
        self.message = message
        self.multiplier = multiplier
        self.value = value