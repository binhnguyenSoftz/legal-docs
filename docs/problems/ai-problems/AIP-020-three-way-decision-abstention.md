---
id: AIP-020
title: Quyết định ba lớp, abstention và ngưỡng theo chi phí lỗi
group: AIG-07
kind: problem            # problem | method | concern | enabler
status: Draft            # Draft | Review | Approved | Deprecated
stage: Defined           # Defined | Exploring | Decided | In production
priority: Must           # Must | Should | Could
early_test: true         # true: nằm trong nhóm khó nhất, thử nghiệm sớm
owner: <Tên người phụ trách>
updated: 2026-09-29
---

# AIP-020 - Quyết định ba lớp, abstention và ngưỡng theo chi phí lỗi

## 1. Định nghĩa

### 1.1. Phát biểu bài toán

Từ kết luận từng điều kiện (AIP-019), kết quả đối chiếu và độ bất định, đề xuất một trong ba lớp: chấp thuận, từ chối, cần bổ sung. Khi độ tin cậy dưới ngưỡng thì không tự quyết mà chuyển cán bộ. Ngưỡng được chọn theo chi phí của từng loại lỗi, lệch về phía an toàn cho người dân.

**Ví dụ:** hồ sơ thừa kế đủ mọi điều kiện nhưng ngày mất trên giấy chứng tử có độ tin cậy 0,55 và mâu thuẫn với tờ khai. Hệ thống không đề xuất "chấp thuận" hay "từ chối" mà chuyển cán bộ, kèm lý do "ngày mất không chắc chắn".

**Phạm vi:**

- Gồm: gộp kết luận thành đề xuất; abstention; chọn ngưỡng theo chi phí lỗi bất đối xứng.
- Không gồm: kết luận từng điều kiện (AIP-019), lời giải thích (AIP-021), nhất quán qua các lần chạy (AIP-022).

### 1.2. Vị trí trong luồng

**Bước:** Suy luận, ra quyết định (nhóm [AIG-07](AIG-07-legal-decision.md) - Suy luận pháp lý và hỗ trợ quyết định). Sơ đồ luồng xem [README](README.md).

- Dựa vào: [AIP-019](AIP-019-legal-reasoning.md) - Suy luận pháp lý; [AIP-013](AIP-013-uncertainty-propagation.md) - Ước lượng độ bất định lan truyền; [AIP-010](AIP-010-conflict-vs-error.md) - Phân biệt mâu thuẫn thật với lỗi OCR/trích xuất; [AIP-012](AIP-012-missing-document-detection.md) - Phát hiện thiếu giấy tờ
- Được dùng bởi: [AIP-022](AIP-022-decision-consistency.md) - Nhất quán kết quả; [AIP-023](AIP-023-controlled-generation.md) - Sinh văn bản kết quả có kiểm soát; [AIP-030](AIP-030-bias-fairness.md) - Bias và fairness; [AIP-033](AIP-033-review-sample-selection.md) - Chọn hồ sơ cần người duyệt

### 1.3. Đầu vào và đầu ra

| | Nội dung | Ví dụ |
|---|---|---|
| Đầu vào | Kết luận suy luận (AIP-019), độ bất định (AIP-013), kết quả đối chiếu (AIP-010), giấy tờ thiếu (AIP-012), chi phí từng loại lỗi | - |
| Đầu ra | Một trong: chấp thuận, từ chối, cần bổ sung, chuyển người; kèm điểm tin cậy và ngưỡng đã dùng | `{decision: "chuyển người", reason: "ngày mất không chắc chắn", score: 0,55}` |

### 1.4. Ràng buộc bắt buộc

| Mã | Ràng buộc | Lý do |
|---|---|---|
| AIP-020-R01 | Kết quả chỉ thuộc một trong ba lớp: chấp thuận, từ chối, cần bổ sung. | Khớp với quy trình nghiệp vụ. |
| AIP-020-R02 | Không đủ tự tin thì chuyển người, không tự quyết. | Tránh quyết định sai với người dân. |
| AIP-020-R03 | Ngưỡng lệch về phía an toàn. (Trước đây là `AIP-031-R01` cũ.) | Chi phí lỗi không đối xứng. |

### 1.5. Bài toán con

| Bài toán con | Mã cũ | Ưu tiên | Nội dung |
|---|---|---|---|
| Quyết định ba lớp và abstention | AIP-028 cũ | Must | Đề xuất lớp, biết khi nào chuyển người |
| Ngưỡng quyết định theo chi phí lỗi bất đối xứng | AIP-031 cũ | Should | Chọn ngưỡng theo chi phí từ chối oan, chấp thuận sai, chuyển người |

