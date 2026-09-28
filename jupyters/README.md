# Notebook thử nghiệm

Notebook chạy thử model và đánh giá nhanh. Kết quả chính thức vẫn ghi vào tài liệu `docs/`.

| Notebook | Nội dung |
|---|---|
| `paddleocr-eval.ipynb` | Chạy PaddleOCR lên golden set tổng hợp, so CER theo mức nhiễu, chữ viết tay / chữ in, và ký tự hay sai |

## Cài đặt

PaddlePaddle mới có wheel tới Python 3.13, nên tạo venv 3.13 bằng `uv`:

```bash
cd jupyters
uv venv .venv --python 3.13
uv pip install --python .venv/bin/python -r requirements.txt --index-strategy unsafe-best-match
.venv/bin/jupyter lab
```

## Dữ liệu

Notebook đọc thư mục `data/` cạnh notebook (đường dẫn tương đối), quét đệ quy mọi ảnh, cấu trúc bên trong tùy ý. Ảnh nằm trong một `ground_truth.json` thì được chấm điểm, ảnh khác chỉ chạy OCR.

- **Local:** trỏ `data` tới kết quả của generator (sinh dữ liệu theo README của generator):

  ```bash
  cd jupyters && ln -s ../src/data-golden-set-generator/generated data
  ```

- **Colab:** upload notebook, giải nén dữ liệu vào `/content/data`, chọn runtime GPU. Cell đầu tiên tự cài `paddlepaddle-gpu` và `paddleocr` khi chạy trên Colab.

## Lưu ý

- Chạy CPU phải tắt oneDNN (`enable_mkldnn=False`), nếu không model PP-OCRv6 báo lỗi `ConvertPirAttribute2RuntimeAttribute`.
- Trên CPU mất khoảng 25 giây/trang cho mỗi model, nên mặc định `MAX_IMAGES = 24`. Kết quả OCR được cache ở `outputs/` (không commit), chạy lại notebook không phải OCR lại.
