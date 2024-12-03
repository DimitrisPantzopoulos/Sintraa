import torch
import torch.nn as nn

class Greta(nn.Module):
    def __init__(self):
        super().__init__()

        self.FoodWastageConsultant = nn.Sequential(
            nn.Linear(3, 16),
            nn.LeakyReLU(negative_slope=0.01),
            nn.Linear(16, 8),
            nn.ReLU(),
            nn.Linear(8, 4)
        )
        
    def forward(self, x):
        x = self.FoodWastageConsultant(x)
        return x

    def predict(self, x):
        return torch.argmax(self.FoodWastageConsultant(x))

import torch
import torch.nn as nn

class Stephen(nn.Module):
    def __init__(self):
        super().__init__()

        self.FinanceConsultant = nn.Sequential(
            nn.Linear(5, 16),
            nn.LeakyReLU(negative_slope=0.01),
            nn.Linear(16, 8),
            nn.ReLU(),
            nn.Linear(8, 4)
        )

        self.StephenDict  = {0 : 1,    1 : 0.5,  2 : -0.5,  3 : -1}
        self.PriceChanges = {0 : 0.10, 1 : 0.05, 2 : -0.05, 3 : -0.10}
        
    def forward(self, x):
        x = self.FinanceConsultant(x)
        return x
    
    def predict(self, x):
        return torch.argmax(self.FinanceConsultant(x))
    