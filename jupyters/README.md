# Notebook thử nghiệm

Notebook chạy thử model và đánh giá nhanh. Kết quả chính thức vẫn ghi vào tài liệu `docs/`.

`ocr-eval.ipynb` chạy PaddleOCR, VietOCR và Tesseract lên golden set tổng hợp, chấm cùng một cách rồi so trên cùng bảng và biểu đồ: CER, WER, Field Accuracy, Document Accuracy, CER bỏ dấu, detection recall, độ suy giảm theo nhiễu, hiệu chỉnh điểm tự tin (ECE), tốc độ, ký tự hay sai.

Chọn model trong `MODELS` (dạng `<engine>/<model>`), bỏ dòng nào thì không chạy model đó. Engine nào không có trong danh sách thì không cần cài. PaddleOCR và VietOCR dùng chung detection `PP-OCRv6_medium_det` với cùng `DET_PARAMS`, nên chênh lệch giữa hai engine là do phần đọc.

`dataset-profile.ipynb` mô tả golden set theo cách các bài báo về bộ dữ liệu OCR thường trình bày: bảng quy mô, phân bố lớp và biến thể, ma trận thuộc tính (loại giấy tờ × đặc điểm), ảnh mẫu, thống kê ảnh/văn bản/bố cục, lược đồ nhãn, t-SNE embedding ảnh, benchmark theo loại. Hình và bảng lưu ở `outputs/dataset-profile/`. Phần benchmark đọc `outputs/scores_*.csv` do `ocr-eval.ipynb` ghi, nên chạy `ocr-eval.ipynb` trước (đặt `MAX_IMAGES = None` để phủ đủ 7 loại). Phần embedding cần `torch`, `torchvision` như VietOCR.

`vlm-eval.ipynb` cho VLM đọc cùng golden set: Vintern-1B (fine-tune tiếng Việt), PaddleOCR-VL, Qwen3-VL, Qwen2.5-VL, Gemma 3. Có hai chế độ: đọc cả trang, và đọc vùng cắt theo bbox (rec-only, ứng với cascade OCR → VLM của AIP-035). Chấm các chỉ số như `ocr-eval.ipynb`, thêm tỷ lệ lặp tới hết token và tỷ lệ đọc thừa. Nếu có `outputs/scores_rec.csv` thì so rec-only với OCR chuyên dụng và tính số trường VLM đọc lại đúng khi OCR sai. Model chạy bằng `transformers` (engine `hf`, `vintern`), hoặc qua server vLLM tương thích OpenAI (engine `vllm`, đặt `VLLM_URL`). Trên CPU mỗi trang mất vài phút với model 2–4B, nên mặc định `MAX_IMAGES = 6`; chạy đầy đủ nên dùng GPU (Colab).

## Cài đặt

PaddlePaddle mới có wheel tới Python 3.13, nên tạo venv 3.13 bằng `uv`:

```bash
cd jupyters
uv venv .venv --python 3.13
uv pip install --python .venv/bin/python -r requirements.txt --index-strategy unsafe-best-match
.venv/bin/jupyter lab
```

Tesseract là chương trình ngoài, cần cài thêm (khoảng 1–2 giây/trang trên CPU):

```bash
sudo apt install tesseract-ocr tesseract-ocr-vie
```

Notebook tự tải `vie.traineddata` của `tessdata_best` vào `models/` (không commit).

VietOCR cần PyTorch. Cài `vietocr` với `--no-deps`: gói này ghim `pillow` cũ và kéo `opencv-python` đè lên bản PaddleOCR đang dùng, trong khi các gói đó chỉ cần khi train:

```bash
uv pip install --python .venv/bin/python torch torchvision --index-url https://download.pytorch.org/whl/cpu
uv pip install --python .venv/bin/python --no-deps vietocr==0.3.13
```

Tên miền `vocr.vn` mà VietOCR dùng để tải config và trọng số đã ngừng hoạt động. Notebook tự tải từ GitHub về `models/vietocr/` (khoảng 240MB, không commit).

`vlm-eval.ipynb` cần thêm `transformers`, `accelerate`, `timm` (đã có trong `requirements.txt`) và PyTorch như VietOCR. Trọng số tải từ Hugging Face vào cache `~/.cache/huggingface` (bf16 khoảng 2GB mỗi tỷ tham số). Gemma 3 là model gated: chấp nhận license trên Hugging Face rồi đặt `HF_TOKEN`.

## Dữ liệu

Notebook đọc thư mục `data/` cạnh notebook (đường dẫn tương đối), là thư mục `generated/` của generator. Notebook quét đệ quy và chỉ lấy ảnh đúng tên generator sinh ra:

- `<doc-id>_p<N>.png`: trang bản sạch
- `<doc-id>_p<N>_<light|medium|heavy>.jpg`: trang đã thêm nhiễu

Ảnh debug `*_bbox.jpg`, `.pdf`, `.html` bị bỏ qua. Ground truth lấy từ `ground_truth.json` cùng thư mục hồ sơ.

- **Local:** trỏ `data` tới kết quả của generator (sinh dữ liệu theo README của generator):

  ```bash
  cd jupyters && ln -s ../src/data-golden-set-generator/generated data
  ```

- **Colab:** nén phần bên trong `generated/` (để đường dẫn ảnh giống local), upload notebook và file zip, chọn runtime GPU. Cell đầu tiên tự cài Tesseract, `paddlepaddle-gpu`, `paddleocr`, `vietocr`:

  ```bash
  cd src/data-golden-set-generator/generated && python3 -m zipfile -c ../../../generated.zip 42
  ```

  Upload `generated.zip` vào `/content`, notebook tự giải nén vào `data/`. Thư mục `outputs/` mất khi hết phiên, tải về nếu cần giữ cache.

## Lưu ý

- Chạy CPU phải tắt oneDNN (`enable_mkldnn=False`), nếu không model PP-OCRv6 báo lỗi `ConvertPirAttribute2RuntimeAttribute`.
- Trên CPU mỗi ảnh mất khoảng 25 giây với mỗi model PaddleOCR, 10 giây với VietOCR, vài giây với Tesseract, nên mặc định `MAX_IMAGES = 24`. Kết quả OCR được cache ở `outputs/<engine>/<model>/` (không commit), chạy lại không phải OCR lại. Thêm model mới chỉ phải chạy model đó.
