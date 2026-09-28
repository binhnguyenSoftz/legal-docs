---
id: AIP-034
title: Model nội bộ hay API ngoài, bảo vệ dữ liệu cá nhân
group: AIG-12
kind: concern            # problem | method | concern | enabler
status: Draft            # Draft | Review | Approved | Deprecated
stage: Defined           # Defined | Exploring | Decided | In production
priority: Must           # Must | Should | Could
early_test: false        # true: nằm trong nhóm khó nhất, thử nghiệm sớm
owner: <Tên người phụ trách>
updated: 2026-09-29
---

# AIP-034 - Model nội bộ hay API ngoài, bảo vệ dữ liệu cá nhân

## 1. Định nghĩa

### 1.1. Phát biểu bài toán

Quyết định từng bước dùng model tự host hay API ngoài dựa trên ràng buộc pháp lý về dữ liệu cá nhân, và khi gửi ra ngoài thì che hoặc thay thế dữ liệu cá nhân (masking, pseudonymization) trước khi gửi.

**Ví dụ:** ảnh CCCD có họ tên, số CCCD, địa chỉ. Bước OCR chạy model tự host. Bước suy luận pháp lý dùng API ngoài, nhưng chỉ nhận dữ kiện đã thay tên bằng mã `P1`, số CCCD bằng `ID1`.

**Phạm vi:**

- Gồm: quyết định hosting từng bước; masking, pseudonymization.
- Không gồm: chọn model cụ thể và tối ưu chi phí (AIP-035).

### 1.2. Vị trí trong luồng

**Bước:** Xuyên suốt: triển khai, vận hành (nhóm [AIG-12](AIG-12-model-operations.md) - Triển khai và vận hành model). Sơ đồ luồng xem [README](README.md).

- Dựa vào: không có.
- Được dùng bởi: [AIP-035](AIP-035-model-serving-cost-latency.md) - Phân tầng model, tối ưu chi phí và độ trễ

### 1.3. Đầu vào và đầu ra

| | Nội dung | Ví dụ |
|---|---|---|
| Đầu vào | Ràng buộc pháp lý về dữ liệu cá nhân, yêu cầu chất lượng | - |
| Đầu ra | Quyết định hosting cho từng bước, cách masking/pseudonymization | - |

### 1.4. Ràng buộc bắt buộc

Chưa có. Bổ sung khi đi sâu vào bài toán, đánh mã `AIP-034-R01`, `R02`...

## 2. Vì sao khó

### 2.1. Thách thức

- Masking làm mất thông tin model cần.
- Model tự host thường yếu hơn API ngoài.

### 2.2. Chi phí khi sai

Lộ dữ liệu cá nhân của người dân.

## 3. Đánh giá

| Chỉ số | Cách đo | Ngưỡng chấp nhận |
|---|---|---|
| `[CẦN XÁC NHẬN]` | `[CẦN XÁC NHẬN]` | `[CẦN XÁC NHẬN]` |

## 4. Hướng tiếp cận và thử nghiệm

### 4.1. Hướng tiếp cận ứng viên

| Hướng | Ưu điểm | Nhược điểm |
|---|---|---|
| Model nội bộ | Dữ liệu không ra ngoài | `[CẦN XÁC NHẬN]` |
| API ngoài kèm masking/pseudonymization | `[CẦN XÁC NHẬN]` | Phải che dữ liệu trước khi gửi |
| `[CẦN XÁC NHẬN]` Chưa khảo sát thêm | | |

### 4.2. Dữ liệu cần chuẩn bị

- `[CẦN XÁC NHẬN]`

### 4.3. Nhật ký thử nghiệm

| Ngày | Thử nghiệm | Kết quả | Kết luận |
|---|---|---|---|
| | | | |

## 5. Câu hỏi còn mở

- [ ] Quy định nào về dữ liệu cá nhân áp dụng cho hệ thống này?

## 6. Tài liệu tham chiếu

Quy tắc ghi: `standards/07-references.md`.

| Mã | Tài liệu | Chiều | Nội dung liên quan |
|---|---|---|---|
| `AIP-035` | [Phân tầng model, tối ưu chi phí và độ trễ](AIP-035-model-serving-cost-latency.md) | Được dùng bởi | Lựa chọn model bị giới hạn bởi ràng buộc dữ liệu cá nhân; tối ưu trong giới hạn hosting đã chọn |

## 7. Lịch sử thay đổi

| Ngày | Người sửa | Nội dung | Đã rà tham chiếu |
|---|---|---|---|
| 2026-09-28 | <Tên> | Tạo mới, định nghĩa ban đầu từ danh sách bài toán AI của luồng | Không cần |
| 2026-09-29 | binhnguyenSoftz | Tổ chức lại: đổi mã từ AIP-046 cũ; nhóm `AIG-12`, thêm `kind`; viết lại phát biểu bài toán | Có |
