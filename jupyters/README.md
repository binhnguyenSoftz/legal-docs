# Notebook thử nghiệm

Notebook chạy thử model và đánh giá nhanh. Kết quả chính thức vẫn ghi vào tài liệu `docs/`.

| Notebook | Nội dung |
|---|---|
| `paddleocr-eval.ipynb` | Chạy PaddleOCR lên golden set tổng hợp. Biểu đồ các hệ số tương thích model – dữ liệu: CER, WER, Field Accuracy, Document Accuracy, CER bỏ dấu, detection recall, độ suy giảm theo nhiễu, hiệu chỉnh điểm tự tin (ECE), tốc độ. Thống kê ký tự hay sai |

## Cài đặt

PaddlePaddle mới có wheel tới Python 3.13, nên tạo venv 3.13 bằng `uv`:

```bash
cd jupyters
uv venv .venv --python 3.13
uv pip install --python .venv/bin/python -r requirements.txt --index-strategy unsafe-best-match
.venv/bin/jupyter lab
```

## Dữ liệu

Notebook đọc thư mục `data/` cạnh notebook (đường dẫn tương đối), là thư mục `generated/` của generator. Notebook quét đệ quy và chỉ lấy ảnh đúng tên generator sinh ra:

- `<doc-id>_p<N>.png`: trang bản sạch
- `<doc-id>_p<N>_<light|medium|heavy>.jpg`: trang đã thêm nhiễu

Ảnh debug `*_bbox.jpg`, `.pdf`, `.html` bị bỏ qua. Ground truth lấy từ `ground_truth.json` cùng thư mục hồ sơ.

- **Local:** trỏ `data` tới kết quả của generator (sinh dữ liệu theo README của generator):

  ```bash
  cd jupyters && ln -s ../src/data-golden-set-generator/generated data
  ```

- **Colab:** upload notebook, nén thư mục `generated/` thành zip rồi giải nén thành `/content/data`, chọn runtime GPU. Cell đầu tiên tự cài `paddlepaddle-gpu` và `paddleocr` khi chạy trên Colab.

## Lưu ý

- Chạy CPU phải tắt oneDNN (`enable_mkldnn=False`), nếu không model PP-OCRv6 báo lỗi `ConvertPirAttribute2RuntimeAttribute`.
- Trên CPU mất khoảng 25 giây/trang cho mỗi model, nên mặc định `MAX_IMAGES = 24`. Kết quả OCR được cache ở `outputs/` (không commit), chạy lại notebook không phải OCR lại.
