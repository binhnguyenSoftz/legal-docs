---
id: AIP-012
title: Phát hiện thiếu giấy tờ
group: AIG-05
kind: problem            # problem | method | concern | enabler
status: Draft            # Draft | Review | Approved | Deprecated
stage: Defined           # Defined | Exploring | Decided | In production
priority: Must           # Must | Should | Could
early_test: false        # true: nằm trong nhóm khó nhất, thử nghiệm sớm
owner: <Tên người phụ trách>
updated: 2026-09-29
---

# AIP-012 - Phát hiện thiếu giấy tờ

## 1. Định nghĩa

### 1.1. Phát biểu bài toán

So danh sách giấy tờ đã nộp (sau phân loại) với thành phần hồ sơ bắt buộc của thủ tục tại thời điểm nộp, tìm giấy tờ còn thiếu. Tính cả điều kiện kèm theo, ví dụ "nếu người để lại di sản đã mất thì phải có giấy chứng tử".

**Ví dụ:** hồ sơ đăng ký biến động do thừa kế có tờ khai, giấy chứng nhận, CCCD của người thừa kế, nhưng không có giấy chứng tử và văn bản khai nhận di sản. Kết quả: thiếu 2 giấy tờ, dẫn tới lớp quyết định "cần bổ sung".

**Phạm vi:**

- Gồm: so thành phần hồ sơ; điều kiện kèm theo.
- Không gồm: xác định loại giấy tờ (AIP-004), tìm thành phần hồ sơ trong văn bản luật (AIP-015).

### 1.2. Vị trí trong luồng

**Bước:** Đối chiếu chéo (nhóm [AIG-05](AIG-05-cross-document-validation.md) - Đối chiếu và kiểm tra chéo giấy tờ). Sơ đồ luồng xem [README](README.md).

- Dựa vào: [AIP-004](AIP-004-document-classification-splitting.md) - Phân loại và tách giấy tờ; [AIP-015](AIP-015-temporal-validity-retrieval.md) - Truy xuất theo hiệu lực thời gian
- Được dùng bởi: [AIP-020](AIP-020-three-way-decision-abstention.md) - Quyết định ba lớp, abstention và ngưỡng theo chi phí lỗi

### 1.3. Đầu vào và đầu ra

| | Nội dung | Ví dụ |
|---|---|---|
| Đầu vào | Loại giấy tờ đã phân loại (AIP-004), yêu cầu thủ tục có hiệu lực (AIP-015) | - |
| Đầu ra | Danh sách giấy tờ còn thiếu | - |

### 1.4. Ràng buộc bắt buộc

Chưa có. Bổ sung khi đi sâu vào bài toán, đánh mã `AIP-012-R01`, `R02`...

## 2. Vì sao khó

### 2.1. Thách thức

- Yêu cầu có thể phụ thuộc điều kiện của từng hồ sơ.

### 2.2. Chi phí khi sai

Báo thiếu sai thì người dân phải nộp lại không cần thiết.

## 3. Đánh giá

| Chỉ số | Cách đo | Ngưỡng chấp nhận |
|---|---|---|
| Precision / recall giấy tờ còn thiếu | `[CẦN XÁC NHẬN]` | `[CẦN XÁC NHẬN]` |

## 4. Hướng tiếp cận và thử nghiệm

### 4.1. Hướng tiếp cận ứng viên

| Hướng | Ưu điểm | Nhược điểm |
|---|---|---|
| `[CẦN XÁC NHẬN]` Chưa khảo sát thêm | | |

### 4.2. Dữ liệu cần chuẩn bị

- Danh mục giấy tờ theo từng thủ tục.

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
| `AIP-004` | [Phân loại và tách giấy tờ](AIP-004-document-classification-splitting.md) | Dựa vào | Đếm loại giấy tờ đã phân loại |
| `AIP-015` | [Truy xuất theo hiệu lực thời gian](AIP-015-temporal-validity-retrieval.md) | Dựa vào | Lấy danh mục giấy tờ theo quy định có hiệu lực |
| `AIP-020` | [Quyết định ba lớp, abstention và ngưỡng theo chi phí lỗi](AIP-020-three-way-decision-abstention.md) | Được dùng bởi | Thiếu giấy tờ dẫn tới lớp "cần bổ sung" |

## 7. Lịch sử thay đổi

| Ngày | Người sửa | Nội dung | Đã rà tham chiếu |
|---|---|---|---|
| 2026-09-28 | <Tên> | Tạo mới, định nghĩa ban đầu từ danh sách bài toán AI của luồng | Không cần |
| 2026-09-29 | binhnguyenSoftz | Tổ chức lại: đổi mã từ AIP-018 cũ; nhóm `AIG-05`, thêm `kind`; viết lại phát biểu bài toán | Có |
