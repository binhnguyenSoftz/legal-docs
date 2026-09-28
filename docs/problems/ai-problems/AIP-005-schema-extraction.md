---
id: AIP-005
title: Trích xuất theo schema và sửa lỗi OCR
group: AIG-03
kind: problem            # problem | method | concern | enabler
status: Draft            # Draft | Review | Approved | Deprecated
stage: Defined           # Defined | Exploring | Decided | In production
priority: Must           # Must | Should | Could
early_test: false        # true: nằm trong nhóm khó nhất, thử nghiệm sớm
owner: <Tên người phụ trách>
updated: 2026-09-29
---

# AIP-005 - Trích xuất theo schema và sửa lỗi OCR

## 1. Định nghĩa

### 1.1. Phát biểu bài toán

Với mỗi giấy tờ đã biết loại (AIP-004), lấy từ text OCR ra đúng các trường mà schema của loại giấy đó yêu cầu (họ tên, ngày sinh, số CCCD, địa chỉ thửa đất, diện tích...), trả về JSON đúng schema. Trường không có trong giấy tờ phải để `null`. Khi OCR đọc sai rõ ràng và ngữ cảnh đủ để sửa, được sửa nhưng phải giữ giá trị gốc.

**Ví dụ:** giấy chứng tử có dòng OCR `Ho ten nguoi chet: Nguyen Van An, chet ngay 12/O3/2019`. Đầu ra: `{"ho_ten": "Nguyễn Văn An", "ngay_mat": "2019-03-12", "noi_mat": null}`, trong đó `ngay_mat` ghi kèm giá trị gốc `12/O3/2019` và cờ "đã sửa" (chữ `O` thành số `0`).

**Phạm vi:**

- Gồm: chọn schema theo loại giấy; trích xuất trường; chuẩn hóa định dạng ngày, số; sửa lỗi OCR bằng ngữ cảnh.
- Không gồm: gắn vị trí nguồn cho từng trường (AIP-006), chuẩn hóa địa chỉ theo danh mục hành chính (AIP-008), khớp người giữa các giấy tờ (AIP-007).

### 1.2. Vị trí trong luồng

**Bước:** Trích xuất (nhóm [AIG-03](AIG-03-information-extraction.md) - Trích xuất thông tin có nguồn). Sơ đồ luồng xem [README](README.md).

- Dựa vào: [AIP-004](AIP-004-document-classification-splitting.md) - Phân loại và tách giấy tờ; [AIP-001](AIP-001-document-ocr.md) - Đọc bố cục và chữ tiếng Việt trên giấy tờ; [AIP-002](AIP-002-ocr-confidence-calibration.md) - Hiệu chỉnh độ tin cậy theo từng trường
- Được dùng bởi: [AIP-006](AIP-006-extraction-grounding.md) - Grounding và chống bịa khi trích xuất; [AIP-007](AIP-007-person-matching.md) - Khớp cùng một người qua nhiều giấy tờ; [AIP-008](AIP-008-address-normalization.md) - Chuẩn hóa địa chỉ hành chính Việt Nam; [AIP-011](AIP-011-temporal-numeric-reasoning.md) - Suy luận thời gian và số học trên dữ liệu trích xuất; [AIP-029](AIP-029-document-prompt-injection.md) - Chống prompt injection từ nội dung tài liệu; [AIP-035](AIP-035-model-serving-cost-latency.md) - Phân tầng model, tối ưu chi phí và độ trễ

### 1.3. Đầu vào và đầu ra

| | Nội dung | Ví dụ |
|---|---|---|
| Đầu vào | Text OCR (AIP-001), loại giấy tờ (AIP-004), schema tương ứng, độ tin cậy đã hiệu chỉnh (AIP-002) | Text OCR của đơn đăng ký |
| Đầu ra | JSON đúng schema. Trường đã sửa kèm giá trị gốc | `{"ho_ten": "Nguyễn Thị Hương", "ngay_sinh": null}` |

### 1.4. Ràng buộc bắt buộc

| Mã | Ràng buộc | Lý do |
|---|---|---|
| AIP-005-R01 | Đầu ra phải đúng JSON theo schema của loại giấy tờ. | Bước sau xử lý bằng code. |
| AIP-005-R02 | Trường không có trong tài liệu phải là `null`, không được suy đoán. | Giá trị bịa gây quyết định sai. |

### 1.5. Bài toán con

| Bài toán con | Mã cũ | Ưu tiên | Nội dung |
|---|---|---|---|
| Trích xuất có cấu trúc theo schema | AIP-008 cũ | Must | Trích trường, ép đúng JSON, để `null` khi không có |
| Sửa lỗi OCR bằng ngữ cảnh | AIP-010 cũ | Should | Sửa lỗi OCR rõ ràng, không sửa quá tay, giữ giá trị gốc |

## 2. Vì sao khó

### 2.1. Thách thức

