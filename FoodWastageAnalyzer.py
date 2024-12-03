import torch

from Models import Greta, Stephen

class Analyzer():
    def __init__(self):
        self.Greta = Greta()
        self.Stephen = Stephen()

        # Load pre-trained weights for models
        self.Greta.load_state_dict(torch.load("TrainedModels/Greta.pth", weights_only=True))
        self.Stephen.load_state_dict(torch.load("TrainedModels/Stephen.pth", weights_only=True))

        # Set models to evaluation mode
        self.Greta.eval()
        self.Stephen.eval()

    def AnalyzeItem(self, x):
        # Extract Greta's input data
        GretaData = torch.tensor(x[0:3], dtype=torch.float32)

        # Get Greta's opinion
        GOpinion = self.Greta.predict(GretaData).item()

        # For Greta:
        # 0: No Changes
        # 1: Reduce Plate Size
        # 2: Reduce Plate Size and Stock
        # 3: Remove from Menu

        # Extract the original price
        OriginalPrice = x[3]

        # Get Stephen's opinion on price adjustment
        # For Stephen:
        # 0: +10% price increase
        # 1: +5% price increase
        # 2: -5% price decrease
        # 3: -10% price decrease
        SOpinion = self.Stephen.predict(torch.tensor(x, dtype=torch.float32)).item()

        # Calculate the adjusted price based on Stephen's opinion
        if SOpinion == 0:
            AdjustedPrice = round(OriginalPrice * 1.10, 2)
        elif SOpinion == 1:
            AdjustedPrice = round(OriginalPrice * 1.05, 2)
        elif SOpinion == 2:
            AdjustedPrice = round(OriginalPrice * 0.95, 2)
        elif SOpinion == 3:
            AdjustedPrice = round(OriginalPrice * 0.90, 2)
        else:
            AdjustedPrice = OriginalPrice

        # Determine Greta's action
        if GOpinion == 0:
            GretaAction = "No changes"
        elif GOpinion == 1:
            GretaAction = "Reduce plate size"
        elif GOpinion == 2:
            GretaAction = "Reduce plate size and stock"
        elif GOpinion == 3:
            GretaAction = "Major changes needed"
        else:
            GretaAction = "Unknown recommendation"

        # Handle conflict: if Stephen suggests a price decrease
        if AdjustedPrice < OriginalPrice and GOpinion > 0:
            GretaAction = "Reduce plate size (stock unchanged due to price reduction)"
            return {
                "Action": "Adjust price and plate size",
                "AdjustedPrice": AdjustedPrice,
                "GretaAction": GretaAction,
                "StephenAction": f"Price adjusted by {AdjustedPrice - OriginalPrice:.2f}",
            }

        return {
            "Action": "Adjust price and/or stock",
            "AdjustedPrice": AdjustedPrice,
            "GretaAction": GretaAction,
            "StephenAction": f"Price adjusted by {AdjustedPrice - OriginalPrice:.2f}",
        }