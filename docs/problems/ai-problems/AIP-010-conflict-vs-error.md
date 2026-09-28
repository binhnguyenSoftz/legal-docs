---
id: AIP-010
title: Phân biệt mâu thuẫn thật với lỗi OCR/trích xuất
group: AIG-05
kind: problem            # problem | method | concern | enabler
status: Draft            # Draft | Review | Approved | Deprecated
stage: Defined           # Defined | Exploring | Decided | In production
priority: Must           # Must | Should | Could
early_test: true         # true: nằm trong nhóm khó nhất, thử nghiệm sớm
owner: <Tên người phụ trách>
updated: 2026-09-29
---

# AIP-010 - Phân biệt mâu thuẫn thật với lỗi OCR/trích xuất

## 1. Định nghĩa

### 1.1. Phát biểu bài toán

Khi cùng một trường có giá trị khác nhau giữa hai giấy tờ, xác định đó là mâu thuẫn thật trong hồ sơ (giấy tờ ghi khác nhau thật) hay chỉ là lỗi đọc/trích xuất. Phân biệt dựa trên độ tin cậy, vị trí nguồn và kiểu sai (ví dụ `3` và `8` dễ nhầm khi viết tay).

**Ví dụ:** CCCD ghi ngày sinh `12/03/1985` (điểm 0,98), tờ khai viết tay ghi `12/08/1985` (điểm 0,61). Hai chữ số `3` và `8` dễ nhầm, điểm tờ khai thấp. Kết luận: nhiều khả năng lỗi đọc, không phải mâu thuẫn thật, kèm hai vùng ảnh để cán bộ xem.

**Phạm vi:**

- Gồm: so giá trị cùng trường giữa các giấy tờ; kết luận mâu thuẫn thật / lỗi đọc / chưa chắc.
- Không gồm: tính toán thời gian, số học (AIP-011), phát hiện thiếu giấy tờ (AIP-012).

### 1.2. Vị trí trong luồng

**Bước:** Đối chiếu chéo (nhóm [AIG-05](AIG-05-cross-document-validation.md) - Đối chiếu và kiểm tra chéo giấy tờ). Sơ đồ luồng xem [README](README.md).

- Dựa vào: [AIP-002](AIP-002-ocr-confidence-calibration.md) - Hiệu chỉnh độ tin cậy theo từng trường; [AIP-006](AIP-006-extraction-grounding.md) - Grounding và chống bịa khi trích xuất; [AIP-007](AIP-007-person-matching.md) - Khớp cùng một người qua nhiều giấy tờ
- Được dùng bởi: [AIP-013](AIP-013-uncertainty-propagation.md) - Ước lượng độ bất định lan truyền; [AIP-020](AIP-020-three-way-decision-abstention.md) - Quyết định ba lớp, abstention và ngưỡng theo chi phí lỗi

### 1.3. Đầu vào và đầu ra

| | Nội dung | Ví dụ |
|---|---|---|
| Đầu vào | Các giá trị cùng một trường từ nhiều giấy tờ, độ tin cậy đã hiệu chỉnh (AIP-002), vị trí nguồn (AIP-006) | Ngày sinh `12/03/1985` và `12/08/1985` |
| Đầu ra | Kết luận: mâu thuẫn thật / lỗi đọc / chưa chắc, kèm bằng chứng | - |

### 1.4. Ràng buộc bắt buộc

Chưa có. Bổ sung khi đi sâu vào bài toán, đánh mã `AIP-010-R01`, `R02`...

## 2. Vì sao khó

### 2.1. Thách thức

- Đây là bài toán quyết định việc hồ sơ có bị từ chối oan hay không.
- Lỗi OCR và mâu thuẫn thật trông giống nhau ở mức dữ liệu.

### 2.2. Chi phí khi sai

Coi lỗi OCR là mâu thuẫn thì từ chối oan. Coi mâu thuẫn thật là lỗi OCR thì chấp thuận hồ sơ sai.

## 3. Đánh giá

| Chỉ số | Cách đo | Ngưỡng chấp nhận |
|---|---|---|
| Precision / recall phát hiện mâu thuẫn thật | Trên golden set AIP-026 | `[CẦN XÁC NHẬN]` |
| Tỉ lệ từ chối oan do lỗi OCR | `[CẦN XÁC NHẬN]` | `[CẦN XÁC NHẬN]` |

## 4. Hướng tiếp cận và thử nghiệm

### 4.1. Hướng tiếp cận ứng viên

| Hướng | Ưu điểm | Nhược điểm |
|---|---|---|
| `[CẦN XÁC NHẬN]` Chưa khảo sát thêm | | |

### 4.2. Dữ liệu cần chuẩn bị

- Hồ sơ có nhãn mâu thuẫn thật và hồ sơ có lỗi OCR gây lệch.

### 4.3. Nhật ký thử nghiệm

| Ngày | Thử nghiệm | Kết quả | Kết luận |
|---|---|---|---|
| | | | |

## 5. Câu hỏi còn mở

- [ ] Khi kết luận "chưa chắc" thì chuyển người duyệt hay yêu cầu người dân bổ sung?

## 6. Tài liệu tham chiếu

Quy tắc ghi: `standards/07-references.md`.

| Mã | Tài liệu | Chiều | Nội dung liên quan |
|---|---|---|---|
| `AIP-002` | [Hiệu chỉnh độ tin cậy theo từng trường](AIP-002-ocr-confidence-calibration.md) | Dựa vào | Dùng độ tin cậy đã hiệu chỉnh để nhận ra lỗi OCR |
| `AIP-006` | [Grounding và chống bịa khi trích xuất](AIP-006-extraction-grounding.md) | Dựa vào | Truy lại vùng ảnh nguồn khi hai giá trị lệch nhau |
| `AIP-007` | [Khớp cùng một người qua nhiều giấy tờ](AIP-007-person-matching.md) | Dựa vào | So sánh dữ liệu của cùng một người |
| `AIP-013` | [Ước lượng độ bất định lan truyền](AIP-013-uncertainty-propagation.md) | Được dùng bởi | Độ bất định của kết quả đối chiếu |
| `AIP-020` | [Quyết định ba lớp, abstention và ngưỡng theo chi phí lỗi](AIP-020-three-way-decision-abstention.md) | Được dùng bởi | Mâu thuẫn thật ảnh hưởng tới quyết định |

## 7. Lịch sử thay đổi

| Ngày | Người sửa | Nội dung | Đã rà tham chiếu |
|---|---|---|---|
| 2026-09-28 | <Tên> | Tạo mới, định nghĩa ban đầu từ danh sách bài toán AI của luồng | Không cần |
| 2026-09-29 | binhnguyenSoftz | Tổ chức lại: đổi mã từ AIP-016 cũ; nhóm `AIG-05`, thêm `kind`; viết lại phát biểu bài toán | Có |
