
from .catwalk import Catwalk
from ..parameter import BestOfMoves

class Best3FoM(Catwalk):
    def __init__(self, color):
        super().__init__(color)
        self.name = 'best3FoM'
   
    def retreiveAllMovesWithGivenColor(self, color):
        super().retreiveAllMovesWithGivenColor(color)
        allPossibleMoves = self.allPossibleMoves

        # Sort the moves based on the FoM property in descending order
        sorted_moves = sorted(allPossibleMoves, key=lambda move: move['fom'], reverse=True)
        
        # Select the top three moves
        top_three_moves = sorted_moves[:BestOfMoves]
        
        self.allPossibleMoves = top_three_moves
        return top_three_moves        
    