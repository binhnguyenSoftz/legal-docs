---
id: AIG-04
title: Khớp thực thể và suy ra quan hệ
type: Luồng              # Luồng | Xuyên suốt
status: Draft            # Draft | Review | Approved | Deprecated
owner: <Tên người phụ trách>
updated: 2026-09-29
---

# AIG-04 - Khớp thực thể và suy ra quan hệ

Nhóm bài toán AI (capability) trong luồng xử lý hồ sơ. Danh sách mọi nhóm và sơ đồ luồng xem [README](README.md).

## 1. Bài toán nghiệp vụ

Biết các giấy tờ khác nhau đang nói về cùng một người, cùng một địa chỉ, cùng một hộ, để đối chiếu chéo được.

## 2. Vị trí trong luồng

**Bước:** Chuẩn hóa, khớp thực thể.

| | Nội dung |
|---|---|
| Đầu vào | Bản ghi trích xuất từ nhiều giấy tờ (AIG-03) |
| Đầu ra | Danh sách thực thể đã khớp (người, địa chỉ chuẩn hóa, hộ) và quan hệ giữa họ |
| Nhận từ | [AIG-03](AIG-03-information-extraction.md) |
| Chuyển cho | [AIG-05](AIG-05-cross-document-validation.md) |

## 3. Đánh giá cấp nhóm

Chỉ số cho biết cả nhóm có đạt không, đo trên golden set [AIP-026](AIP-026-layered-golden-set.md). Chỉ số chi tiết nằm trong từng bài toán con.

| Chỉ số | Ngưỡng chấp nhận |
|---|---|
| Precision/recall của cặp khớp | `[CẦN XÁC NHẬN]` |
| Tỉ lệ khớp nhầm hai người khác nhau | `[CẦN XÁC NHẬN]` |

## 4. Bài toán con

Mỗi bài toán con là một file `AIP` riêng, có mức ưu tiên, giai đoạn và nhật ký thử nghiệm riêng. Ý nghĩa cột "Loại" xem [README](README.md) mục 3.

| Mã | Bài toán | Loại | Ưu tiên | Thử nghiệm sớm |
|---|---|---|---|---|
| [AIP-007](AIP-007-person-matching.md) | Khớp cùng một người qua nhiều giấy tờ | Bài toán | Must |  |
| [AIP-008](AIP-008-address-normalization.md) | Chuẩn hóa địa chỉ hành chính Việt Nam | Bài toán | Should |  |
| [AIP-009](AIP-009-household-inference.md) | Suy ra quan hệ hộ | Bài toán | Should |  |

## 5. Lịch sử thay đổi

| Ngày | Người sửa | Nội dung | Đã rà tham chiếu |
|---|---|---|---|
| 2026-09-29 | binhnguyenSoftz | Tạo mới khi tổ chức lại bài toán AI thành 13 nhóm | Không cần |
