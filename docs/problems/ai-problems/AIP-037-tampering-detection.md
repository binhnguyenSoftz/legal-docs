---
id: AIP-037
title: Phát hiện giả mạo, chỉnh sửa ảnh
group: AIG-13
kind: concern            # problem | method | concern | enabler
status: Draft            # Draft | Review | Approved | Deprecated
stage: Defined           # Defined | Exploring | Decided | In production
priority: Could          # Must | Should | Could
early_test: false        # true: nằm trong nhóm khó nhất, thử nghiệm sớm
owner: <Tên người phụ trách>
updated: 2026-09-29
---

# AIP-037 - Phát hiện giả mạo, chỉnh sửa ảnh

## 1. Định nghĩa

### 1.1. Phát biểu bài toán

Phát hiện dấu hiệu giấy tờ bị giả mạo hoặc chỉnh sửa ảnh: dấu mộc không khớp mẫu, vùng ảnh ghép, chữ bị sửa, số liệu bị chèn. Chỉ cảnh báo và chỉ vùng nghi ngờ cho cán bộ, không tự kết luận giả mạo.

**Ví dụ:** giấy xác nhận có dấu mộc đỏ nhưng vùng dấu có độ nén JPEG khác phần còn lại và viền dấu bị cắt thẳng. Kết quả `{suspect: true, region: "stamp", reason: "nén ảnh không đồng nhất"}`.

**Phạm vi:**

- Gồm: phát hiện chỉnh sửa ảnh, dấu mộc bất thường; chỉ vùng nghi ngờ.
- Không gồm: xác minh với cơ quan cấp giấy tờ (nghiệp vụ, không phải AI).

### 1.2. Vị trí trong luồng

**Bước:** Xuyên suốt: toàn vẹn giấy tờ (nhóm [AIG-13](AIG-13-document-integrity.md) - Toàn vẹn giấy tờ). Sơ đồ luồng xem [README](README.md).

- Dựa vào: [AIP-001](AIP-001-document-ocr.md) - Đọc bố cục và chữ tiếng Việt trên giấy tờ
- Được dùng bởi: không có.

### 1.3. Đầu vào và đầu ra

| | Nội dung | Ví dụ |
|---|---|---|
| Đầu vào | Ảnh giấy tờ và các vùng dấu mộc, chữ ký (AIP-001) | Ảnh xác nhận có dấu mộc |
| Đầu ra | Cảnh báo nghi giả mạo kèm vùng nghi ngờ | `{suspect: true, region: "stamp"}` |

### 1.4. Ràng buộc bắt buộc

Chưa có. Bổ sung khi đi sâu vào bài toán, đánh mã `AIP-037-R01`, `R02`...

## 2. Vì sao khó

### 2.1. Thách thức

- Mộc không khớp với đơn vị ghi trên giấy.
- Ảnh ghép khó phát hiện bằng mắt.

### 2.2. Chi phí khi sai

Báo nhầm thì hồ sơ thật bị nghi ngờ. Bỏ sót thì hồ sơ giả được chấp thuận.

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

- Mẫu dấu mộc thật theo đơn vị (nếu có).
- Mẫu ảnh đã bị chỉnh sửa để kiểm thử.

### 4.3. Nhật ký thử nghiệm

| Ngày | Thử nghiệm | Kết quả | Kết luận |
|---|---|---|---|
| | | | |

## 5. Câu hỏi còn mở

- [ ] Bài toán này là tùy chọn. Khi nào cần làm?

## 6. Tài liệu tham chiếu

Quy tắc ghi: `standards/07-references.md`.

| Mã | Tài liệu | Chiều | Nội dung liên quan |
|---|---|---|---|
| `AIP-001` | [Đọc bố cục và chữ tiếng Việt trên giấy tờ](AIP-001-document-ocr.md) | Dựa vào | Dùng vùng dấu mộc, chữ ký đã tách |

## 7. Lịch sử thay đổi

| Ngày | Người sửa | Nội dung | Đã rà tham chiếu |
|---|---|---|---|
| 2026-09-28 | <Tên> | Tạo mới, định nghĩa ban đầu từ danh sách bài toán AI của luồng | Không cần |
| 2026-09-29 | binhnguyenSoftz | Tổ chức lại: đổi mã từ AIP-005 cũ; nhóm `AIG-13`, thêm `kind`; viết lại phát biểu bài toán | Có |
