---
id: AIP-024
title: Grounding trích dẫn pháp lý
group: AIG-08
kind: problem            # problem | method | concern | enabler
status: Draft            # Draft | Review | Approved | Deprecated
stage: Defined           # Defined | Exploring | Decided | In production
priority: Must           # Must | Should | Could
early_test: false        # true: nằm trong nhóm khó nhất, thử nghiệm sớm
owner: <Tên người phụ trách>
updated: 2026-09-29
---

# AIP-024 - Grounding trích dẫn pháp lý

## 1. Định nghĩa

### 1.1. Phát biểu bài toán

Mọi căn cứ pháp lý xuất hiện trong văn bản sinh ra chỉ được lấy từ kết quả truy xuất có hiệu lực, và phải trỏ tới đúng điều/khoản/điểm của đúng văn bản. Model không được tự viết số hiệu văn bản hay số điều.

**Ví dụ:** câu "theo quy định tại khoản 1 Điều ... Luật ..." trong thông báo từ chối phải khớp với một chunk trong kết quả của AIP-015. Nếu model viết một số điều không có trong kết quả truy xuất thì câu đó bị chặn.

**Phạm vi:**

- Gồm: trích dẫn chỉ từ kết quả truy xuất; gắn trích dẫn với chunk nguồn.
- Không gồm: kiểm chứng dữ kiện hồ sơ trong văn bản (AIP-025).

### 1.2. Vị trí trong luồng

**Bước:** Sinh văn bản (nhóm [AIG-08](AIG-08-legal-generation.md) - Sinh và kiểm chứng văn bản kết quả). Sơ đồ luồng xem [README](README.md).

- Dựa vào: [AIP-015](AIP-015-temporal-validity-retrieval.md) - Truy xuất theo hiệu lực thời gian; [AIP-023](AIP-023-controlled-generation.md) - Sinh văn bản kết quả có kiểm soát
- Được dùng bởi: [AIP-025](AIP-025-post-generation-verification.md) - Kiểm chứng sau sinh

### 1.3. Đầu vào và đầu ra

| | Nội dung | Ví dụ |
|---|---|---|
| Đầu vào | Kết quả truy xuất có hiệu lực (AIP-015), văn bản đang sinh (AIP-023) | - |
| Đầu ra | Trích dẫn gắn với chunk nguồn | - |

### 1.4. Ràng buộc bắt buộc

| Mã | Ràng buộc | Lý do |
|---|---|---|
| AIP-024-R01 | Căn cứ pháp lý chỉ lấy từ kết quả truy xuất, không tự sinh số điều. | Trích dẫn sai là sai căn cứ pháp lý. |

## 2. Vì sao khó

### 2.1. Thách thức

- LLM có xu hướng tự sinh số điều, số văn bản.

### 2.2. Chi phí khi sai

Trích dẫn điều luật không tồn tại hoặc sai điều.

## 3. Đánh giá

| Chỉ số | Cách đo | Ngưỡng chấp nhận |
|---|---|---|
| Tỉ lệ trích dẫn khớp kho luật | `[CẦN XÁC NHẬN]` | `[CẦN XÁC NHẬN]` |

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
| `AIP-015` | [Truy xuất theo hiệu lực thời gian](AIP-015-temporal-validity-retrieval.md) | Dựa vào | Chỉ trích dẫn điều luật từ kết quả truy xuất |
| `AIP-023` | [Sinh văn bản kết quả có kiểm soát](AIP-023-controlled-generation.md) | Dựa vào | Trích dẫn nằm trong văn bản sinh ra |
| `AIP-025` | [Kiểm chứng sau sinh](AIP-025-post-generation-verification.md) | Được dùng bởi | Kiểm chứng trích dẫn với kho luật |

## 7. Lịch sử thay đổi

| Ngày | Người sửa | Nội dung | Đã rà tham chiếu |
|---|---|---|---|
| 2026-09-28 | <Tên> | Tạo mới, định nghĩa ban đầu từ danh sách bài toán AI của luồng | Không cần |
| 2026-09-29 | binhnguyenSoftz | Tổ chức lại: đổi mã từ AIP-033 cũ; nhóm `AIG-08`, thêm `kind`; viết lại phát biểu bài toán | Có |
