---
id: AIP-025
title: Kiểm chứng sau sinh
group: AIG-08
kind: problem            # problem | method | concern | enabler
status: Draft            # Draft | Review | Approved | Deprecated
stage: Defined           # Defined | Exploring | Decided | In production
priority: Must           # Must | Should | Could
early_test: false        # true: nằm trong nhóm khó nhất, thử nghiệm sớm
owner: <Tên người phụ trách>
updated: 2026-09-29
---

# AIP-025 - Kiểm chứng sau sinh

## 1. Định nghĩa

### 1.1. Phát biểu bài toán

Trước khi chuyển cán bộ, đối chiếu tự động mọi dữ kiện trong văn bản đã sinh (họ tên, số giấy tờ, ngày, diện tích, số tiền) với dữ liệu đã duyệt, và mọi trích dẫn với kho luật. Sai một chỗ thì không cho qua.

**Ví dụ:** văn bản ghi "thửa đất số 126" trong khi dữ liệu đã duyệt là `125`. Kiểm chứng trả "không đạt", chỉ ra câu sai và giá trị đúng, văn bản được sinh lại.

**Phạm vi:**

- Gồm: đối chiếu dữ kiện và trích dẫn trong văn bản; danh sách chỗ sai.
- Không gồm: chấm văn phong, chất lượng câu chữ (AIP-027).

### 1.2. Vị trí trong luồng

**Bước:** Sinh văn bản (nhóm [AIG-08](AIG-08-legal-generation.md) - Sinh và kiểm chứng văn bản kết quả). Sơ đồ luồng xem [README](README.md).

- Dựa vào: [AIP-023](AIP-023-controlled-generation.md) - Sinh văn bản kết quả có kiểm soát; [AIP-024](AIP-024-citation-grounding.md) - Grounding trích dẫn pháp lý
- Được dùng bởi: không có.

### 1.3. Đầu vào và đầu ra

| | Nội dung | Ví dụ |
|---|---|---|
| Đầu vào | Văn bản đã sinh, dữ liệu đã duyệt, kho luật | - |
| Đầu ra | Đạt / không đạt kèm danh sách chỗ sai | - |

### 1.4. Ràng buộc bắt buộc

| Mã | Ràng buộc | Lý do |
|---|---|---|
| AIP-025-R01 | Mọi dữ kiện và mọi trích dẫn phải được kiểm chứng trước khi phát hành. | Chặn lỗi của bước sinh. |

## 2. Vì sao khó

### 2.1. Thách thức

- Tách được từng dữ kiện và từng trích dẫn trong văn bản tự do.

### 2.2. Chi phí khi sai

Bỏ sót lỗi thì văn bản sai tới tay người dân.

## 3. Đánh giá

| Chỉ số | Cách đo | Ngưỡng chấp nhận |
|---|---|---|
| Tỉ lệ phát hiện lỗi đã cài sẵn | `[CẦN XÁC NHẬN]` | `[CẦN XÁC NHẬN]` |

## 4. Hướng tiếp cận và thử nghiệm

### 4.1. Hướng tiếp cận ứng viên

| Hướng | Ưu điểm | Nhược điểm |
|---|---|---|
| Model hoặc code kiểm tra riêng | `[CẦN XÁC NHẬN]` | `[CẦN XÁC NHẬN]` |
| `[CẦN XÁC NHẬN]` Chưa khảo sát thêm | | |

### 4.2. Dữ liệu cần chuẩn bị

- Văn bản có cài lỗi để kiểm thử.

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
| `AIP-023` | [Sinh văn bản kết quả có kiểm soát](AIP-023-controlled-generation.md) | Dựa vào | Kiểm chứng dữ kiện trong văn bản |
| `AIP-024` | [Grounding trích dẫn pháp lý](AIP-024-citation-grounding.md) | Dựa vào | Kiểm chứng trích dẫn với kho luật |

## 7. Lịch sử thay đổi

| Ngày | Người sửa | Nội dung | Đã rà tham chiếu |
|---|---|---|---|
| 2026-09-28 | <Tên> | Tạo mới, định nghĩa ban đầu từ danh sách bài toán AI của luồng | Không cần |
| 2026-09-29 | binhnguyenSoftz | Tổ chức lại: đổi mã từ AIP-034 cũ; nhóm `AIG-08`, thêm `kind`; viết lại phát biểu bài toán | Có |
