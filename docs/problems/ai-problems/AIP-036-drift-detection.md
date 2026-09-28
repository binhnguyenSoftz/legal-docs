---
id: AIP-036
title: Drift detection
group: AIG-12
kind: enabler            # problem | method | concern | enabler
status: Draft            # Draft | Review | Approved | Deprecated
stage: Defined           # Defined | Exploring | Decided | In production
priority: Could          # Must | Should | Could
early_test: false        # true: nằm trong nhóm khó nhất, thử nghiệm sớm
owner: <Tên người phụ trách>
updated: 2026-09-29
---

# AIP-036 - Drift detection

## 1. Định nghĩa

### 1.1. Phát biểu bài toán

Theo dõi dữ liệu và chỉ số khi chạy thật để phát hiện sớm khi đầu vào thay đổi (chất lượng scan, mẫu biểu mới, loại giấy tờ mới) hoặc luật thay đổi, trước khi chất lượng giảm rõ.

**Ví dụ:** từ tháng 10, tỉ lệ trường điểm thấp trên CCCD tăng từ 5% lên 18%. Phân tích cho thấy thẻ căn cước mẫu mới đã xuất hiện. Cảnh báo drift gửi người phụ trách AIG-01.

**Phạm vi:**

- Gồm: theo dõi phân phối đầu vào, chỉ số khi chạy thật; cảnh báo.
- Không gồm: regression khi chính hệ thống đổi phiên bản (AIP-028).

### 1.2. Vị trí trong luồng

**Bước:** Xuyên suốt: triển khai, vận hành (nhóm [AIG-12](AIG-12-model-operations.md) - Triển khai và vận hành model). Sơ đồ luồng xem [README](README.md).

- Dựa vào: [AIP-003](AIP-003-image-quality-check.md) - Đánh giá chất lượng ảnh; [AIP-015](AIP-015-temporal-validity-retrieval.md) - Truy xuất theo hiệu lực thời gian
- Được dùng bởi: không có.

### 1.3. Đầu vào và đầu ra

| | Nội dung | Ví dụ |
|---|---|---|
| Đầu vào | Chỉ số chạy thật theo thời gian | - |
| Đầu ra | Cảnh báo drift | - |

### 1.4. Ràng buộc bắt buộc

Chưa có. Bổ sung khi đi sâu vào bài toán, đánh mã `AIP-036-R01`, `R02`...

## 2. Vì sao khó

### 2.1. Thách thức

- Không có nhãn ở dữ liệu chạy thật.

### 2.2. Chi phí khi sai

Chất lượng giảm dần mà không ai biết.

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
| `AIP-003` | [Đánh giá chất lượng ảnh](AIP-003-image-quality-check.md) | Dựa vào | Theo dõi chất lượng ảnh scan theo thời gian |
| `AIP-015` | [Truy xuất theo hiệu lực thời gian](AIP-015-temporal-validity-retrieval.md) | Dựa vào | Theo dõi thay đổi quy định |

## 7. Lịch sử thay đổi

| Ngày | Người sửa | Nội dung | Đã rà tham chiếu |
|---|---|---|---|
| 2026-09-28 | <Tên> | Tạo mới, định nghĩa ban đầu từ danh sách bài toán AI của luồng | Không cần |
| 2026-09-29 | binhnguyenSoftz | Tổ chức lại: đổi mã từ AIP-041 cũ; nhóm `AIG-12`, thêm `kind`; viết lại phát biểu bài toán | Có |
