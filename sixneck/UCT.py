class connect6State:
    def __init__(self):

class Node:
    def __init__(self, move = None, parent = None, state = None):
        self.move = move
        self.parentNode = parent
        self.childNodes = []
        self.wins = 0
        self.visits = 0
        self.untriedMoves = state.GetMoves
        self.color = player.color

    def UCTSelectChild(self):
        s = sorted(self.childNodes, key = lambda c: c.wins/c.visits + sqrt(2*log(self.visits)/c.visits))[-1]
        return s
    
    def AddChild(self, m, s):
        n = Node(move=m, parent=self, state=s)
        self.untriedMoves.remove(m)
        self.childNodes.append(n)
        return n
    
    def Update(self, result):
        self.visits += 1
        self.wins += results

def UCT(rootstate, iteration_max):
    rootnode = Node(state = rootstate)

    for i in range(iteration_max):
        node = rootnode
        state = node.Clone()

        #Select
        while node.untriedMoves == [] and node.childNodes != []:
            node = node.UCTSelectChild()
            state.DoMove(node.move)
        
        #Expand
        if node.untriedMoves != []:
            m = random.choice(node.untriedMoves)
            state.DoMove(m)
            node = node.AddChild(m, state)
        
        #Rollout
        while state.GetMoves() != []:
            state.DoMove(random.choice(state.GetMoves()))
        
        #Backpropagate
        while node != None:
            node.Update(state.GetResult(node.playerJustMoved))
            node = node.parentNode