Bản đầu tiên có thể dùng ngưỡng đặt tay, thận trọng. Tối ưu ngưỡng theo chi phí làm sau khi có số liệu.

## 2. Vì sao khó

### 2.1. Thách thức

- Phải biết mình không biết (abstention).
- Kết hợp độ bất định từ nhiều tầng.
- Cần định lượng chi phí của từ chối oan, chấp thuận sai và chuyển người.

### 2.2. Chi phí khi sai

- Tự quyết khi không chắc gây từ chối oan hoặc chấp thuận sai. Chuyển người quá nhiều làm mất lợi ích tự động hóa.
- Ngưỡng sai làm tăng loại lỗi đắt nhất.

## 3. Đánh giá

| Chỉ số | Cách đo | Ngưỡng chấp nhận |
|---|---|---|
| Độ khớp quyết định với chuyên viên | Trên golden set AIP-026 | `[CẦN XÁC NHẬN]` |
| Tỉ lệ chuyển người | `[CẦN XÁC NHẬN]` | `[CẦN XÁC NHẬN]` |
| Tỉ lệ sai trên phần tự quyết | `[CẦN XÁC NHẬN]` | `[CẦN XÁC NHẬN]` |
| Tổng chi phí lỗi kỳ vọng | `[CẦN XÁC NHẬN]` | `[CẦN XÁC NHẬN]` |

## 4. Hướng tiếp cận và thử nghiệm

### 4.1. Hướng tiếp cận ứng viên

| Hướng | Ưu điểm | Nhược điểm |
|---|---|---|
| `[CẦN XÁC NHẬN]` Chưa khảo sát thêm | | |

### 4.2. Dữ liệu cần chuẩn bị

- Hồ sơ đã có quyết định của chuyên viên.
- Ước lượng chi phí từng loại lỗi cho từng thủ tục.

### 4.3. Nhật ký thử nghiệm

| Ngày | Thử nghiệm | Kết quả | Kết luận |
|---|---|---|---|
| | | | |

## 5. Câu hỏi còn mở

- [ ] Tỉ lệ chuyển người chấp nhận được là bao nhiêu?
- [ ] Với thủ tục này, lỗi nào đắt hơn: từ chối oan hay chấp thuận sai?

## 6. Tài liệu tham chiếu

Quy tắc ghi: `standards/07-references.md`.

| Mã | Tài liệu | Chiều | Nội dung liên quan |
|---|---|---|---|
| `AIP-019` | [Suy luận pháp lý](AIP-019-legal-reasoning.md) | Dựa vào | Ra quyết định từ kết luận từng điều kiện |
| `AIP-013` | [Ước lượng độ bất định lan truyền](AIP-013-uncertainty-propagation.md) | Dựa vào | Dùng độ bất định để quyết định chuyển người |
| `AIP-010` | [Phân biệt mâu thuẫn thật với lỗi OCR/trích xuất](AIP-010-conflict-vs-error.md) | Dựa vào | Mâu thuẫn thật ảnh hưởng tới quyết định |
| `AIP-012` | [Phát hiện thiếu giấy tờ](AIP-012-missing-document-detection.md) | Dựa vào | Thiếu giấy tờ dẫn tới lớp "cần bổ sung" |
| `AIP-022` | [Nhất quán kết quả](AIP-022-decision-consistency.md) | Được dùng bởi | Quyết định phải ổn định qua các lần chạy |
| `AIP-023` | [Sinh văn bản kết quả có kiểm soát](AIP-023-controlled-generation.md) | Được dùng bởi | Sinh văn bản theo quyết định đã chốt |
| `AIP-030` | [Bias và fairness](AIP-030-bias-fairness.md) | Được dùng bởi | Đo tỉ lệ từ chối theo nhóm |
| `AIP-033` | [Chọn hồ sơ cần người duyệt](AIP-033-review-sample-selection.md) | Được dùng bởi | Chọn hồ sơ có độ tin cậy thấp cho người duyệt |

## 7. Lịch sử thay đổi

| Ngày | Người sửa | Nội dung | Đã rà tham chiếu |
|---|---|---|---|
| 2026-09-28 | <Tên> | Tạo mới, định nghĩa ban đầu từ danh sách bài toán AI của luồng | Không cần |
| 2026-09-29 | binhnguyenSoftz | Tổ chức lại: gộp AIP-028 cũ (quyết định ba lớp) và AIP-031 cũ (ngưỡng theo chi phí lỗi), `AIP-031-R01` cũ thành `AIP-020-R03`; nhóm `AIG-07`; viết lại phát biểu bài toán | Có |
