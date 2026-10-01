---
id: AIG-01
title: Đọc ảnh và OCR
type: Luồng              # Luồng | Xuyên suốt
status: Draft            # Draft | Review | Approved | Deprecated
owner: <Tên người phụ trách>
updated: 2026-09-29
---

# AIG-01 - Đọc ảnh và OCR

Nhóm bài toán AI (capability) trong luồng xử lý hồ sơ. Danh sách mọi nhóm và sơ đồ luồng xem [README](README.md).

## 1. Bài toán nghiệp vụ

Biến ảnh chụp, file scan giấy tờ thành văn bản có vị trí trên ảnh và điểm tin cậy đúng cho từng trường, đủ để bước sau quyết định trường nào tin được, trường nào phải chuyển người.

## 2. Vị trí trong luồng

**Bước:** Đọc ảnh.

| | Nội dung |
|---|---|
| Đầu vào | Ảnh chụp, file scan (PDF, JPG) người dân nộp |
| Đầu ra | Text theo vùng, tọa độ, điểm tin cậy đã hiệu chỉnh; cờ ảnh kém chất lượng |
| Nhận từ | - |
| Chuyển cho | [AIG-02](AIG-02-classification-splitting.md), [AIG-03](AIG-03-information-extraction.md) |

## 3. Đánh giá cấp nhóm

Chỉ số cho biết cả nhóm có đạt không, đo trên golden set [AIP-026](AIP-026-layered-golden-set.md). Chỉ số chi tiết nằm trong từng bài toán con.

| Chỉ số | Ngưỡng chấp nhận |
|---|---|
| CER/WER theo loại chữ (in, viết tay) | `[CẦN XÁC NHẬN]` |
| ECE của điểm tin cậy theo trường | `[CẦN XÁC NHẬN]` |

## 4. Bài toán con

Mỗi bài toán con là một file `AIP` riêng, có mức ưu tiên, giai đoạn và nhật ký thử nghiệm riêng. Ý nghĩa cột "Loại" xem [README](README.md) mục 3.

| Mã | Bài toán | Loại | Ưu tiên | Thử nghiệm sớm |
|---|---|---|---|---|
| [AIP-001](AIP-001-document-ocr.md) | Đọc bố cục và chữ tiếng Việt trên giấy tờ | Bài toán | Must | Có |
| [AIP-002](AIP-002-ocr-confidence-calibration.md) | Hiệu chỉnh độ tin cậy theo từng trường | Bài toán | Must | Có |
| [AIP-003](AIP-003-image-quality-check.md) | Đánh giá chất lượng ảnh | Bài toán | Should |  |

## 5. Lịch sử thay đổi

| Ngày | Người sửa | Nội dung | Đã rà tham chiếu |
|---|---|---|---|
| 2026-09-29 | binhnguyenSoftz | Tạo mới khi tổ chức lại bài toán AI thành 13 nhóm | Không cần |
| 2026-09-30 | binhnguyenSoftz | Bỏ bài toán phát hiện giả mạo (AIP-037, AIG-13): xóa lưu ý trỏ tới AIP-037 | Có |
