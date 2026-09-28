---
id: AIP-033
title: Chọn hồ sơ cần người duyệt
group: AIG-11
kind: problem            # problem | method | concern | enabler
status: Draft            # Draft | Review | Approved | Deprecated
stage: Defined           # Defined | Exploring | Decided | In production
priority: Could          # Must | Should | Could
early_test: false        # true: nằm trong nhóm khó nhất, thử nghiệm sớm
owner: <Tên người phụ trách>
updated: 2026-09-29
---

# AIP-033 - Chọn hồ sơ cần người duyệt

## 1. Định nghĩa

### 1.1. Phát biểu bài toán

Trong số hồ sơ hệ thống đã xử lý, chọn hồ sơ nào đưa cán bộ duyệt kỹ để vừa bắt lỗi vừa thu được nhiều thông tin nhất cho cải tiến, trong giới hạn thời gian của cán bộ.

**Ví dụ:** mỗi ngày cán bộ duyệt kỹ được 30 hồ sơ. Hệ thống chọn: mọi hồ sơ độ tin cậy dưới ngưỡng, cộng một mẫu ngẫu nhiên hồ sơ độ tin cậy cao để kiểm tra lỗi "tự tin mà sai".

**Phạm vi:**

- Gồm: tiêu chí chọn hồ sơ; cân bằng giữa bắt lỗi và thu dữ liệu.
- Không gồm: học từ chỉnh sửa của cán bộ (AIP-032).

### 1.2. Vị trí trong luồng

**Bước:** Xuyên suốt: học từ phản hồi (nhóm [AIG-11](AIG-11-feedback-learning.md) - Học từ phản hồi và cải tiến liên tục). Sơ đồ luồng xem [README](README.md).

- Dựa vào: [AIP-020](AIP-020-three-way-decision-abstention.md) - Quyết định ba lớp, abstention và ngưỡng theo chi phí lỗi; [AIP-032](AIP-032-reviewer-feedback-learning.md) - Học từ chỉnh sửa của cán bộ duyệt
- Được dùng bởi: không có.

### 1.3. Đầu vào và đầu ra

| | Nội dung | Ví dụ |
|---|---|---|
| Đầu vào | Hồ sơ và độ tin cậy của hệ thống | - |
| Đầu ra | Danh sách hồ sơ ưu tiên duyệt | - |

### 1.4. Ràng buộc bắt buộc

Chưa có. Bổ sung khi đi sâu vào bài toán, đánh mã `AIP-033-R01`, `R02`...

## 2. Vì sao khó

### 2.1. Thách thức

- Cân bằng giữa nhu cầu vận hành và nhu cầu thu dữ liệu.

### 2.2. Chi phí khi sai

Chọn sai thì tốn công duyệt mà không cải thiện được model.

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
| `AIP-020` | [Quyết định ba lớp, abstention và ngưỡng theo chi phí lỗi](AIP-020-three-way-decision-abstention.md) | Dựa vào | Chọn hồ sơ có độ tin cậy thấp cho người duyệt |
| `AIP-032` | [Học từ chỉnh sửa của cán bộ duyệt](AIP-032-reviewer-feedback-learning.md) | Dựa vào | Hồ sơ được duyệt trở thành dữ liệu huấn luyện |

## 7. Lịch sử thay đổi

| Ngày | Người sửa | Nội dung | Đã rà tham chiếu |
|---|---|---|---|
| 2026-09-28 | <Tên> | Tạo mới, định nghĩa ban đầu từ danh sách bài toán AI của luồng | Không cần |
| 2026-09-29 | binhnguyenSoftz | Tổ chức lại: đổi mã từ AIP-044 cũ; nhóm `AIG-11`, thêm `kind`; viết lại phát biểu bài toán | Có |
