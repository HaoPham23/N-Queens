from n_queens import NQueens
import time

size = int(input("Input size: "))

nqueens = NQueens(size)

alg = input("Input algorithm: dfs/bfs/hill_climbing/queen_search2: ")
# alg = 'queen_search2'
start_time = time.time()
nqueens.find_solution(alg)
end_time = time.time()
print(f"[+] Total running time of {alg.upper()} algorithm for n = {size}: {end_time - start_time} (s)")
# nqueens.print_board()