---
id: AIP-017
title: Giải quyết xung đột giữa văn bản
group: AIG-06
kind: problem            # problem | method | concern | enabler
status: Draft            # Draft | Review | Approved | Deprecated
stage: Defined           # Defined | Exploring | Decided | In production
priority: Should         # Must | Should | Could
early_test: false        # true: nằm trong nhóm khó nhất, thử nghiệm sớm
owner: <Tên người phụ trách>
updated: 2026-09-29
---

# AIP-017 - Giải quyết xung đột giữa văn bản

## 1. Định nghĩa

### 1.1. Phát biểu bài toán

Khi nhiều quy định cùng điều chỉnh một vấn đề nhưng nói khác nhau, chọn quy định được áp dụng theo thứ bậc hiệu lực (luật trên nghị định, luật chuyên ngành, văn bản sau thay văn bản trước) và ghi rõ lý do chọn.

**Ví dụ:** luật chuyên ngành và một thông tư hướng dẫn quy định thời hạn xử lý khác nhau. Hệ thống chọn quy định của luật, ghi lý do "văn bản có hiệu lực pháp lý cao hơn", và đánh dấu để cán bộ xem.

**Phạm vi:**

- Gồm: chọn quy định áp dụng khi có xung đột, kèm lý do.
- Không gồm: lấy phiên bản có hiệu lực (AIP-015).

### 1.2. Vị trí trong luồng

**Bước:** Truy xuất pháp luật (nhóm [AIG-06](AIG-06-legal-retrieval.md) - Truy xuất pháp luật theo hiệu lực). Sơ đồ luồng xem [README](README.md).

- Dựa vào: [AIP-016](AIP-016-legal-document-relations.md) - Quan hệ giữa văn bản pháp luật
- Được dùng bởi: [AIP-019](AIP-019-legal-reasoning.md) - Suy luận pháp lý

### 1.3. Đầu vào và đầu ra

| | Nội dung | Ví dụ |
|---|---|---|
| Đầu vào | Các chunk quy định cùng vấn đề, quan hệ văn bản (AIP-016) | - |
| Đầu ra | Quy định được áp dụng và lý do | - |

### 1.4. Ràng buộc bắt buộc

Chưa có. Bổ sung khi đi sâu vào bài toán, đánh mã `AIP-017-R01`, `R02`...

## 2. Vì sao khó

### 2.1. Thách thức

- Cần biết thứ bậc hiệu lực và nguyên tắc áp dụng khi xung đột.

### 2.2. Chi phí khi sai

Áp quy định có thứ bậc thấp hơn khi có xung đột là sai căn cứ.

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
| `AIP-016` | [Quan hệ giữa văn bản pháp luật](AIP-016-legal-document-relations.md) | Dựa vào | Dùng quan hệ và thứ bậc văn bản |
| `AIP-019` | [Suy luận pháp lý](AIP-019-legal-reasoning.md) | Được dùng bởi | Dùng quy định được chọn khi có xung đột |

## 7. Lịch sử thay đổi

| Ngày | Người sửa | Nội dung | Đã rà tham chiếu |
|---|---|---|---|
| 2026-09-28 | <Tên> | Tạo mới, định nghĩa ban đầu từ danh sách bài toán AI của luồng | Không cần |
| 2026-09-29 | binhnguyenSoftz | Tổ chức lại: đổi mã từ AIP-024 cũ; nhóm `AIG-06`, thêm `kind`; viết lại phát biểu bài toán | Có |
