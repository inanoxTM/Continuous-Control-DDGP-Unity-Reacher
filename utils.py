import torch


TARGET_SCORE = 30
SINGLE_AGENT = False
BUFFER_SIZE = int(1e6)  
GAMMA = 0.99            
TAU = 1e-3              
EPSILON = 1.0           
EPSILON_DECAY = 1e-6    
n_episodes=1000         
max_t=10000
OU_SIGMA = 0.2          
OU_THETA = 0.15         
BATCH_SIZE = 164       
LR_ACTOR = 5e-4         
LR_CRITIC = 6e-4        
LR_DECAY = True
LR_DECAY_STEP = 1
LR_DECAY_GAMMA = 0.8
WEIGHT_DECAY = 0 
OPTIMIZER = "RMSPROP"
UPDATE_EVERY = 40       
NUM_EPOCHS = 10          
device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")