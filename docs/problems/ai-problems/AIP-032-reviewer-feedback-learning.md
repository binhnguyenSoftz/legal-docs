---
id: AIP-032
title: Học từ chỉnh sửa của cán bộ duyệt
group: AIG-11
kind: enabler            # problem | method | concern | enabler
status: Draft            # Draft | Review | Approved | Deprecated
stage: Defined           # Defined | Exploring | Decided | In production
priority: Should         # Must | Should | Could
early_test: false        # true: nằm trong nhóm khó nhất, thử nghiệm sớm
owner: <Tên người phụ trách>
updated: 2026-09-29
---

# AIP-032 - Học từ chỉnh sửa của cán bộ duyệt

## 1. Định nghĩa

### 1.1. Phát biểu bài toán

Ghi lại mọi chỉnh sửa của cán bộ duyệt trên kết quả hệ thống (sửa giá trị trường, đổi quyết định, sửa văn bản), lọc chỉnh sửa đáng tin, rồi dùng làm dữ liệu đánh giá và cải tiến. Từ phân tích lỗi, quyết định cách cải tiến: sửa prompt, sửa retrieval, hay fine-tune model.

**Ví dụ:** trong một tháng, cán bộ sửa trường `ngay_mat` trên 40 giấy chứng tử viết tay, phần lớn do đọc nhầm năm. Các cặp (giá trị hệ thống, giá trị cán bộ sửa) được thêm vào golden set AIP-026. Phân tích cho thấy lỗi nằm ở OCR, không ở prompt trích xuất, nên đề xuất fine-tune OCR và ghi quyết định thành ADR.

**Phạm vi:**

- Gồm: thu thập, lọc chỉnh sửa; đưa vào golden set, dữ liệu huấn luyện; quyết định fine-tune hay cải thiện prompt/retrieval.
- Không gồm: chọn hồ sơ nào cần người duyệt (AIP-033), phát hiện drift (AIP-036).

### 1.2. Vị trí trong luồng

**Bước:** Xuyên suốt: học từ phản hồi (nhóm [AIG-11](AIG-11-feedback-learning.md) - Học từ phản hồi và cải tiến liên tục). Sơ đồ luồng xem [README](README.md).

- Dựa vào: [AIP-026](AIP-026-layered-golden-set.md) - Golden set và metric theo từng tầng
- Được dùng bởi: [AIP-033](AIP-033-review-sample-selection.md) - Chọn hồ sơ cần người duyệt

### 1.3. Đầu vào và đầu ra

| | Nội dung | Ví dụ |
|---|---|---|
| Đầu vào | Chỉnh sửa của cán bộ trên kết quả hệ thống; phân tích lỗi; chi phí | Log sửa trường `ngay_mat` |
| Đầu ra | Dữ liệu bổ sung golden set và huấn luyện; quyết định cách cải tiến, ghi thành ADR | ADR "Fine-tune OCR cho giấy chứng tử viết tay" |

### 1.4. Ràng buộc bắt buộc

Chưa có. Bổ sung khi đi sâu vào bài toán, đánh mã `AIP-032-R01`, `R02`...

### 1.5. Bài toán con

| Bài toán con | Mã cũ | Ưu tiên | Nội dung |
|---|---|---|---|
| Học từ chỉnh sửa của cán bộ duyệt | AIP-043 cũ | Should | Dùng chỉnh sửa làm dữ liệu huấn luyện và đánh giá (active learning) |
| Fine-tune hay cải thiện prompt/retrieval | AIP-045 cũ | Could | Chọn cách cải tiến dựa trên phân tích lỗi và dữ liệu có sẵn |

## 2. Vì sao khó

### 2.1. Thách thức

- Chỉnh sửa của cán bộ có thể không nhất quán.
- Fine-tune tốn dữ liệu và công vận hành.

### 2.2. Chi phí khi sai

- Học từ nhãn sai làm model tệ đi.
- Fine-tune không cần thiết tốn chi phí. Không fine-tune khi cần thì chất lượng dậm chân.

## 3. Đánh giá

| Chỉ số | Cách đo | Ngưỡng chấp nhận |
|---|---|---|
| Mức cải thiện metric sau mỗi vòng cải tiến | So metric trên golden set AIP-026 trước và sau | `[CẦN XÁC NHẬN]` |
| Tỉ lệ chỉnh sửa bị loại vì không nhất quán | `[CẦN XÁC NHẬN]` | `[CẦN XÁC NHẬN]` |

## 4. Hướng tiếp cận và thử nghiệm

### 4.1. Hướng tiếp cận ứng viên

| Hướng | Ưu điểm | Nhược điểm |
|---|---|---|
| Active learning | `[CẦN XÁC NHẬN]` | `[CẦN XÁC NHẬN]` |
| `[CẦN XÁC NHẬN]` Chưa khảo sát thêm | | |

### 4.2. Dữ liệu cần chuẩn bị

- Log chỉnh sửa của cán bộ.

### 4.3. Nhật ký thử nghiệm

| Ngày | Thử nghiệm | Kết quả | Kết luận |
|---|---|---|---|
| | | | |

## 5. Câu hỏi còn mở

- [ ] Giao diện duyệt có lưu lại chỉnh sửa theo từng trường không?

## 6. Tài liệu tham chiếu

Quy tắc ghi: `standards/07-references.md`.

| Mã | Tài liệu | Chiều | Nội dung liên quan |
|---|---|---|---|
| `AIP-026` | [Golden set và metric theo từng tầng](AIP-026-layered-golden-set.md) | Dựa vào | Bổ sung chỉnh sửa của cán bộ vào golden set |
| `AIP-033` | [Chọn hồ sơ cần người duyệt](AIP-033-review-sample-selection.md) | Được dùng bởi | Hồ sơ được duyệt trở thành dữ liệu huấn luyện |

## 7. Lịch sử thay đổi

| Ngày | Người sửa | Nội dung | Đã rà tham chiếu |
|---|---|---|---|
| 2026-09-28 | <Tên> | Tạo mới, định nghĩa ban đầu từ danh sách bài toán AI của luồng | Không cần |
| 2026-09-29 | binhnguyenSoftz | Tổ chức lại: gộp AIP-043 cũ (học từ chỉnh sửa) và AIP-045 cũ (fine-tune hay prompt); nhóm `AIG-11`; viết lại phát biểu bài toán | Có |
