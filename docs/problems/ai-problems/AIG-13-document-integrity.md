---
id: AIG-13
title: Toàn vẹn giấy tờ
type: Xuyên suốt              # Luồng | Xuyên suốt
status: Draft            # Draft | Review | Approved | Deprecated
owner: <Tên người phụ trách>
updated: 2026-09-29
---

# AIG-13 - Toàn vẹn giấy tờ

Nhóm bài toán AI (capability) trong luồng xử lý hồ sơ. Danh sách mọi nhóm và sơ đồ luồng xem [README](README.md).

## 1. Bài toán nghiệp vụ

Phát hiện giấy tờ bị giả mạo hoặc chỉnh sửa ảnh trước khi dữ liệu của nó được dùng để ra quyết định.

## 2. Vị trí trong luồng

**Bước:** Xuyên suốt: toàn vẹn giấy tờ.

| | Nội dung |
|---|---|
| Đầu vào | Ảnh giấy tờ gốc (AIG-01) |
| Đầu ra | Cờ nghi giả mạo, vùng nghi chỉnh sửa, điểm tin cậy |
| Nhận từ | [AIG-01](AIG-01-document-vision-ocr.md) |
| Chuyển cho | [AIG-07](AIG-07-legal-decision.md) |

## 3. Đánh giá cấp nhóm

Chỉ số cho biết cả nhóm có đạt không, đo trên golden set [AIP-026](AIP-026-layered-golden-set.md). Chỉ số chi tiết nằm trong từng bài toán con.

| Chỉ số | Ngưỡng chấp nhận |
|---|---|
| Precision/recall phát hiện giả mạo | `[CẦN XÁC NHẬN]` |
| Tỉ lệ báo nhầm trên giấy tờ thật | `[CẦN XÁC NHẬN]` |

## 4. Bài toán con

Mỗi bài toán con là một file `AIP` riêng, có mức ưu tiên, giai đoạn và nhật ký thử nghiệm riêng. Ý nghĩa cột "Loại" xem [README](README.md) mục 3.

| Mã | Bài toán | Loại | Ưu tiên | Thử nghiệm sớm |
|---|---|---|---|---|
| [AIP-037](AIP-037-tampering-detection.md) | Phát hiện giả mạo, chỉnh sửa ảnh | Rủi ro | Could |  |

## 5. Lịch sử thay đổi

| Ngày | Người sửa | Nội dung | Đã rà tham chiếu |
|---|---|---|---|
| 2026-09-29 | binhnguyenSoftz | Tạo mới khi tổ chức lại bài toán AI thành 13 nhóm | Không cần |
