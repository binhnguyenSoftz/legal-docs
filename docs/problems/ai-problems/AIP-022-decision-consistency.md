---
id: AIP-022
title: Nhất quán kết quả
group: AIG-07
kind: concern            # problem | method | concern | enabler
status: Draft            # Draft | Review | Approved | Deprecated
stage: Defined           # Defined | Exploring | Decided | In production
priority: Should         # Must | Should | Could
early_test: false        # true: nằm trong nhóm khó nhất, thử nghiệm sớm
owner: <Tên người phụ trách>
updated: 2026-09-29
---

# AIP-022 - Nhất quán kết quả

## 1. Định nghĩa

### 1.1. Phát biểu bài toán

Cùng một hồ sơ, cùng cấu hình, chạy nhiều lần phải ra cùng quyết định. Hai hồ sơ giống nhau về bản chất phải ra quyết định giống nhau. Đo và giảm độ dao động do tính ngẫu nhiên của LLM.

**Ví dụ:** chạy lại một hồ sơ 10 lần, 9 lần "chấp thuận", 1 lần "cần bổ sung". Đây là lỗi nhất quán, cần tìm bước gây dao động (thường là phần LLM diễn giải) và cố định lại.

**Phạm vi:**

- Gồm: đo độ ổn định qua nhiều lần chạy; cố định cấu hình, giảm dao động.
- Không gồm: regression khi đổi phiên bản (AIP-028).

### 1.2. Vị trí trong luồng

**Bước:** Suy luận, ra quyết định (nhóm [AIG-07](AIG-07-legal-decision.md) - Suy luận pháp lý và hỗ trợ quyết định). Sơ đồ luồng xem [README](README.md).

- Dựa vào: [AIP-020](AIP-020-three-way-decision-abstention.md) - Quyết định ba lớp, abstention và ngưỡng theo chi phí lỗi
- Được dùng bởi: không có.

### 1.3. Đầu vào và đầu ra

| | Nội dung | Ví dụ |
|---|---|---|
| Đầu vào | Hồ sơ và cấu hình pipeline | - |
| Đầu ra | Quyết định ổn định qua các lần chạy | - |

### 1.4. Ràng buộc bắt buộc

| Mã | Ràng buộc | Lý do |
|---|---|---|
| AIP-022-R01 | Cùng hồ sơ, cùng phiên bản model, prompt và luật thì phải ra cùng quyết định. | Công bằng và kiểm tra lại được. |

## 2. Vì sao khó

### 2.1. Thách thức

- LLM không tất định.
- Cần kiểm soát bằng cấu hình và self-consistency.

### 2.2. Chi phí khi sai

Hai lần chạy ra hai kết quả khác nhau làm mất niềm tin vào hệ thống.

## 3. Đánh giá

| Chỉ số | Cách đo | Ngưỡng chấp nhận |
|---|---|---|
| Tỉ lệ hồ sơ có kết quả khác nhau giữa N lần chạy | `[CẦN XÁC NHẬN]` | `[CẦN XÁC NHẬN]` |

## 4. Hướng tiếp cận và thử nghiệm

### 4.1. Hướng tiếp cận ứng viên

| Hướng | Ưu điểm | Nhược điểm |
|---|---|---|
| Self-consistency | `[CẦN XÁC NHẬN]` | `[CẦN XÁC NHẬN]` |
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
| `AIP-020` | [Quyết định ba lớp, abstention và ngưỡng theo chi phí lỗi](AIP-020-three-way-decision-abstention.md) | Dựa vào | Quyết định phải ổn định qua các lần chạy |

## 7. Lịch sử thay đổi

| Ngày | Người sửa | Nội dung | Đã rà tham chiếu |
|---|---|---|---|
| 2026-09-28 | <Tên> | Tạo mới, định nghĩa ban đầu từ danh sách bài toán AI của luồng | Không cần |
| 2026-09-29 | binhnguyenSoftz | Tổ chức lại: đổi mã từ AIP-030 cũ; nhóm `AIG-07`, thêm `kind`; viết lại phát biểu bài toán | Có |
