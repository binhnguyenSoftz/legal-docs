---
id: AIP-021
title: Giải thích và faithfulness
group: AIG-07
kind: problem            # problem | method | concern | enabler
status: Draft            # Draft | Review | Approved | Deprecated
stage: Defined           # Defined | Exploring | Decided | In production
priority: Must           # Must | Should | Could
early_test: false        # true: nằm trong nhóm khó nhất, thử nghiệm sớm
owner: <Tên người phụ trách>
updated: 2026-09-29
---

# AIP-021 - Giải thích và faithfulness

## 1. Định nghĩa

### 1.1. Phát biểu bài toán

Lời giải thích đi kèm quyết định phải phản ánh đúng cơ sở mà hệ thống thực sự dùng để ra quyết định (faithfulness), và mỗi ý phải dẫn tới dữ liệu hồ sơ và điều khoản kiểm chứng được.

**Ví dụ:** giải thích "Đề xuất cần bổ sung vì thiếu giấy chứng tử" phải khớp với kết quả của AIP-012, dẫn tới điều khoản quy định thành phần hồ sơ, và không được nêu lý do mà quá trình suy luận không dùng tới.

**Phạm vi:**

- Gồm: lời giải thích, dẫn chứng tới dữ liệu và điều luật, kiểm tra faithfulness.
- Không gồm: văn bản gửi người dân (AIP-023).

### 1.2. Vị trí trong luồng

**Bước:** Suy luận, ra quyết định (nhóm [AIG-07](AIG-07-legal-decision.md) - Suy luận pháp lý và hỗ trợ quyết định). Sơ đồ luồng xem [README](README.md).

- Dựa vào: [AIP-019](AIP-019-legal-reasoning.md) - Suy luận pháp lý
- Được dùng bởi: không có.

### 1.3. Đầu vào và đầu ra

| | Nội dung | Ví dụ |
|---|---|---|
| Đầu vào | Quá trình và kết quả suy luận (AIP-019) | - |
| Đầu ra | Lập luận kèm dẫn chứng tới dữ liệu và điều luật | - |

### 1.4. Ràng buộc bắt buộc

| Mã | Ràng buộc | Lý do |
|---|---|---|
| AIP-021-R01 | Mỗi bước lập luận phải có dẫn chứng tới dữ liệu hồ sơ hoặc điều luật. | Cán bộ và người dân kiểm chứng được. |

## 2. Vì sao khó

### 2.1. Thách thức

- Model có thể đưa ra lời giải thích hợp lý nhưng không phải lý do thật.

### 2.2. Chi phí khi sai

Giải thích sai khiến cán bộ tin vào quyết định sai.

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
| `AIP-019` | [Suy luận pháp lý](AIP-019-legal-reasoning.md) | Dựa vào | Lập luận phải khớp cơ sở quyết định |

## 7. Lịch sử thay đổi

| Ngày | Người sửa | Nội dung | Đã rà tham chiếu |
|---|---|---|---|
| 2026-09-28 | <Tên> | Tạo mới, định nghĩa ban đầu từ danh sách bài toán AI của luồng | Không cần |
| 2026-09-29 | binhnguyenSoftz | Tổ chức lại: đổi mã từ AIP-029 cũ; nhóm `AIG-07`, thêm `kind`; viết lại phát biểu bài toán | Có |
