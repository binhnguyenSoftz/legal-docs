---
id: AIP-035
title: Phân tầng model, tối ưu chi phí và độ trễ
group: AIG-12
kind: enabler            # problem | method | concern | enabler
status: Draft            # Draft | Review | Approved | Deprecated
stage: Defined           # Defined | Exploring | Decided | In production
priority: Should         # Must | Should | Could
early_test: false        # true: nằm trong nhóm khó nhất, thử nghiệm sớm
owner: <Tên người phụ trách>
updated: 2026-09-29
---

# AIP-035 - Phân tầng model, tối ưu chi phí và độ trễ

## 1. Định nghĩa

### 1.1. Phát biểu bài toán

Chọn model cho từng bước của luồng (model nhỏ cho bước dễ, model mạnh cho bước khó), đặt điều kiện chuyển lên model mạnh hơn, và áp các kỹ thuật cache, batching, quantization để chi phí và độ trễ trên mỗi hồ sơ nằm trong ngân sách mà chất lượng không giảm dưới ngưỡng đã chốt.

**Ví dụ:** trích xuất CCCD dùng model nhỏ vì mẫu cố định. Trích xuất giấy sang đất viết tay, không có mẫu, dùng model nhỏ trước; nếu độ tin cậy dưới 0,7 thì chạy lại bằng model mạnh (cascade). Suy luận pháp lý luôn dùng model mạnh.

**Phạm vi:**

- Gồm: bảng model theo bước; cascade; cache, batching, quantization khi tự host.
- Không gồm: quyết định host nội bộ hay dùng API ngoài (AIP-034), phát hiện drift (AIP-036).

### 1.2. Vị trí trong luồng

**Bước:** Xuyên suốt: triển khai, vận hành (nhóm [AIG-12](AIG-12-model-operations.md) - Triển khai và vận hành model). Sơ đồ luồng xem [README](README.md).

- Dựa vào: [AIP-005](AIP-005-schema-extraction.md) - Trích xuất theo schema và sửa lỗi OCR; [AIP-034](AIP-034-data-privacy-hosting.md) - Model nội bộ hay API ngoài, bảo vệ dữ liệu cá nhân
- Được dùng bởi: không có.

### 1.3. Đầu vào và đầu ra

| | Nội dung | Ví dụ |
|---|---|---|
| Đầu vào | Danh sách bước cần model; số liệu chi phí, độ trễ, độ chính xác theo bước; ngân sách | - |
| Đầu ra | Bảng model cho từng bước kèm điều kiện chuyển model; cấu hình cache, cascade, batching, quantization | `{step: "extract", model: "small", escalate_if: "score < 0,7"}` |

### 1.4. Ràng buộc bắt buộc

Chưa có. Bổ sung khi đi sâu vào bài toán, đánh mã `AIP-035-R01`, `R02`...

### 1.5. Bài toán con

| Bài toán con | Mã cũ | Ưu tiên | Nội dung |
|---|---|---|---|
| Chọn và phân tầng model | AIP-012 cũ | Should | Chọn model cho từng bước, điều kiện chuyển model |
| Tối ưu chi phí và độ trễ | AIP-047 cũ | Could | Cache, cascade, batching, quantization |

## 2. Vì sao khó

### 2.1. Thách thức

- Ba mục tiêu chi phí, độ trễ, độ chính xác kéo ngược nhau.
- Kết quả phụ thuộc ràng buộc dữ liệu cá nhân (AIP-034).
- Tối ưu có thể làm giảm độ chính xác.

### 2.2. Chi phí khi sai

- Chọn model quá yếu thì sai nhiều. Chọn quá mạnh thì tốn chi phí và chậm.
- Chi phí vượt ngân sách hoặc người dân chờ quá lâu.

## 3. Đánh giá

| Chỉ số | Cách đo | Ngưỡng chấp nhận |
|---|---|---|
| Độ chính xác, chi phí, độ trễ theo từng bước | Trên golden set AIP-026 | `[CẦN XÁC NHẬN]` |
| Chi phí và độ trễ trên một hồ sơ | `[CẦN XÁC NHẬN]` | `[CẦN XÁC NHẬN]` |

## 4. Hướng tiếp cận và thử nghiệm

### 4.1. Hướng tiếp cận ứng viên

| Hướng | Ưu điểm | Nhược điểm |
|---|---|---|
| Model nhỏ cho trích xuất, model mạnh cho suy luận | Giảm chi phí | `[CẦN XÁC NHẬN]` |
| Cascade model | `[CẦN XÁC NHẬN]` | `[CẦN XÁC NHẬN]` |
| Cache | `[CẦN XÁC NHẬN]` | `[CẦN XÁC NHẬN]` |
| Batching | `[CẦN XÁC NHẬN]` | `[CẦN XÁC NHẬN]` |
| Quantization khi tự host | `[CẦN XÁC NHẬN]` | `[CẦN XÁC NHẬN]` |
| `[CẦN XÁC NHẬN]` Chưa khảo sát thêm | | |

### 4.2. Dữ liệu cần chuẩn bị

- Số liệu chi phí, độ trễ theo bước khi chạy trên golden set.

### 4.3. Nhật ký thử nghiệm

| Ngày | Thử nghiệm | Kết quả | Kết luận |
|---|---|---|---|
| | | | |

## 5. Câu hỏi còn mở

- [ ] Ngân sách chi phí và độ trễ mục tiêu cho một hồ sơ là bao nhiêu?

## 6. Tài liệu tham chiếu

Quy tắc ghi: `standards/07-references.md`.

| Mã | Tài liệu | Chiều | Nội dung liên quan |
|---|---|---|---|
| `AIP-005` | [Trích xuất theo schema và sửa lỗi OCR](AIP-005-schema-extraction.md) | Dựa vào | Chọn model cho bước trích xuất |
| `AIP-034` | [Model nội bộ hay API ngoài, bảo vệ dữ liệu cá nhân](AIP-034-data-privacy-hosting.md) | Dựa vào | Lựa chọn model và tối ưu bị giới hạn bởi hosting đã chọn |

## 7. Lịch sử thay đổi

| Ngày | Người sửa | Nội dung | Đã rà tham chiếu |
|---|---|---|---|
| 2026-09-28 | <Tên> | Tạo mới, định nghĩa ban đầu từ danh sách bài toán AI của luồng | Không cần |
| 2026-09-29 | binhnguyenSoftz | Tổ chức lại: gộp AIP-012 cũ (phân tầng model) và AIP-047 cũ (chi phí, độ trễ); nhóm `AIG-12`; viết lại phát biểu bài toán | Có |
