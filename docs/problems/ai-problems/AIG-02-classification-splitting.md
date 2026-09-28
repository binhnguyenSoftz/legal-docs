---
id: AIG-02
title: Phân loại và tách giấy tờ
type: Luồng              # Luồng | Xuyên suốt
status: Draft            # Draft | Review | Approved | Deprecated
owner: <Tên người phụ trách>
updated: 2026-09-29
---

# AIG-02 - Phân loại và tách giấy tờ

Nhóm bài toán AI (capability) trong luồng xử lý hồ sơ. Danh sách mọi nhóm và sơ đồ luồng xem [README](README.md).

## 1. Bài toán nghiệp vụ

Xác định trong file nộp lên có những giấy tờ nào, mỗi giấy tờ gồm các trang nào và thuộc loại gì, để chọn đúng schema trích xuất và đếm đúng giấy tờ còn thiếu.

## 2. Vị trí trong luồng

**Bước:** Phân loại, tách giấy tờ.

| | Nội dung |
|---|---|
| Đầu vào | Ảnh các trang, text OCR (AIG-01) |
| Đầu ra | Danh sách giấy tờ: trang, loại, điểm tin cậy |
| Nhận từ | [AIG-01](AIG-01-document-vision-ocr.md) |
| Chuyển cho | [AIG-03](AIG-03-information-extraction.md), [AIG-05](AIG-05-cross-document-validation.md) |

## 3. Đánh giá cấp nhóm

Chỉ số cho biết cả nhóm có đạt không, đo trên golden set [AIP-026](AIP-026-layered-golden-set.md). Chỉ số chi tiết nằm trong từng bài toán con.

| Chỉ số | Ngưỡng chấp nhận |
|---|---|
| Accuracy, F1 theo loại giấy | `[CẦN XÁC NHẬN]` |
| Độ chính xác ranh giới | `[CẦN XÁC NHẬN]` |

## 4. Bài toán con

Mỗi bài toán con là một file `AIP` riêng, có mức ưu tiên, giai đoạn và nhật ký thử nghiệm riêng. Ý nghĩa cột "Loại" xem [README](README.md) mục 3.

| Mã | Bài toán | Loại | Ưu tiên | Thử nghiệm sớm |
|---|---|---|---|---|
| [AIP-004](AIP-004-document-classification-splitting.md) | Phân loại và tách giấy tờ | Bài toán | Must |  |

## 5. Lịch sử thay đổi

| Ngày | Người sửa | Nội dung | Đã rà tham chiếu |
|---|---|---|---|
| 2026-09-29 | binhnguyenSoftz | Tạo mới khi tổ chức lại bài toán AI thành 13 nhóm | Không cần |
