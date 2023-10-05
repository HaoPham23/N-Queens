from queue import Queue
import random

class NQueens:
    def __init__(self, size):
        """
        `queen` is a 1D array. The i-th queen is placed on the board at row i and column `queen[i]`
        """
        self.size = size
        self.queen = []
    
    def reset_state(self):
        self.queen = []

    def find_solution(self, algorithm = 'dfs'):
        self.reset_state()
        match algorithm:
            case 'dfs':
                self._dfs()
            case 'bfs':
                self._bfs()
            case 'hill_climbing':
                pass
            case 'queen_search2':
                self._queen_search2()
            case _:
                print('[!] Unknown algorithm')
                return False
        assert self.is_safe(self.queen)
        return True
    
    def _dfs(self):
        if self.size <= 3:
            return []
        stack = [[]]
        while stack:
            solution = stack.pop()
            n = len(solution)
            if n == self.size:
                self.queen = solution
                return
            for col in range(self.size):
                new_state = solution.copy() # deep copy
                new_state.append(col)
                if self.is_safe(new_state):
                    stack.append(new_state)
        return

    def _bfs(self):
        if self.size <= 3:
            return []
        queue = Queue()
        queue.put([])
        while not queue.empty():
            solution = queue.get()
            n = len(solution)
            if n == self.size:
                self.queen = solution
                return
            for col in range(self.size):
                new_state = solution.copy() # deep copy
                new_state.append(col)
                if self.is_safe(new_state):
                    queue.put(new_state)
        return

    def _queen_search2(self, c1 = 0.45, c2 = 32):
        """
        Based on the paper: Fast Search Algorithms for the N-Queens Problem
        """
        def swap_ok(i, j, queen, collisions, dn, dp):  
            new_collisions = collisions
            if dn[i + queen[i]] == 1:
                new_collisions += 1
            if dn[j + queen[j]] == 1:
                new_collisions += 1
            if dp[i - queen[i] - (1 - self.size)] == 1:
                new_collisions += 1
            if dp[j - queen[j] - (1 - self.size)] == 1:
                new_collisions += 1
            if dn[i + queen[j]] == 0:
                new_collisions -= 1
            if dn[j + queen[i]] == 0:
                new_collisions -= 1
            if dp[i - queen[j] - (1 - self.size)] == 0:
                new_collisions -= 1
            if dp[j - queen[i] - (1 - self.size)] == 0:
                new_collisions -= 1
            if new_collisions < collisions:
                return True
            return False
        
        def perform_swap(i, j, queen, collisions, dn, dp):
            if dn[i + queen[i]] == 1:
                collisions += 1
            if dn[j + queen[j]] == 1:
                collisions += 1
            if dp[i - queen[i] - (1 - self.size)] == 1:
                collisions += 1
            if dp[j - queen[j] - (1 - self.size)] == 1:
                collisions += 1
            if dn[i + queen[j]] == 0:
                collisions -= 1
            if dn[j + queen[i]] == 0:
                collisions -= 1
            if dp[i - queen[j] - (1 - self.size)] == 0:
                collisions -= 1
            if dp[j - queen[i] - (1 - self.size)] == 0:
                collisions -= 1
            dn[i + queen[i]] -= 1
            dn[j + queen[j]] -= 1
            dn[i + queen[j]] += 1
            dn[j + queen[i]] += 1

            dp[i - queen[i] - (1 - self.size)] -= 1
            dp[j - queen[j] - (1 - self.size)] -= 1
            dp[i - queen[j] - (1 - self.size)] += 1
            dp[j - queen[i] - (1 - self.size)] += 1

            queen[i], queen[j] = queen[j], queen[i]
            return collisions
        
        def compute_collisions(queen):
            dn = [0] * (2*self.size - 2 + 1)
            dp = [0] * (2*self.size - 2 + 1)
            for row in range(len(queen)):
                col = queen[row]
                dn[row + col] += 1
                dp[row - col - (1 - self.size)] += 1
            collisions = 0
            for x in dn:
                if x > 0:
                    collisions += x - 1
            for x in dp:
                if x > 0:
                    collisions += x - 1
            return collisions, dn, dp
        
        def compute_attacks(queen, dn, dp):
            attack = []
            for row in range(len(queen)):
                col = queen[row]
                if dn[row + col] > 1 or dp[row - col - (1 - self.size)] > 1:
                    attack.append(row)
            return len(attack), attack
        
        collisions = -1
        while collisions != 0:
            # Generate a random permutation of queen[0] to queen[size-1]
            queen = list(range(self.size))
            random.shuffle(queen)
            collisions, dn, dp = compute_collisions(queen)
            limit = c1 * collisions
            number_of_attacks, attack = compute_attacks(queen, dn, dp)
            loopcount = 0
            while loopcount <= c2 * self.size:
                for k in range(number_of_attacks):
                    i = attack[k]
                    j = random.choice(range(self.size))
                    if swap_ok(i, j, queen, collisions, dn, dp):
                        collisions = perform_swap(i, j, queen, collisions, dn, dp)
                        if collisions == 0:
                            self.queen = queen
                            return
                        if collisions < limit:
                            limit = c1 * collisions
                            number_of_attacks, attack = compute_attacks(queen, dn, dp)
                            break
                loopcount += number_of_attacks

    def is_safe(self, state):
        """
        Return `True` if the target `state` doesn't have any two queens attacking each other.
        """
        for row1 in range(1, len(state)):
            col1 = state[row1]
            for row2 in range(row1):
                col2 = state[row2]
                if col1 == col2 or (row1 + col1 == row2 + col2) or (row1 - col1 == row2 - col2):
                    return False
        return True

    def print_board(self, queen = None):
        if len(self.queen) != self.size:
            print('[+] Please find a solution first!')
            return
        for i in range(self.size):
            print(' ---' * self.size)
            for j in range(self.size):
                if self.queen[i] == j:
                    p = 'Q'
                else:
                    p = ' '
                print('| %s ' % p, end='')
            print('|')
        print(' ---' * self.size)