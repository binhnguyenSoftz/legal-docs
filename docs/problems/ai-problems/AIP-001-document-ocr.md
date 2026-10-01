---
id: AIP-001
title: Đọc bố cục và chữ tiếng Việt trên giấy tờ
group: AIG-01
kind: problem            # problem | method | concern | enabler
status: Draft            # Draft | Review | Approved | Deprecated
stage: Defined           # Defined | Exploring | Decided | In production
priority: Must           # Must | Should | Could
early_test: true         # true: nằm trong nhóm khó nhất, thử nghiệm sớm
owner: <Tên người phụ trách>
updated: 2026-09-29
---

# AIP-001 - Đọc bố cục và chữ tiếng Việt trên giấy tờ

## 1. Định nghĩa

### 1.1. Phát biểu bài toán

Từ ảnh một trang giấy tờ, tách trang thành các vùng (nội dung chính, bảng, ô tick, dấu mộc, chữ ký, ghi chú lề), rồi đọc chữ trong từng vùng thành văn bản tiếng Việt có dấu. Chữ có thể là chữ in, đánh máy hoặc viết tay. Kết quả phải đủ chính xác để bước trích xuất (AIP-005) dùng được, và mỗi đoạn chữ phải giữ tọa độ trên ảnh để truy nguồn (AIP-006).

**Ví dụ:** trang 1 của tờ đăng ký nhà - đất đánh máy, có ô "Họ và tên chủ hộ" điền tay, dấu mộc đỏ đè lên chữ ký. Đầu ra: vùng `stamp`, vùng `signature`, vùng `handwriting` chứa `"Nguyễn Thị Hương"` với điểm thô 0,82 và bounding box của vùng đó.

**Phạm vi:**

- Gồm: phân tích bố cục; OCR chữ in, chữ đánh máy, chữ viết tay; điểm tin cậy thô cho từng từ.
- Không gồm: hiệu chỉnh điểm tin cậy (AIP-002), kiểm tra chất lượng ảnh (AIP-003), sửa lỗi OCR bằng ngữ cảnh (AIP-005).

### 1.2. Vị trí trong luồng

**Bước:** Đọc ảnh (nhóm [AIG-01](AIG-01-document-vision-ocr.md) - Đọc ảnh và OCR). Sơ đồ luồng xem [README](README.md).

- Dựa vào: [AIP-003](AIP-003-image-quality-check.md) - Đánh giá chất lượng ảnh
- Được dùng bởi: [AIP-002](AIP-002-ocr-confidence-calibration.md) - Hiệu chỉnh độ tin cậy theo từng trường; [AIP-004](AIP-004-document-classification-splitting.md) - Phân loại và tách giấy tờ; [AIP-005](AIP-005-schema-extraction.md) - Trích xuất theo schema và sửa lỗi OCR; [AIP-006](AIP-006-extraction-grounding.md) - Grounding và chống bịa khi trích xuất; [AIP-030](AIP-030-bias-fairness.md) - Bias và fairness

### 1.3. Đầu vào và đầu ra

| | Nội dung | Ví dụ |
|---|---|---|
| Đầu vào | Ảnh một trang đã đạt ngưỡng chất lượng (AIP-003) | Trang 1 của đơn đăng ký |
| Đầu ra | Danh sách vùng: loại, bounding box, văn bản đọc được, điểm tin cậy thô cho từng từ | `{type: "handwriting", page: 1, bbox: [...], text: "Nguyễn Thị Hương", score: 0,82}` |

### 1.4. Ràng buộc bắt buộc

Chưa có. Bổ sung khi đi sâu vào bài toán, đánh mã `AIP-001-R01`, `R02`...

### 1.5. Bài toán con

| Bài toán con | Mã cũ | Ưu tiên | Nội dung |
|---|---|---|---|
| OCR chữ in, đánh máy, viết tay tiếng Việt | AIP-001 cũ | Must | Đọc chữ trong từng vùng, giữ đúng dấu thanh |
| Phân tích bố cục | AIP-002 cũ | Should | Tách vùng nội dung, bảng, ô tick, dấu mộc, chữ ký, ghi chú lề |