- Ép model trả đúng JSON theo schema.
- Model có xu hướng điền giá trị cho trường không có trong tài liệu.
- Ranh giới giữa sửa lỗi OCR và "sửa quá tay" thành một giá trị khác nhưng hợp lý.
- Giấy tờ không có mẫu cố định (giấy sang đất viết tay) không dựa vào vị trí trường được.

### 2.2. Chi phí khi sai

- Giá trị bịa đi thẳng vào đối chiếu và quyết định. Sai kiểu này nguy hiểm hơn để trống.
- Sửa quá tay tạo ra dữ liệu sai trông rất đúng, khó phát hiện hơn lỗi OCR gốc.

## 3. Đánh giá

| Chỉ số | Cách đo | Ngưỡng chấp nhận |
|---|---|---|
| Field-level accuracy / F1 | Trên golden set AIP-026 | `[CẦN XÁC NHẬN]` |
| Tỉ lệ JSON sai schema | `[CẦN XÁC NHẬN]` | `[CẦN XÁC NHẬN]` |
| Tỉ lệ trường bị bịa | Trường có giá trị trong khi nhãn là `null` | `[CẦN XÁC NHẬN]` |
| Tỉ lệ sửa đúng | Trên cặp giá trị OCR sai và giá trị đúng | `[CẦN XÁC NHẬN]` |
| Tỉ lệ sửa sai | Giá trị đúng bị sửa thành sai | `[CẦN XÁC NHẬN]` |

## 4. Hướng tiếp cận và thử nghiệm

### 4.1. Hướng tiếp cận ứng viên

| Hướng | Ưu điểm | Nhược điểm |
|---|---|---|
| `[CẦN XÁC NHẬN]` Chưa khảo sát thêm | | |

### 4.2. Dữ liệu cần chuẩn bị

- Schema cho từng loại giấy tờ.
- Text OCR có nhãn giá trị từng trường.
- Cặp giá trị OCR sai và giá trị đúng.

### 4.3. Nhật ký thử nghiệm

| Ngày | Thử nghiệm | Kết quả | Kết luận |
|---|---|---|---|
| | | | |

## 5. Câu hỏi còn mở

- [ ] Ai định nghĩa và duyệt schema cho từng loại giấy tờ?
- [ ] Có giữ giá trị OCR gốc song song với giá trị đã sửa không?

## 6. Tài liệu tham chiếu

Quy tắc ghi: `standards/07-references.md`.

| Mã | Tài liệu | Chiều | Nội dung liên quan |
|---|---|---|---|
| `AIP-004` | [Phân loại và tách giấy tờ](AIP-004-document-classification-splitting.md) | Dựa vào | Chọn schema theo loại giấy tờ |
| `AIP-001` | [Đọc bố cục và chữ tiếng Việt trên giấy tờ](AIP-001-document-ocr.md) | Dựa vào | Trích xuất trên text OCR |
| `AIP-002` | [Hiệu chỉnh độ tin cậy theo từng trường](AIP-002-ocr-confidence-calibration.md) | Dựa vào | Chọn trường cần sửa lỗi theo độ tin cậy đã hiệu chỉnh |
| `AIP-006` | [Grounding và chống bịa khi trích xuất](AIP-006-extraction-grounding.md) | Được dùng bởi | Gắn vị trí nguồn cho từng trường, kể cả trường đã sửa |
| `AIP-007` | [Khớp cùng một người qua nhiều giấy tờ](AIP-007-person-matching.md) | Được dùng bởi | Dùng họ tên, ngày sinh, số giấy tờ đã trích xuất |
| `AIP-008` | [Chuẩn hóa địa chỉ hành chính Việt Nam](AIP-008-address-normalization.md) | Được dùng bởi | Dùng địa chỉ đã trích xuất |
| `AIP-011` | [Suy luận thời gian và số học trên dữ liệu trích xuất](AIP-011-temporal-numeric-reasoning.md) | Được dùng bởi | Tính trên dữ liệu đã trích xuất |
| `AIP-029` | [Chống prompt injection từ nội dung tài liệu](AIP-029-document-prompt-injection.md) | Được dùng bởi | Nội dung tài liệu đi vào prompt trích xuất |
| `AIP-035` | [Phân tầng model, tối ưu chi phí và độ trễ](AIP-035-model-serving-cost-latency.md) | Được dùng bởi | Chọn model cho bước trích xuất |

## 7. Lịch sử thay đổi

| Ngày | Người sửa | Nội dung | Đã rà tham chiếu |
|---|---|---|---|
| 2026-09-28 | <Tên> | Tạo mới, định nghĩa ban đầu từ danh sách bài toán AI của luồng | Không cần |
| 2026-09-29 | binhnguyenSoftz | Tổ chức lại: gộp AIP-008 cũ (trích xuất theo schema) và AIP-010 cũ (sửa lỗi OCR); nhóm `AIG-03`; viết lại phát biểu bài toán | Có |
