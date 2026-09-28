---
id: AIP-011
title: Suy luận thời gian và số học trên dữ liệu trích xuất
group: AIG-05
kind: method             # problem | method | concern | enabler
status: Draft            # Draft | Review | Approved | Deprecated
stage: Defined           # Defined | Exploring | Decided | In production
priority: Must           # Must | Should | Could
early_test: false        # true: nằm trong nhóm khó nhất, thử nghiệm sớm
owner: <Tên người phụ trách>
updated: 2026-09-29
---

# AIP-011 - Suy luận thời gian và số học trên dữ liệu trích xuất

## 1. Định nghĩa

### 1.1. Phát biểu bài toán

Tính các giá trị ngày tháng, tuổi, thời hạn, diện tích, số tiền trên dữ liệu đã trích xuất và kiểm tra các điều kiện so sánh (trước/sau, đủ tuổi, còn hạn). Phần này chạy bằng code hoặc rule engine, không giao LLM tính.

**Ví dụ:** ngày mất `2019-03-12`, ngày nộp hồ sơ `2026-09-01`: kiểm tra thời hiệu yêu cầu chia di sản. Tổng diện tích các thửa trên giấy chứng nhận `98,5 + 45,0 = 143,5 m²` phải khớp bản vẽ hiện trạng, lệch quá sai số cho phép thì báo.

**Phạm vi:**

- Gồm: tính ngày, tuổi, thời hạn, tổng, hiệu; kiểm tra điều kiện so sánh.
- Không gồm: quyết định giá trị nào đúng khi hai nguồn khác nhau (AIP-010).

### 1.2. Vị trí trong luồng

**Bước:** Đối chiếu chéo (nhóm [AIG-05](AIG-05-cross-document-validation.md) - Đối chiếu và kiểm tra chéo giấy tờ). Sơ đồ luồng xem [README](README.md).

- Dựa vào: [AIP-005](AIP-005-schema-extraction.md) - Trích xuất theo schema và sửa lỗi OCR
- Được dùng bởi: [AIP-019](AIP-019-legal-reasoning.md) - Suy luận pháp lý

### 1.3. Đầu vào và đầu ra

| | Nội dung | Ví dụ |
|---|---|---|
| Đầu vào | Dữ liệu đã trích xuất và chuẩn hóa | Ngày sinh và ngày nộp hồ sơ |
| Đầu ra | Kết quả tính toán dùng cho đối chiếu và suy luận | Tuổi tại ngày nộp: 39 |

### 1.4. Ràng buộc bắt buộc

| Mã | Ràng buộc | Lý do |
|---|---|---|
| AIP-011-R01 | Phép tính thời gian và số học do code thực hiện, không giao cho LLM. | LLM tính sai và không ổn định. |

## 2. Vì sao khó

### 2.1. Thách thức

- LLM thường yếu ở suy luận thời gian và số học.

### 2.2. Chi phí khi sai

Tính sai tuổi hoặc thời hạn dẫn tới áp sai điều kiện.

## 3. Đánh giá

| Chỉ số | Cách đo | Ngưỡng chấp nhận |
|---|---|---|
| Tỉ lệ tính đúng | Có thể kiểm tra tuyệt đối bằng unit test | `[CẦN XÁC NHẬN]` |

## 4. Hướng tiếp cận và thử nghiệm

### 4.1. Hướng tiếp cận ứng viên

| Hướng | Ưu điểm | Nhược điểm |
|---|---|---|
| Code thuần | Chính xác, kiểm thử được | Phải chuẩn hóa dữ liệu đầu vào |
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
| `AIP-005` | [Trích xuất theo schema và sửa lỗi OCR](AIP-005-schema-extraction.md) | Dựa vào | Tính trên dữ liệu đã trích xuất |
| `AIP-019` | [Suy luận pháp lý](AIP-019-legal-reasoning.md) | Được dùng bởi | Giao phần tính toán thời gian, số học cho code |

## 7. Lịch sử thay đổi

| Ngày | Người sửa | Nội dung | Đã rà tham chiếu |
|---|---|---|---|
| 2026-09-28 | <Tên> | Tạo mới, định nghĩa ban đầu từ danh sách bài toán AI của luồng | Không cần |
| 2026-09-29 | binhnguyenSoftz | Tổ chức lại: đổi mã từ AIP-017 cũ; nhóm `AIG-05`, thêm `kind`; viết lại phát biểu bài toán | Có |
