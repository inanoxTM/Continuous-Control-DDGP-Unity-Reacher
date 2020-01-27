import numpy as np

import torch
import torch.nn as nn
import torch.nn.functional as F


def hidden_init(layer):
    fan_in = layer.weight.data.size()[0]
    lim = 1. / np.sqrt(fan_in)
    return (-lim, lim)

class Actor(nn.Module):
  
    def __init__(self, state_size, action_size, seed = 1, hidden_layers = [164,128]):
        """Initialize parameters and build model.
        Params
        ======
            state_size (int): Dimension of each state
            action_size (int): Dimension of each action
            seed (int): Random seed
            fc1_units (int): Number of nodes in first hidden layer
            fc2_units (int): Number of nodes in second hidden layer
        """
        super(Actor, self).__init__()
        self.seed = torch.manual_seed(seed)

        self.batchnorm_input = nn.BatchNorm1d(state_size)
        self.batchnorm_layers = nn.ModuleList([nn.BatchNorm1d(hidden_layers[0])])
        self.batchnorm_layers.extend([nn.BatchNorm1d(layer) for layer in hidden_layers[1:]])

        self.hidden_layers = nn.ModuleList([nn.Linear(state_size, hidden_layers[0])])
        layer_sizes = zip(hidden_layers[:-1], hidden_layers[1:])

        self.hidden_layers.extend([nn.Linear(fc1_units,fc2_units) for fc1_units, fc2_units in layer_sizes])
        self.output = nn.Linear(hidden_layers[-1], action_size)

        self.reset_parameters()

        
    def reset_parameters(self):
        for layer in self.hidden_layers:
            layer.weight.data.uniform_(*hidden_init(layer))
        self.output.weight.data.uniform_(-3e-3, 3e-3)
        self.output.bias.data.uniform_(-3e-3, 3e-3)

    def forward(self, state):
        """Build an actor (policy) network that maps states -> actions."""
        state = self.batchnorm_input(state)
        for linear, batch in zip(self.hidden_layers, self.batchnorm_layers):
            state = F.relu(batch(linear(state)))
        return F.tanh(self.output(state))

class Critic(nn.Module):

    def __init__(self, state_size, action_size, seed = 1, hidden_layers = [164,128]):
        """Initialize parameters and build model.
        Params
        ======
            state_size (int): Dimension of each state
            action_size (int): Dimension of each action
            seed (int): Random seed
            fcs1_units (int): Number of nodes in the first hidden layer
            fc2_units (int): Number of nodes in the second hidden layer
        """
        super(Critic, self).__init__()
        self.seed = torch.manual_seed(seed)

        self.bn0 = nn.BatchNorm1d(state_size)
        self.bn1 = nn.BatchNorm1d(hidden_layers[0])
        self.fcs1 = nn.Linear(state_size, hidden_layers[0])
        self.fcs2 = nn.Linear(hidden_layers[0]+action_size, hidden_layers[1])
        self.fcs3 = nn.Linear(hidden_layers[1], 1)
        self.reset_parameters()


    def reset_parameters(self):
        self.fcs1.weight.data.uniform_(*hidden_init(self.fcs1))
        self.fcs2.weight.data.uniform_(*hidden_init(self.fcs2))
        self.fcs3.weight.data.uniform_(-3e-3, 3e-3)
        self.fcs3.bias.data.uniform_(-3e-3, 3e-3)  

    def forward(self, state, action):
        
        state = self.bn0(state)
        out_s = F.relu(self.bn1(self.fcs1(state)))
        out = torch.cat((out_s, action), dim=1)
        out = F.relu(self.fcs2(out))
        return self.fcs3(out)


