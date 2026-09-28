---
id: AIP-016
title: Quan hệ giữa văn bản pháp luật
group: AIG-06
kind: problem            # problem | method | concern | enabler
status: Draft            # Draft | Review | Approved | Deprecated
stage: Defined           # Defined | Exploring | Decided | In production
priority: Must           # Must | Should | Could
early_test: false        # true: nằm trong nhóm khó nhất, thử nghiệm sớm
owner: <Tên người phụ trách>
updated: 2026-09-29
---

# AIP-016 - Quan hệ giữa văn bản pháp luật

## 1. Định nghĩa

### 1.1. Phát biểu bài toán

Dựng và cập nhật dữ liệu có cấu trúc về quan hệ giữa các văn bản pháp luật: văn bản nào sửa đổi, thay thế, bãi bỏ, hướng dẫn văn bản nào, từ ngày nào, ở mức điều/khoản nào.

**Ví dụ:** một nghị định hướng dẫn bị sửa đổi một phần bởi nghị định sau. Dữ liệu quan hệ ghi: điều X của văn bản A bị sửa bởi điều Y của văn bản B, hiệu lực từ ngày ...; điều Z của văn bản A vẫn giữ nguyên.

**Phạm vi:**

- Gồm: quan hệ sửa đổi, thay thế, bãi bỏ, hướng dẫn, chuyển tiếp ở mức điều/khoản.
- Không gồm: chọn phiên bản theo thời điểm (AIP-015), xử lý xung đột nội dung (AIP-017).

### 1.2. Vị trí trong luồng

**Bước:** Truy xuất pháp luật (nhóm [AIG-06](AIG-06-legal-retrieval.md) - Truy xuất pháp luật theo hiệu lực). Sơ đồ luồng xem [README](README.md).

- Dựa vào: không có.
- Được dùng bởi: [AIP-015](AIP-015-temporal-validity-retrieval.md) - Truy xuất theo hiệu lực thời gian; [AIP-017](AIP-017-legal-conflict-resolution.md) - Giải quyết xung đột giữa văn bản

### 1.3. Đầu vào và đầu ra

| | Nội dung | Ví dụ |
|---|---|---|
| Đầu vào | Kho văn bản pháp luật | - |
| Đầu ra | Knowledge graph hoặc metadata có cấu trúc về quan hệ văn bản | - |

### 1.4. Ràng buộc bắt buộc

Chưa có. Bổ sung khi đi sâu vào bài toán, đánh mã `AIP-016-R01`, `R02`...

## 2. Vì sao khó

### 2.1. Thách thức

- Quan hệ có thể ở mức điều, khoản, không chỉ mức văn bản.

### 2.2. Chi phí khi sai

Thiếu quan hệ thì truy xuất ra văn bản đã bị thay thế.

## 3. Đánh giá

| Chỉ số | Cách đo | Ngưỡng chấp nhận |
|---|---|---|
| `[CẦN XÁC NHẬN]` | `[CẦN XÁC NHẬN]` | `[CẦN XÁC NHẬN]` |

## 4. Hướng tiếp cận và thử nghiệm

### 4.1. Hướng tiếp cận ứng viên

| Hướng | Ưu điểm | Nhược điểm |
|---|---|---|
| Knowledge graph | `[CẦN XÁC NHẬN]` | `[CẦN XÁC NHẬN]` |
| Metadata có cấu trúc | `[CẦN XÁC NHẬN]` | `[CẦN XÁC NHẬN]` |
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
| `AIP-015` | [Truy xuất theo hiệu lực thời gian](AIP-015-temporal-validity-retrieval.md) | Được dùng bởi | Dùng quan hệ sửa đổi, thay thế để xác định phiên bản |
| `AIP-017` | [Giải quyết xung đột giữa văn bản](AIP-017-legal-conflict-resolution.md) | Được dùng bởi | Dùng quan hệ và thứ bậc văn bản |

## 7. Lịch sử thay đổi

| Ngày | Người sửa | Nội dung | Đã rà tham chiếu |
|---|---|---|---|
| 2026-09-28 | <Tên> | Tạo mới, định nghĩa ban đầu từ danh sách bài toán AI của luồng | Không cần |
| 2026-09-29 | binhnguyenSoftz | Tổ chức lại: đổi mã từ AIP-023 cũ; nhóm `AIG-06`, thêm `kind`; viết lại phát biểu bài toán | Có |
