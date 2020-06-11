from mcts.nodes import MonteCarloTreeSearchNode


class MonteCarloTreeSearch:
    def __init__(self, node: MonteCarloTreeSearchNode):
        self.root = node

    def best_action(self, simulations_number=1000, que=None):
        for _ in range(0, simulations_number):
            v = self.tree_policy()
            reward = v.rollout()
            v.backpropagate(reward)
        # exploitation only
        for c in self.root.children:
            print(c.state.current_move, " = ", c.score)
        print()
        print(self.root.best_child(c_param=0.).state.current_move)
        best = self.root.best_child(c_param=0.)
        if que is not None:
            que.put(best)
        else:
            return best

    def tree_policy(self):
        current_node = self.root
        while not current_node.is_terminal_node():
            if not current_node.is_fully_expanded():
                return current_node.expand()
            else:
                current_node = current_node.best_child()
        return current_node