Phân tích bố cục để `Should` vì VLM hoặc OCR thương mại thường tự xử lý được bố cục đơn giản. `[CẦN XÁC NHẬN]` Nếu thử nghiệm cho thấy OCR đọc lẫn vùng (dấu đè chữ, ghi chú lề) thì nâng lên `Must`.

## 2. Vì sao khó

### 2.1. Thách thức

- Dấu thanh tiếng Việt dễ đọc sai hoặc mất (`Hương` thành `Huong`, `Hưởng`).
- Người viết dùng viết tắt không thống nhất. Nét chữ đa dạng theo người viết.
- Chữ viết đè lên dòng kẻ của mẫu in sẵn. Dấu mộc và chữ ký đè lên chữ.
- Nhiều loại vùng trên cùng trang. Ghi chú lề dễ bị lẫn vào nội dung chính.
- Trang có nhiều cột hoặc nhiều khung: OCR đọc cả trang thường sắp dòng theo tọa độ, nên hai dòng khác cột nằm cùng chiều cao dễ bị gộp thành một dòng. Chữ vẫn đọc đúng nhưng giá trị bị lẫn giữa các trường.
- Giấy tờ cũ: giấy ố, mực phai, chữ đánh máy mờ.
- Có thể phải fine-tune trên dữ liệu viết tay của chính dự án, nên cần dữ liệu có gán nhãn.

### 2.2. Chi phí khi sai

- OCR sai họ tên, số giấy tờ hoặc ngày tháng làm sai mọi bước sau. Hậu quả nặng nhất là hồ sơ hợp lệ bị báo mâu thuẫn rồi bị từ chối oan.
- Tách sai vùng thì OCR đọc lẫn nội dung, ô tick bị bỏ qua, hoặc ghi chú lề bị hiểu là nội dung chính.

## 3. Đánh giá

| Chỉ số | Cách đo | Ngưỡng chấp nhận |
|---|---|---|
| CER (Character Error Rate) | Trên ảnh có nhãn trong golden set AIP-026, tính riêng chữ in và chữ viết tay | `[CẦN XÁC NHẬN]` |
| WER (Word Error Rate) | Như trên, tính riêng lỗi dấu thanh | `[CẦN XÁC NHẬN]` |
| Độ chính xác theo trường | Tỉ lệ trường đọc đúng hoàn toàn | `[CẦN XÁC NHẬN]` |
| Độ chính xác phân tích bố cục (tách vùng theo loại) | Vùng bố cục (nội dung, bảng, ô tick, dấu mộc, chữ ký, ghi chú lề), không phải dòng, từ chữ của OCR. `[CẦN XÁC NHẬN]` cách khớp vùng dự đoán với vùng nhãn | `[CẦN XÁC NHẬN]` |
| Tỉ lệ trường bị lẫn giữa các cột, khung | Trên trang có nhiều cột hoặc khung: tỉ lệ trường chứa chữ của cột, khung bên cạnh. CER không bắt được lỗi này | `[CẦN XÁC NHẬN]` |

## 4. Hướng tiếp cận và thử nghiệm

### 4.1. Hướng tiếp cận ứng viên

| Hướng | Ưu điểm | Nhược điểm |
|---|---|---|
| OCR chuyên dụng kèm mô hình bố cục riêng | `[CẦN XÁC NHẬN]` | `[CẦN XÁC NHẬN]` |
| VLM (Vision Language Model) đọc cả trang | Tự xử lý bố cục | `[CẦN XÁC NHẬN]` |
| Kết hợp OCR chuyên dụng và VLM | `[CẦN XÁC NHẬN]` | `[CẦN XÁC NHẬN]` |
| Fine-tune trên dữ liệu viết tay của dự án | Sát với dữ liệu thật | Cần dữ liệu gán nhãn |
| `[CẦN XÁC NHẬN]` Chưa khảo sát thêm | | |

