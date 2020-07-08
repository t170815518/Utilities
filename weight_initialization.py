# From StackOverflow

# takes in a module and applies the specified weight initialization
def weights_init_normal(m):
'''Takes in a module and initializes all linear layers with weight
       values taken from a normal distribution.
       '''
    # for every Linear layer in a model
    if type(m) == nn.Linear:
        y = m.in_features
        # m.weight.data shoud be taken from a normal distribution
        m.weight.data.normal_(0.0, 1 / np.sqrt(y))
        # m.bias.data should be 0
        m.bias.data.fill_(0.01)
        
def weights_init_normal(m):
'''Takes in a module and initializes all linear layers with weight
       values taken from a normal distribution.'''
    # for every Linear layer in a model
    if type(m) == nn.Linear:
        n = m.in_features
        y = 1.0/np.sqrt(n)
        m.weight.data.uniform_(-y, y)
        m.bias.data.fill_(0.05)
