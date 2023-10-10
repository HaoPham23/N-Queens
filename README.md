## How to run

```sh
python3 main.py
```

## QS 2 Algorithm

Tóm tắt: QS2 là 1 thuật toán heuristic, tìm ra lời giải bằng cách định nghĩa 1 hàm (giống loss function) và cố gắng tối ưu nó (gần giống kỹ thuật gradient descent). Ở đây hàm loss function được định nghĩa là số cặp hậu đang đụng độ nhau trên bàn cờ (gọi là `collisions`). Tìm được trạng thái có `collisions = 0` đồng nghĩa với việc tìm ra lời giải bài toán.

Mô tả:

1. Khởi tạo: Chọn random 1 hoán vị từ 1 đến `N` và đặt các con hậu vào vị trí tương ứng, sau đó tính giá trị của hàm `collisions`. Các con hậu được đặt vào hoán vị của (1, 2,...,`N`) sẽ đảm bảo chúng không bị đụng độ bởi các con cùng hàng và cột. Quá trình tìm kiếm lời giải sẽ được tối ưu, do chỉ cần xử lí đụng độ trên các đường chéo.
2. Nếu `collisions = 0` thì tìm thấy lời giải.
3. Chọn ra 2 con hậu đang bị ai đó tấn công.
4. Thử hoán đổi hàng của chúng, nhưng vẫn giữ lại cột. Tức là ban đầu 2 hậu ở vị trí `(x, a)` và `(y, b)` thì sau khi hoán đổi sẽ là `(y, a)` và `(x, b)`.
5. Tính lại `collisions`. Nếu `collisions` giảm thì thực hiện hoán đổi, không thì giữ nguyên. 
6. Nếu `collisions = 0` thì kết thúc, không thì quay lại bước 2. 

## References
The Queen Search 2 (QS2) is based on this paper:

1. Sosic, Rok, and Jun Gu. "Fast search algorithms for the n-queens problem." IEEE Transactions on Systems, Man, and Cybernetics 21.6 (1991): 1572-1576.

Here is another fast algorithm (Min-conflict): 

2. https://medium.com/@pranav.putta22/solving-n-queens-for-1-million-queens-with-minconflict-62ef798556e0

An explicit solution, run in O(n), but not an AI algorithm:

3. https://dl.acm.org/doi/pdf/10.1145/122319.122322