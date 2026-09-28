---
id: AIP-006
title: Grounding và chống bịa khi trích xuất
group: AIG-03
kind: problem            # problem | method | concern | enabler
status: Draft            # Draft | Review | Approved | Deprecated
stage: Defined           # Defined | Exploring | Decided | In production
priority: Must           # Must | Should | Could
early_test: false        # true: nằm trong nhóm khó nhất, thử nghiệm sớm
owner: <Tên người phụ trách>
updated: 2026-09-29
---

# AIP-006 - Grounding và chống bịa khi trích xuất

## 1. Định nghĩa

### 1.1. Phát biểu bài toán

Mỗi giá trị trích xuất phải chỉ ra được nó nằm ở đâu trên ảnh (trang, bounding box, đoạn chữ gốc). Giá trị không tìm được nguồn thì bị loại hoặc đánh dấu, không được đi tiếp. Nhờ vậy cán bộ bấm vào trường là thấy ngay chỗ trên ảnh, và bước sau biết giá trị nào do model tự bịa.

**Ví dụ:** trường `so_thua` = `125` trỏ tới trang 2, bbox `[412, 880, 468, 905]`, chữ gốc `Thửa số: 125`. Trường `dien_tich` = `98,5` nhưng không tìm thấy chuỗi nào gần giống trên ảnh, nên bị đánh dấu "không có nguồn".

**Phạm vi:**

- Gồm: gắn vị trí nguồn; phát hiện giá trị không có nguồn.
- Không gồm: trích xuất giá trị (AIP-005), trích dẫn pháp lý trong văn bản sinh ra (AIP-024).

### 1.2. Vị trí trong luồng

**Bước:** Trích xuất (nhóm [AIG-03](AIG-03-information-extraction.md) - Trích xuất thông tin có nguồn). Sơ đồ luồng xem [README](README.md).

- Dựa vào: [AIP-005](AIP-005-schema-extraction.md) - Trích xuất theo schema và sửa lỗi OCR; [AIP-001](AIP-001-document-ocr.md) - Đọc bố cục và chữ tiếng Việt trên giấy tờ
- Được dùng bởi: [AIP-010](AIP-010-conflict-vs-error.md) - Phân biệt mâu thuẫn thật với lỗi OCR/trích xuất

### 1.3. Đầu vào và đầu ra

| | Nội dung | Ví dụ |
|---|---|---|
| Đầu vào | Kết quả trích xuất (AIP-005), vùng bố cục (AIP-001) | Trường `ho_ten` |
| Đầu ra | Giá trị kèm vị trí nguồn | `{value: "...", page: 1, bbox: [...]}` |

### 1.4. Ràng buộc bắt buộc

| Mã | Ràng buộc | Lý do |
|---|---|---|
| AIP-006-R01 | Mỗi giá trị trích xuất phải gắn trang và bounding box nguồn. | Để người và code kiểm chứng được. |
| AIP-006-R02 | Giá trị không truy được vị trí nguồn thì coi là chưa kiểm chứng. | Không để giá trị bịa đi vào quyết định. |

## 2. Vì sao khó

### 2.1. Thách thức

- LLM có thể sinh giá trị không có trong tài liệu (hallucination).
- Nối giá trị LLM trả về với đúng vùng ảnh gốc.

### 2.2. Chi phí khi sai

Không có nguồn thì cán bộ không kiểm tra lại được, và không phân biệt được lỗi OCR với mâu thuẫn thật (AIP-010).

## 3. Đánh giá

| Chỉ số | Cách đo | Ngưỡng chấp nhận |
|---|---|---|
| Tỉ lệ giá trị có nguồn đúng | `[CẦN XÁC NHẬN]` | `[CẦN XÁC NHẬN]` |

## 4. Hướng tiếp cận và thử nghiệm

### 4.1. Hướng tiếp cận ứng viên

| Hướng | Ưu điểm | Nhược điểm |
|---|---|---|
| `[CẦN XÁC NHẬN]` Chưa khảo sát thêm | | |

### 4.2. Dữ liệu cần chuẩn bị

- Nhãn vị trí nguồn cho từng trường trong golden set.

### 4.3. Nhật ký thử nghiệm

| Ngày | Thử nghiệm | Kết quả | Kết luận |
|---|---|---|---|
| | | | |

## 5. Câu hỏi còn mở

Chưa có.

## 6. Tài liệu tham chiếu

Quy tắc ghi: `standards/07-references.md`.

| Mã | Tài liệu | Chiều | Nội dung liên quan |
|---|---|---|---|
| `AIP-005` | [Trích xuất theo schema và sửa lỗi OCR](AIP-005-schema-extraction.md) | Dựa vào | Gắn vị trí nguồn cho từng trường trích xuất |
| `AIP-001` | [Đọc bố cục và chữ tiếng Việt trên giấy tờ](AIP-001-document-ocr.md) | Dựa vào | Dùng bounding box từ phân tích bố cục |
| `AIP-010` | [Phân biệt mâu thuẫn thật với lỗi OCR/trích xuất](AIP-010-conflict-vs-error.md) | Được dùng bởi | Truy lại vùng ảnh nguồn khi hai giá trị lệch nhau |

## 7. Lịch sử thay đổi

| Ngày | Người sửa | Nội dung | Đã rà tham chiếu |
|---|---|---|---|
| 2026-09-28 | <Tên> | Tạo mới, định nghĩa ban đầu từ danh sách bài toán AI của luồng | Không cần |
| 2026-09-29 | binhnguyenSoftz | Tổ chức lại: đổi mã từ AIP-009 cũ; nhóm `AIG-03`, thêm `kind`; viết lại phát biểu bài toán | Có |
