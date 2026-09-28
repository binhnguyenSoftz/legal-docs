---
id: AIP-008
title: Chuẩn hóa địa chỉ hành chính Việt Nam
group: AIG-04
kind: problem            # problem | method | concern | enabler
status: Draft            # Draft | Review | Approved | Deprecated
stage: Defined           # Defined | Exploring | Decided | In production
priority: Should         # Must | Should | Could
early_test: false        # true: nằm trong nhóm khó nhất, thử nghiệm sớm
owner: <Tên người phụ trách>
updated: 2026-09-29
---

# AIP-008 - Chuẩn hóa địa chỉ hành chính Việt Nam

## 1. Định nghĩa

### 1.1. Phát biểu bài toán

Đưa chuỗi địa chỉ trích xuất về đơn vị hành chính chuẩn (tỉnh, huyện, xã và mã), có tính tới địa chỉ viết tắt, sai chính tả và đơn vị hành chính đã sáp nhập hoặc đổi tên theo thời kỳ.

**Ví dụ:** `P. 3, Q. Bình Thạnh, TP.HCM` và `Phường 3 - Bình Thạnh - Sài Gòn` cùng được chuẩn hóa về một mã xã. Địa chỉ ghi trên giấy tờ cũ theo đơn vị đã sáp nhập được ánh xạ sang đơn vị hiện hành, giữ lại tên cũ.

**Phạm vi:**

- Gồm: chuẩn hóa tên, mã; ánh xạ đơn vị hành chính cũ sang mới.
- Không gồm: trích xuất chuỗi địa chỉ (AIP-005), so khớp thửa đất.

### 1.2. Vị trí trong luồng

**Bước:** Chuẩn hóa, khớp thực thể (nhóm [AIG-04](AIG-04-entity-resolution.md) - Khớp thực thể và suy ra quan hệ). Sơ đồ luồng xem [README](README.md).

- Dựa vào: [AIP-005](AIP-005-schema-extraction.md) - Trích xuất theo schema và sửa lỗi OCR
- Được dùng bởi: [AIP-009](AIP-009-household-inference.md) - Suy ra quan hệ hộ

### 1.3. Đầu vào và đầu ra

| | Nội dung | Ví dụ |
|---|---|---|
| Đầu vào | Chuỗi địa chỉ đã trích xuất | `P. 3, Q. Bình Thạnh` |
| Đầu ra | Mã và tên đơn vị hành chính chuẩn | - |

### 1.4. Ràng buộc bắt buộc

Chưa có. Bổ sung khi đi sâu vào bài toán, đánh mã `AIP-008-R01`, `R02`...

## 2. Vì sao khó

### 2.1. Thách thức

- Cần fuzzy matching vì cách viết rất đa dạng.
- Tên đơn vị đã đổi hoặc sáp nhập, giấy cũ và giấy mới ghi khác nhau.

### 2.2. Chi phí khi sai

Chuẩn hóa sai làm hai địa chỉ giống nhau bị coi là khác, dẫn tới báo mâu thuẫn sai.

## 3. Đánh giá

| Chỉ số | Cách đo | Ngưỡng chấp nhận |
|---|---|---|
| Tỉ lệ chuẩn hóa đúng | `[CẦN XÁC NHẬN]` | `[CẦN XÁC NHẬN]` |

## 4. Hướng tiếp cận và thử nghiệm

### 4.1. Hướng tiếp cận ứng viên

| Hướng | Ưu điểm | Nhược điểm |
|---|---|---|
| Fuzzy matching với danh mục đơn vị hành chính | `[CẦN XÁC NHẬN]` | `[CẦN XÁC NHẬN]` |
| `[CẦN XÁC NHẬN]` Chưa khảo sát thêm | | |

### 4.2. Dữ liệu cần chuẩn bị

- Danh mục đơn vị hành chính kèm lịch sử đổi tên, sáp nhập.

### 4.3. Nhật ký thử nghiệm

| Ngày | Thử nghiệm | Kết quả | Kết luận |
|---|---|---|---|
| | | | |

## 5. Câu hỏi còn mở

- [ ] Lấy danh mục đơn vị hành chính và lịch sử thay đổi từ nguồn nào?

## 6. Tài liệu tham chiếu

Quy tắc ghi: `standards/07-references.md`.

| Mã | Tài liệu | Chiều | Nội dung liên quan |
|---|---|---|---|
| `AIP-005` | [Trích xuất theo schema và sửa lỗi OCR](AIP-005-schema-extraction.md) | Dựa vào | Dùng địa chỉ đã trích xuất |
| `AIP-009` | [Suy ra quan hệ hộ](AIP-009-household-inference.md) | Được dùng bởi | Dùng địa chỉ đã chuẩn hóa |

## 7. Lịch sử thay đổi

| Ngày | Người sửa | Nội dung | Đã rà tham chiếu |
|---|---|---|---|
| 2026-09-28 | <Tên> | Tạo mới, định nghĩa ban đầu từ danh sách bài toán AI của luồng | Không cần |
| 2026-09-29 | binhnguyenSoftz | Tổ chức lại: đổi mã từ AIP-014 cũ; nhóm `AIG-04`, thêm `kind`; viết lại phát biểu bài toán | Có |
