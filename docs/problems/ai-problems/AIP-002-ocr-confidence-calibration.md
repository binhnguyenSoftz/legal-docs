---
id: AIP-002
title: Hiệu chỉnh độ tin cậy theo từng trường
group: AIG-01
kind: problem            # problem | method | concern | enabler
status: Draft            # Draft | Review | Approved | Deprecated
stage: Defined           # Defined | Exploring | Decided | In production
priority: Must           # Must | Should | Could
early_test: true         # true: nằm trong nhóm khó nhất, thử nghiệm sớm
owner: <Tên người phụ trách>
updated: 2026-09-29
---

# AIP-002 - Hiệu chỉnh độ tin cậy theo từng trường

## 1. Định nghĩa

### 1.1. Phát biểu bài toán

Chuyển điểm tin cậy thô của OCR/VLM thành xác suất đúng thật cho từng trường, để ngưỡng "tin được / phải chuyển người" có ý nghĩa. Điểm 0,8 phải nghĩa là khoảng 80% trường có điểm đó đọc đúng, trên từng loại trường và loại chữ.

**Ví dụ:** OCR cho ngày sinh viết tay điểm thô 0,95, nhưng đo trên golden set chỉ 80% trường như vậy đọc đúng. Sau hiệu chỉnh, trường đó có điểm 0,80, thấp hơn ngưỡng 0,9 nên được đánh dấu cần kiểm tra.

**Phạm vi:**

- Gồm: hiệu chỉnh theo loại trường (ngày, số, họ tên, địa chỉ) và loại chữ (in, viết tay).
- Không gồm: sinh điểm thô (AIP-001), lan truyền độ bất định sang kết luận (AIP-013).

### 1.2. Vị trí trong luồng

**Bước:** Đọc ảnh (nhóm [AIG-01](AIG-01-document-vision-ocr.md) - Đọc ảnh và OCR). Sơ đồ luồng xem [README](README.md).

- Dựa vào: [AIP-001](AIP-001-document-ocr.md) - Đọc bố cục và chữ tiếng Việt trên giấy tờ
- Được dùng bởi: [AIP-005](AIP-005-schema-extraction.md) - Trích xuất theo schema và sửa lỗi OCR; [AIP-010](AIP-010-conflict-vs-error.md) - Phân biệt mâu thuẫn thật với lỗi OCR/trích xuất; [AIP-013](AIP-013-uncertainty-propagation.md) - Ước lượng độ bất định lan truyền

### 1.3. Đầu vào và đầu ra

| | Nội dung | Ví dụ |
|---|---|---|
| Đầu vào | Kết quả OCR/VLM kèm điểm tin cậy thô | Trường ngày sinh, điểm thô 0,95 |
| Đầu ra | Điểm tin cậy đã hiệu chỉnh theo từng trường | Điểm 0,95 thô tương ứng xác suất đúng thực tế 0,80 |

### 1.4. Ràng buộc bắt buộc

Chưa có. Bổ sung khi đi sâu vào bài toán, đánh mã `AIP-002-R01`, `R02`...

## 2. Vì sao khó

### 2.1. Thách thức

- Điểm tin cậy của OCR/VLM thường không phản ánh đúng xác suất sai.
- Mức sai khác nhau theo loại trường (họ tên, ngày tháng, số giấy tờ), nên phải hiệu chỉnh theo từng trường.

### 2.2. Chi phí khi sai

Điểm quá cao thì lỗi OCR lọt qua, bị coi là dữ liệu thật. Điểm quá thấp thì quá nhiều hồ sơ phải chuyển người duyệt.

## 3. Đánh giá

| Chỉ số | Cách đo | Ngưỡng chấp nhận |
|---|---|---|
| Sai số hiệu chỉnh (ví dụ ECE) theo từng trường | Trên golden set AIP-026 | `[CẦN XÁC NHẬN]` |
| Reliability diagram | Vẽ theo từng loại trường | `[CẦN XÁC NHẬN]` |

## 4. Hướng tiếp cận và thử nghiệm

### 4.1. Hướng tiếp cận ứng viên

| Hướng | Ưu điểm | Nhược điểm |
|---|---|---|
| `[CẦN XÁC NHẬN]` Chưa khảo sát thêm | | |

### 4.2. Dữ liệu cần chuẩn bị

- Kết quả OCR có nhãn đúng/sai theo từng trường, lấy từ golden set.

### 4.3. Nhật ký thử nghiệm

| Ngày | Thử nghiệm | Kết quả | Kết luận |
|---|---|---|---|
| | | | |

## 5. Câu hỏi còn mở

- [ ] Hiệu chỉnh riêng cho từng model OCR hay chung?

## 6. Tài liệu tham chiếu

Quy tắc ghi: `standards/07-references.md`.

| Mã | Tài liệu | Chiều | Nội dung liên quan |
|---|---|---|---|
| `AIP-001` | [Đọc bố cục và chữ tiếng Việt trên giấy tờ](AIP-001-document-ocr.md) | Dựa vào | Hiệu chỉnh điểm tin cậy đầu ra của OCR |
| `AIP-005` | [Trích xuất theo schema và sửa lỗi OCR](AIP-005-schema-extraction.md) | Được dùng bởi | Chọn trường cần sửa theo độ tin cậy đã hiệu chỉnh |
| `AIP-010` | [Phân biệt mâu thuẫn thật với lỗi OCR/trích xuất](AIP-010-conflict-vs-error.md) | Được dùng bởi | Dùng độ tin cậy đã hiệu chỉnh để nhận ra lỗi OCR |
| `AIP-013` | [Ước lượng độ bất định lan truyền](AIP-013-uncertainty-propagation.md) | Được dùng bởi | Sai số OCR đầu vào |

## 7. Lịch sử thay đổi

| Ngày | Người sửa | Nội dung | Đã rà tham chiếu |
|---|---|---|---|
| 2026-09-28 | <Tên> | Tạo mới, định nghĩa ban đầu từ danh sách bài toán AI của luồng | Không cần |
| 2026-09-29 | binhnguyenSoftz | Tổ chức lại: đổi mã từ AIP-003 cũ; nhóm `AIG-01`, thêm `kind`; viết lại phát biểu bài toán | Có |
