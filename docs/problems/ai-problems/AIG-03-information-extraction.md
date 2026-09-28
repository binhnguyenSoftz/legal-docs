---
id: AIG-03
title: Trích xuất thông tin có nguồn
type: Luồng              # Luồng | Xuyên suốt
status: Draft            # Draft | Review | Approved | Deprecated
owner: <Tên người phụ trách>
updated: 2026-09-29
---

# AIG-03 - Trích xuất thông tin có nguồn

Nhóm bài toán AI (capability) trong luồng xử lý hồ sơ. Danh sách mọi nhóm và sơ đồ luồng xem [README](README.md).

## 1. Bài toán nghiệp vụ

Lấy các trường cần cho thủ tục ra dữ liệu có cấu trúc theo schema. Mỗi giá trị phải chỉ được vị trí nguồn trên ảnh, không bịa.

## 2. Vị trí trong luồng

**Bước:** Trích xuất.

| | Nội dung |
|---|---|
| Đầu vào | Giấy tờ đã phân loại (AIG-02), text và vị trí OCR (AIG-01) |
| Đầu ra | Bản ghi theo schema, mỗi trường có giá trị, nguồn, điểm tin cậy |
| Nhận từ | [AIG-01](AIG-01-document-vision-ocr.md), [AIG-02](AIG-02-classification-splitting.md) |
| Chuyển cho | [AIG-04](AIG-04-entity-resolution.md), [AIG-05](AIG-05-cross-document-validation.md) |

## 3. Đánh giá cấp nhóm

Chỉ số cho biết cả nhóm có đạt không, đo trên golden set [AIP-026](AIP-026-layered-golden-set.md). Chỉ số chi tiết nằm trong từng bài toán con.

| Chỉ số | Ngưỡng chấp nhận |
|---|---|
| Precision/recall theo trường | `[CẦN XÁC NHẬN]` |
| Tỉ lệ giá trị không có nguồn | `[CẦN XÁC NHẬN]` |

## 4. Bài toán con

Mỗi bài toán con là một file `AIP` riêng, có mức ưu tiên, giai đoạn và nhật ký thử nghiệm riêng. Ý nghĩa cột "Loại" xem [README](README.md) mục 3.

| Mã | Bài toán | Loại | Ưu tiên | Thử nghiệm sớm |
|---|---|---|---|---|
| [AIP-005](AIP-005-schema-extraction.md) | Trích xuất theo schema và sửa lỗi OCR | Bài toán | Must |  |
| [AIP-006](AIP-006-extraction-grounding.md) | Grounding và chống bịa khi trích xuất | Bài toán | Must |  |

> Lưu ý: Chống prompt injection ([AIP-029](AIP-029-document-prompt-injection.md), nhóm [AIG-10](AIG-10-safety-security.md)) và phân tầng model ([AIP-035](AIP-035-model-serving-cost-latency.md), nhóm [AIG-12](AIG-12-model-operations.md)) vẫn phải áp dụng cho bước trích xuất.

## 5. Lịch sử thay đổi

| Ngày | Người sửa | Nội dung | Đã rà tham chiếu |
|---|---|---|---|
| 2026-09-29 | binhnguyenSoftz | Tạo mới khi tổ chức lại bài toán AI thành 13 nhóm | Không cần |
