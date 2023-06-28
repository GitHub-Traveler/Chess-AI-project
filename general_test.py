import chess

def evaluation(self, color):
    self.perf += 1
    result = self.engine.analyse(self.board, chess.engine.Limit(depth=0))
    
    return int(result['score'].white().score(mate_score=10000000))