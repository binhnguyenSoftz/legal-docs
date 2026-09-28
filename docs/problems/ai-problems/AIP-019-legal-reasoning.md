---
id: AIP-019
title: Suy luận pháp lý
group: AIG-07
kind: problem            # problem | method | concern | enabler
status: Draft            # Draft | Review | Approved | Deprecated
stage: Defined           # Defined | Exploring | Decided | In production
priority: Must           # Must | Should | Could
early_test: false        # true: nằm trong nhóm khó nhất, thử nghiệm sớm
owner: <Tên người phụ trách>
updated: 2026-09-29
---

# AIP-019 - Suy luận pháp lý

## 1. Định nghĩa

### 1.1. Phát biểu bài toán

Với từng điều kiện mà điều khoản đặt ra, đối chiếu dữ kiện của hồ sơ và kết luận đạt, không đạt hoặc chưa rõ, kèm căn cứ. Điều kiện xác định được bằng code (so ngày, đủ giấy tờ) thì chạy bằng rule; LLM chỉ xử lý phần cần diễn giải.

**Ví dụ:** điều kiện "người nhận thừa kế thuộc hàng thừa kế thứ nhất": rule kiểm tra quan hệ "con" từ AIP-009, kết luận đạt. Điều kiện "đất không có tranh chấp": cần đọc văn bản xác nhận của UBND xã, giao LLM diễn giải, kết luận chưa rõ vì văn bản ghi "chưa phát hiện tranh chấp".

**Phạm vi:**

- Gồm: kết luận từng điều kiện; tách phần rule và phần LLM (neuro-symbolic).
- Không gồm: gộp kết luận thành quyết định (AIP-020), viết lời giải thích (AIP-021).

### 1.2. Vị trí trong luồng

**Bước:** Suy luận, ra quyết định (nhóm [AIG-07](AIG-07-legal-decision.md) - Suy luận pháp lý và hỗ trợ quyết định). Sơ đồ luồng xem [README](README.md).

- Dựa vào: [AIP-015](AIP-015-temporal-validity-retrieval.md) - Truy xuất theo hiệu lực thời gian; [AIP-017](AIP-017-legal-conflict-resolution.md) - Giải quyết xung đột giữa văn bản; [AIP-011](AIP-011-temporal-numeric-reasoning.md) - Suy luận thời gian và số học trên dữ liệu trích xuất
- Được dùng bởi: [AIP-020](AIP-020-three-way-decision-abstention.md) - Quyết định ba lớp, abstention và ngưỡng theo chi phí lỗi; [AIP-021](AIP-021-explainability-faithfulness.md) - Giải thích và faithfulness

### 1.3. Đầu vào và đầu ra

| | Nội dung | Ví dụ |
|---|---|---|
| Đầu vào | Sự kiện đã đối chiếu, điều khoản có hiệu lực (AIP-015), kết quả tính toán (AIP-011) | - |
| Đầu ra | Kết luận từng điều kiện đạt / không đạt / chưa rõ, kèm căn cứ | - |

### 1.4. Ràng buộc bắt buộc

| Mã | Ràng buộc | Lý do |
|---|---|---|
| AIP-019-R01 | Điều kiện xác định được bằng code thì chạy bằng rule engine/code. LLM chỉ xử lý phần cần diễn giải. (Trước đây là `AIP-027-R01` cũ.) | Kết quả chính xác, lặp lại được, kiểm thử được. |

## 2. Vì sao khó

### 2.1. Thách thức

- Điều kiện lồng nhau.
- Ngoại lệ.
- Quy định mơ hồ.
- Xác định ranh giới giữa phần xác định (chạy bằng code) và phần cần diễn giải (giao LLM).
- Giữ rule khớp với luật khi luật thay đổi.

### 2.2. Chi phí khi sai

- Áp sai điều kiện dẫn tới quyết định sai.
- Giao phần xác định cho LLM làm mất tính nhất quán.

## 3. Đánh giá

| Chỉ số | Cách đo | Ngưỡng chấp nhận |
|---|---|---|
| Độ khớp với chuyên viên theo từng điều kiện | Trên golden set AIP-026 | `[CẦN XÁC NHẬN]` |
| Tỉ lệ điều kiện xác định được chạy bằng code | Đếm trên danh sách điều kiện của thủ tục | `[CẦN XÁC NHẬN]` |

## 4. Hướng tiếp cận và thử nghiệm

### 4.1. Hướng tiếp cận ứng viên

| Hướng | Ưu điểm | Nhược điểm |
|---|---|---|
| Neuro-symbolic: rule engine/code cho điều kiện xác định, LLM cho phần cần diễn giải (từ AIP-027 cũ) | Phần xác định chính xác, lặp lại được, kiểm thử được | Phải bảo trì bộ rule theo luật; khó chốt ranh giới hai phần |
| `[CẦN XÁC NHẬN]` Chưa khảo sát thêm | | |

Với hướng neuro-symbolic, đầu ra trung gian là bộ rule chạy bằng code và danh sách phần giao cho LLM, lập từ điều khoản pháp luật của thủ tục.

### 4.2. Dữ liệu cần chuẩn bị

- Hồ sơ đã được chuyên viên kết luận theo từng điều kiện.
- Danh sách điều kiện của thủ tục, đánh dấu điều kiện nào xác định được bằng code.

### 4.3. Nhật ký thử nghiệm

| Ngày | Thử nghiệm | Kết quả | Kết luận |
|---|---|---|---|
| | | | |

## 5. Câu hỏi còn mở

- [ ] Dùng rule engine nào hay tự viết?

## 6. Tài liệu tham chiếu

Quy tắc ghi: `standards/07-references.md`.

| Mã | Tài liệu | Chiều | Nội dung liên quan |
|---|---|---|---|
| `AIP-015` | [Truy xuất theo hiệu lực thời gian](AIP-015-temporal-validity-retrieval.md) | Dựa vào | Áp dụng điều khoản có hiệu lực |
| `AIP-017` | [Giải quyết xung đột giữa văn bản](AIP-017-legal-conflict-resolution.md) | Dựa vào | Dùng quy định được chọn khi có xung đột |
| `AIP-011` | [Suy luận thời gian và số học trên dữ liệu trích xuất](AIP-011-temporal-numeric-reasoning.md) | Dựa vào | Giao phần tính toán thời gian, số học cho code |
| `AIP-020` | [Quyết định ba lớp, abstention và ngưỡng theo chi phí lỗi](AIP-020-three-way-decision-abstention.md) | Được dùng bởi | Ra quyết định từ kết luận từng điều kiện |
| `AIP-021` | [Giải thích và faithfulness](AIP-021-explainability-faithfulness.md) | Được dùng bởi | Lập luận phải khớp cơ sở quyết định |

## 7. Lịch sử thay đổi

| Ngày | Người sửa | Nội dung | Đã rà tham chiếu |
|---|---|---|---|
| 2026-09-28 | <Tên> | Tạo mới, định nghĩa ban đầu từ danh sách bài toán AI của luồng | Không cần |
| 2026-09-29 | binhnguyenSoftz | Tổ chức lại: đổi mã từ AIP-026 cũ, gộp AIP-027 cũ (neuro-symbolic) vào mục 1.4, 2, 4.1, `AIP-027-R01` cũ thành `AIP-019-R01`; nhóm `AIG-07`; viết lại phát biểu bài toán | Có |
