---
id: AIP-004
title: Phân loại và tách giấy tờ
group: AIG-02
kind: problem            # problem | method | concern | enabler
status: Draft            # Draft | Review | Approved | Deprecated
stage: Defined           # Defined | Exploring | Decided | In production
priority: Must           # Must | Should | Could
early_test: false        # true: nằm trong nhóm khó nhất, thử nghiệm sớm
owner: <Tên người phụ trách>
updated: 2026-09-29
---

# AIP-004 - Phân loại và tách giấy tờ

## 1. Định nghĩa

### 1.1. Phát biểu bài toán

Từ file scan hoặc ảnh nhiều trang, xác định ranh giới từng giấy tờ và loại của giấy tờ đó (CCCD, đơn, xác nhận, biên bản...), kể cả khi gặp loại giấy chưa có trong danh mục.

**Ví dụ:** file PDF 12 trang: trang 1-2 là đơn đề nghị, trang 3 là CCCD, trang 4-11 là giấy chứng nhận cũ, trang 12 là một giấy viết tay không có trong danh mục. Kết quả: 4 giấy tờ, giấy cuối gắn loại `unknown` để cán bộ xem thay vì ép thành loại gần nhất.

**Phạm vi:**

- Gồm: phân loại loại giấy tờ; tách ranh giới trong file nhiều trang; phát hiện loại chưa biết.
- Không gồm: đọc chữ (AIP-001), trích xuất trường (AIP-005).

### 1.2. Vị trí trong luồng

**Bước:** Phân loại, tách giấy tờ (nhóm [AIG-02](AIG-02-classification-splitting.md) - Phân loại và tách giấy tờ). Sơ đồ luồng xem [README](README.md).

- Dựa vào: [AIP-001](AIP-001-document-ocr.md) - Đọc bố cục và chữ tiếng Việt trên giấy tờ
- Được dùng bởi: [AIP-005](AIP-005-schema-extraction.md) - Trích xuất theo schema và sửa lỗi OCR; [AIP-012](AIP-012-missing-document-detection.md) - Phát hiện thiếu giấy tờ

### 1.3. Đầu vào và đầu ra

| | Nội dung | Ví dụ |
|---|---|---|
| Đầu vào | Ảnh các trang và text OCR (AIP-001) | File PDF 12 trang gồm 4 giấy tờ |
| Đầu ra | Danh sách giấy tờ, mỗi giấy tờ gồm các trang, loại và điểm tin cậy | `[{pages: [1,2], type: "đơn", score: 0,93}, {pages: [3], type: "CCCD", score: 0,97}]` |

### 1.4. Ràng buộc bắt buộc

Chưa có. Bổ sung khi đi sâu vào bài toán, đánh mã `AIP-004-R01`, `R02`...

### 1.5. Bài toán con

| Bài toán con | Mã cũ | Ưu tiên | Nội dung |
|---|---|---|---|
| Phân loại từng trang, từng giấy tờ | AIP-004 cũ | Must | Gán loại giấy tờ và điểm tin cậy |
| Phát hiện ranh giới giấy tờ | AIP-007 cũ | Should | Xác định trang bắt đầu, kết thúc một giấy tờ; phát hiện loại chưa biết |

Bản đầu tiên có thể giả định mỗi file là một giấy tờ, nên phần tách ranh giới để `Should`. `[CẦN XÁC NHẬN]` Nếu người dân thường nộp một file gồm nhiều giấy tờ, cần nâng phần này lên `Must`.

## 2. Vì sao khó

### 2.1. Thách thức

- Cần dùng cả ảnh và text, vì có loại giấy chỉ khác nhau ở tiêu đề hoặc bố cục.
- Loại giấy chưa từng thấy (open-set / out-of-distribution) không được ép vào loại đã biết.
- Giấy tờ nhiều trang có trang giữa không có tiêu đề.

### 2.2. Chi phí khi sai

- Phân loại sai thì chọn sai schema trích xuất và đếm sai giấy tờ còn thiếu.
- Tách sai thì dữ liệu của hai giấy tờ bị trộn, hoặc một giấy tờ bị tính là hai.

## 3. Đánh giá

| Chỉ số | Cách đo | Ngưỡng chấp nhận |
|---|---|---|
| Accuracy, F1 theo từng loại giấy | Trên golden set AIP-026 | `[CẦN XÁC NHẬN]` |
| Độ chính xác ranh giới | `[CẦN XÁC NHẬN]` | `[CẦN XÁC NHẬN]` |
| Tỉ lệ phát hiện đúng loại chưa biết | `[CẦN XÁC NHẬN]` | `[CẦN XÁC NHẬN]` |

## 4. Hướng tiếp cận và thử nghiệm

### 4.1. Hướng tiếp cận ứng viên

| Hướng | Ưu điểm | Nhược điểm |
|---|---|---|
| `[CẦN XÁC NHẬN]` Chưa khảo sát thêm | | |

### 4.2. Dữ liệu cần chuẩn bị

- Danh mục loại giấy tờ trong luồng.
- Ảnh có nhãn loại.
- File scan nhiều trang có nhãn ranh giới.
- Mẫu giấy tờ ngoài danh mục.

### 4.3. Nhật ký thử nghiệm

| Ngày | Thử nghiệm | Kết quả | Kết luận |
|---|---|---|---|
| | | | |

## 5. Câu hỏi còn mở

- [ ] Danh mục loại giấy tờ cần hỗ trợ ở giai đoạn đầu gồm những loại nào?
- [ ] Gặp loại giấy chưa biết thì xử lý thế nào: chuyển người hay bỏ qua?
- [ ] Người dân có nộp một file gồm nhiều giấy tờ không, hay mỗi giấy tờ một file?

## 6. Tài liệu tham chiếu

Quy tắc ghi: `standards/07-references.md`.

| Mã | Tài liệu | Chiều | Nội dung liên quan |
|---|---|---|---|
| `AIP-001` | [Đọc bố cục và chữ tiếng Việt trên giấy tờ](AIP-001-document-ocr.md) | Dựa vào | Dùng text OCR làm đặc trưng phân loại |
| `AIP-005` | [Trích xuất theo schema và sửa lỗi OCR](AIP-005-schema-extraction.md) | Được dùng bởi | Chọn schema theo loại giấy tờ |
| `AIP-012` | [Phát hiện thiếu giấy tờ](AIP-012-missing-document-detection.md) | Được dùng bởi | Đếm loại giấy tờ đã phân loại |

## 7. Lịch sử thay đổi

| Ngày | Người sửa | Nội dung | Đã rà tham chiếu |
|---|---|---|---|
| 2026-09-28 | <Tên> | Tạo mới, định nghĩa ban đầu từ danh sách bài toán AI của luồng | Không cần |
| 2026-09-29 | binhnguyenSoftz | Tổ chức lại: gộp AIP-006 cũ (phân loại) và AIP-007 cũ (tách ranh giới); nhóm `AIG-02`; viết lại phát biểu bài toán | Có |
