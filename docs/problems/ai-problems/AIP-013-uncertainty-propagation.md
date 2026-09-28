---
id: AIP-013
title: Ước lượng độ bất định lan truyền
group: AIG-05
kind: method             # problem | method | concern | enabler
status: Draft            # Draft | Review | Approved | Deprecated
stage: Defined           # Defined | Exploring | Decided | In production
priority: Should         # Must | Should | Could
early_test: false        # true: nằm trong nhóm khó nhất, thử nghiệm sớm
owner: <Tên người phụ trách>
updated: 2026-09-29
---

# AIP-013 - Ước lượng độ bất định lan truyền

## 1. Định nghĩa

### 1.1. Phát biểu bài toán

Ước lượng sai số OCR và trích xuất ở từng trường ảnh hưởng thế nào tới từng kết luận ở bước sau. Kết luận dựa trên nhiều trường không chắc chắn thì độ bất định phải cao tương ứng, để bước quyết định biết khi nào chuyển người.

**Ví dụ:** điều kiện "người thừa kế đủ 18 tuổi" dựa trên ngày sinh viết tay có điểm 0,62. Nếu năm sinh đọc sai một chữ số, kết luận có thể đảo. Độ bất định của điều kiện này được đánh giá cao dù phép so sánh tuổi luôn chính xác.

**Phạm vi:**

- Gồm: lan truyền độ tin cậy từ trường sang kết luận.
- Không gồm: hiệu chỉnh điểm từng trường (AIP-002), chọn ngưỡng quyết định (AIP-020).

### 1.2. Vị trí trong luồng

**Bước:** Đối chiếu chéo (nhóm [AIG-05](AIG-05-cross-document-validation.md) - Đối chiếu và kiểm tra chéo giấy tờ). Sơ đồ luồng xem [README](README.md).

- Dựa vào: [AIP-002](AIP-002-ocr-confidence-calibration.md) - Hiệu chỉnh độ tin cậy theo từng trường; [AIP-010](AIP-010-conflict-vs-error.md) - Phân biệt mâu thuẫn thật với lỗi OCR/trích xuất
- Được dùng bởi: [AIP-020](AIP-020-three-way-decision-abstention.md) - Quyết định ba lớp, abstention và ngưỡng theo chi phí lỗi

### 1.3. Đầu vào và đầu ra

| | Nội dung | Ví dụ |
|---|---|---|
| Đầu vào | Độ tin cậy từng trường (AIP-002), kết quả đối chiếu (AIP-010) | - |
| Đầu ra | Độ bất định của từng kết luận | - |

### 1.4. Ràng buộc bắt buộc

Chưa có. Bổ sung khi đi sâu vào bài toán, đánh mã `AIP-013-R01`, `R02`...

## 2. Vì sao khó

### 2.1. Thách thức

- Sai số cộng dồn qua nhiều bước.

### 2.2. Chi phí khi sai

Đánh giá thấp độ bất định thì hệ thống tự quyết khi lẽ ra phải chuyển người.

## 3. Đánh giá

| Chỉ số | Cách đo | Ngưỡng chấp nhận |
|---|---|---|
| `[CẦN XÁC NHẬN]` | `[CẦN XÁC NHẬN]` | `[CẦN XÁC NHẬN]` |

## 4. Hướng tiếp cận và thử nghiệm

### 4.1. Hướng tiếp cận ứng viên

| Hướng | Ưu điểm | Nhược điểm |
|---|---|---|
| `[CẦN XÁC NHẬN]` Chưa khảo sát thêm | | |

### 4.2. Dữ liệu cần chuẩn bị

- `[CẦN XÁC NHẬN]`

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
| `AIP-002` | [Hiệu chỉnh độ tin cậy theo từng trường](AIP-002-ocr-confidence-calibration.md) | Dựa vào | Sai số OCR đầu vào |
| `AIP-010` | [Phân biệt mâu thuẫn thật với lỗi OCR/trích xuất](AIP-010-conflict-vs-error.md) | Dựa vào | Độ bất định của kết quả đối chiếu |
| `AIP-020` | [Quyết định ba lớp, abstention và ngưỡng theo chi phí lỗi](AIP-020-three-way-decision-abstention.md) | Được dùng bởi | Dùng độ bất định để quyết định chuyển người |

## 7. Lịch sử thay đổi

| Ngày | Người sửa | Nội dung | Đã rà tham chiếu |
|---|---|---|---|
| 2026-09-28 | <Tên> | Tạo mới, định nghĩa ban đầu từ danh sách bài toán AI của luồng | Không cần |
| 2026-09-29 | binhnguyenSoftz | Tổ chức lại: đổi mã từ AIP-019 cũ; nhóm `AIG-05`, thêm `kind`; viết lại phát biểu bài toán | Có |
