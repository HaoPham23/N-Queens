from n_queens import NQueens
import time
def main():
    size = int(input("[+] Enter the size of chessboard: "))
    alg_num = int(input(
    """
[+] Enter the algorithm: 

    1. DFS (n <= 25)
    2. BFS (n <= 15)
    3. Hill Climbing
    4. Queen Search 2 (QS2)
    5. Explicit

[+] Your option number: """))

    alg_options = ['dfs', 'bfs', 'hill_climbing', 'queen_search2', 'explicit']
    if alg_num < 1 or alg_num > len(alg_options):
        print('[!] Please choose a valid option!')
        return
    alg = alg_options[alg_num - 1]    
    nqueens = NQueens(size)
    start_time = time.time()
    nqueens.find_solution(alg)
    end_time = time.time()
    print(f"[+] Total running time of {alg.upper()} algorithm for n = {size}: {end_time - start_time} (s)")
    isVerify = input("[+] Verify the solution? (y/n): ")
    if isVerify.lower() == 'y':
        print(nqueens.is_valid(nqueens.queen))
    isPrint = input('[+] Print the chessboard? (y/n): ')
    if isPrint.lower() == 'y':
        nqueens.print_board()
    
if __name__ == "__main__":
    main()