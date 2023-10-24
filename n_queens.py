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
        return True
    
    def _dfs(self):
        if self.size <= 3:
            return []
        stack = [[]]
        while stack:
            solution = stack.pop()
            n = len(solution)
            for col in range(self.size):
                new_state = solution.copy() # deep copy
                new_state.append(col)
                if self.is_valid(new_state):
                    if (len(new_state) == self.size):
                        self.queen = new_state
                        return
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
            for col in range(self.size):
                new_state = solution.copy() # deep copy
                new_state.append(col)
                if self.is_valid(new_state):
                    if (len(new_state) == self.size):
                        self.queen = new_state
                        return
                    queue.put(new_state)
        return

    def _queen_search2(self, c1 = 0.45, c2 = 32):
        """
        Based on the paper: Fast Search Algorithms for the N-Queens Problem
        """
        def swap_ok(i, j, queen, dn, dp):
            """
            Thử swap 2 con hậu hàng `i` và `j` với nhau. Nếu collision giảm thì return True.
            """  
            idx_dn = set([i + queen[i], j + queen[j], i + queen[j], j + queen[i]])
            idx_dp = set([i - queen[i], j - queen[j], i - queen[j], j - queen[i]])
            diff = 0 # diff = old_collision - new_collision
            for idx in idx_dn:
                if dn[idx] > 0:
                    diff += dn[idx] - 1
            for idx in idx_dp:
                if dp[idx - (1 - self.size)] > 0:
                    diff += dp[idx - (1 - self.size)] - 1
            # Swap
            dn[i + queen[i]] -= 1
            dn[j + queen[j]] -= 1
            dn[i + queen[j]] += 1
            dn[j + queen[i]] += 1
            dp[i - queen[i] - (1 - self.size)] -= 1
            dp[j - queen[j] - (1 - self.size)] -= 1
            dp[i - queen[j] - (1 - self.size)] += 1
            dp[j - queen[i] - (1 - self.size)] += 1
            for idx in idx_dn:
                if dn[idx] > 0:
                    diff -= dn[idx] - 1
            for idx in idx_dp:
                if dp[idx - (1 - self.size)] > 0:
                    diff -= dp[idx - (1 - self.size)] - 1

            # Undo swap
            dn[i + queen[i]] += 1
            dn[j + queen[j]] += 1
            dn[i + queen[j]] -= 1
            dn[j + queen[i]] -= 1
            dp[i - queen[i] - (1 - self.size)] += 1
            dp[j - queen[j] - (1 - self.size)] += 1
            dp[i - queen[j] - (1 - self.size)] -= 1
            dp[j - queen[i] - (1 - self.size)] -= 1
            if diff > 0:
                return True
            return False
        
        def perform_swap(i, j, queen, collisions, dn, dp):
            """
            Swap 2 con hậu ở hàng i và j, cập nhật lại `dn`, `dp` và `collision`
            """
            idx_dn = set([i + queen[i], j + queen[j], i + queen[j], j + queen[i]])
            idx_dp = set([i - queen[i], j - queen[j], i - queen[j], j - queen[i]])
            diff = 0
            for idx in idx_dn:
                if dn[idx] > 0:
                    diff += dn[idx] - 1
            for idx in idx_dp:
                if dp[idx - (1 - self.size)] > 0:
                    diff += dp[idx - (1 - self.size)] - 1
            # swap
            dn[i + queen[i]] -= 1
            dn[j + queen[j]] -= 1
            dn[i + queen[j]] += 1
            dn[j + queen[i]] += 1
            dp[i - queen[i] - (1 - self.size)] -= 1
            dp[j - queen[j] - (1 - self.size)] -= 1
            dp[i - queen[j] - (1 - self.size)] += 1
            dp[j - queen[i] - (1 - self.size)] += 1
            for idx in idx_dn:
                if dn[idx] > 0:
                    diff -= dn[idx] - 1
            for idx in idx_dp:
                if dp[idx - (1 - self.size)] > 0:
                    diff -= dp[idx - (1 - self.size)] - 1
            queen[i], queen[j] = queen[j], queen[i]
            collisions -= diff
            return collisions
        
        def compute_collisions(queen):
            """
            Lưu 2 mảng `dn` và `dp` lần lượt lưu trữ số lượng con hậu trong đường chéo negative và positive.
            """
            dn = [0] * (2*self.size - 2 + 1)
            dp = [0] * (2*self.size - 2 + 1)
            for row in range(len(queen)):
                col = queen[row]
                dn[row + col] += 1
                dp[row - col - (1 - self.size)] += 1
            collisions = sum([x-1 for x in dn if x > 0]) + sum([x-1 for x in dp if x > 0])
            return collisions, dn, dp
        
        def compute_attacks(queen, dn, dp):
            """
            Return an array containing all queens that are attacked.
            """
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
                if number_of_attacks == 0:
                    self.queen = queen
                    return
                for k in range(number_of_attacks):
                    i = attack[k]
                    j = random.choice(range(self.size))
                    if swap_ok(i, j, queen, dn, dp):
                        collisions = perform_swap(i, j, queen, collisions, dn, dp)
                        if collisions == 0:
                            self.queen = queen
                            return
                        if collisions < limit:
                            limit = c1 * collisions
                            number_of_attacks, attack = compute_attacks(queen, dn, dp)
                            break
                loopcount += number_of_attacks
    
    def is_valid(self, queens):
        """
        Return `True` if the target `state` doesn't have any two queens attacking each other.
        """
        if len(set(queens)) != len(queens):
            return False
        dn = [0] * (2*self.size - 1)
        dp = [0] * (2*self.size - 1)
        for row in range(len(queens)):
            col = queens[row]
            if dn[row + col] > 0 or dp[row - col - (1 - self.size)] > 0:
                return False
            dn[row + col] = 1
            dp[row - col - (1 - self.size)] = 1
        return True

    def print_board(self):
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