**Thử nghiệm cần chạy đầu tiên:** trên 20-30 trang có nhiều cột hoặc khung, so sánh (1) OCR cả trang với (2) tách vùng rồi OCR từng vùng. So CER và tỉ lệ trường bị lẫn giữa các cột, khung. Nếu (2) tốt hơn rõ thì nâng phân tích bố cục (mục 1.5) lên `Must`; nếu không khác nhiều thì giữ `Should` để đỡ công bảo trì bước tách vùng.

### 4.2. Dữ liệu cần chuẩn bị

- Tập ảnh thật của các loại giấy tờ trong luồng (danh sách ở AIP-027 mục 4.2), đã che thông tin cá nhân nếu cần.
- Nhãn văn bản đúng cho từng vùng.
- Nhãn vùng theo từng loại (nội dung, bảng, ô tick, dấu mộc, chữ ký, ghi chú lề).

### 4.3. Nhật ký thử nghiệm

| Ngày | Thử nghiệm | Kết quả | Kết luận |
|---|---|---|---|
| | | | |

## 5. Câu hỏi còn mở

- [ ] Có được dùng ảnh hồ sơ thật để gán nhãn và fine-tune không?
- [ ] Cần bao nhiêu mẫu để đánh giá có ý nghĩa?
- [ ] Danh sách loại vùng cần tách đã đủ chưa?
- [ ] Những loại giấy tờ nào trong luồng có nhiều cột hoặc khung (biểu mẫu kẻ ô), loại nào viết tự do?

## 6. Tài liệu tham chiếu

Quy tắc ghi: `standards/07-references.md`.

| Mã | Tài liệu | Chiều | Nội dung liên quan |
|---|---|---|---|
| `AIP-003` | [Đánh giá chất lượng ảnh](AIP-003-image-quality-check.md) | Dựa vào | Chỉ đọc ảnh đạt ngưỡng chất lượng |
| `AIP-002` | [Hiệu chỉnh độ tin cậy theo từng trường](AIP-002-ocr-confidence-calibration.md) | Được dùng bởi | Hiệu chỉnh điểm tin cậy thô của OCR |
| `AIP-004` | [Phân loại và tách giấy tờ](AIP-004-document-classification-splitting.md) | Được dùng bởi | Dùng text OCR làm đặc trưng phân loại |
| `AIP-005` | [Trích xuất theo schema và sửa lỗi OCR](AIP-005-schema-extraction.md) | Được dùng bởi | Trích xuất trên text OCR |
| `AIP-006` | [Grounding và chống bịa khi trích xuất](AIP-006-extraction-grounding.md) | Được dùng bởi | Dùng bounding box của vùng làm vị trí nguồn |
| `AIP-030` | [Bias và fairness](AIP-030-bias-fairness.md) | Được dùng bởi | Đo chênh lệch chất lượng OCR theo nhóm người |

## 7. Lịch sử thay đổi

| Ngày | Người sửa | Nội dung | Đã rà tham chiếu |
|---|---|---|---|
| 2026-09-28 | <Tên> | Tạo mới, định nghĩa ban đầu từ danh sách bài toán AI của luồng | Không cần |
| 2026-09-29 | binhnguyenSoftz | Tổ chức lại: gộp AIP-001 cũ (OCR viết tay) và AIP-002 cũ (phân tích bố cục); nhóm `AIG-01`; viết lại phát biểu bài toán | Có |
| 2026-09-29 | binhnguyenSoftz | Thêm thách thức trang nhiều cột, khung; chỉ số tỉ lệ trường bị lẫn giữa các cột, khung; thử nghiệm so sánh OCR cả trang với tách vùng | Không cần |
| 2026-09-29 | binhnguyenSoftz | Đổi tên chỉ số "phát hiện vùng theo loại" thành "phân tích bố cục (tách vùng theo loại)" | Không cần |
| 2026-09-30 | binhnguyenSoftz | Bỏ bài toán phát hiện giả mạo (AIP-037, AIG-13): xóa tham chiếu tới AIP-037 ở mục 1.1, 1.2, 6 | Có |
