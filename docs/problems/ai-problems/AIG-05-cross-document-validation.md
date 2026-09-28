---
id: AIG-05
title: Đối chiếu và kiểm tra chéo giấy tờ
type: Luồng              # Luồng | Xuyên suốt
status: Draft            # Draft | Review | Approved | Deprecated
owner: <Tên người phụ trách>
updated: 2026-09-29
---

# AIG-05 - Đối chiếu và kiểm tra chéo giấy tờ

Nhóm bài toán AI (capability) trong luồng xử lý hồ sơ. Danh sách mọi nhóm và sơ đồ luồng xem [README](README.md).

## 1. Bài toán nghiệp vụ

Kiểm tra dữ liệu giữa các giấy tờ có nhất quán không, phân biệt mâu thuẫn thật với lỗi đọc, và phát hiện giấy tờ còn thiếu so với yêu cầu thủ tục.

## 2. Vị trí trong luồng

**Bước:** Đối chiếu chéo.

| | Nội dung |
|---|---|
| Đầu vào | Thực thể đã khớp (AIG-04), yêu cầu thủ tục có hiệu lực (AIG-06) |
| Đầu ra | Danh sách mâu thuẫn, giấy tờ thiếu, kết quả kiểm tra thời gian/số học, độ bất định |
| Nhận từ | [AIG-04](AIG-04-entity-resolution.md), [AIG-06](AIG-06-legal-retrieval.md) |
| Chuyển cho | [AIG-07](AIG-07-legal-decision.md) |

## 3. Đánh giá cấp nhóm

Chỉ số cho biết cả nhóm có đạt không, đo trên golden set [AIP-026](AIP-026-layered-golden-set.md). Chỉ số chi tiết nằm trong từng bài toán con.

| Chỉ số | Ngưỡng chấp nhận |
|---|---|
| Precision/recall phát hiện mâu thuẫn thật | `[CẦN XÁC NHẬN]` |
| Tỉ lệ báo nhầm do lỗi OCR | `[CẦN XÁC NHẬN]` |

## 4. Bài toán con

Mỗi bài toán con là một file `AIP` riêng, có mức ưu tiên, giai đoạn và nhật ký thử nghiệm riêng. Ý nghĩa cột "Loại" xem [README](README.md) mục 3.

| Mã | Bài toán | Loại | Ưu tiên | Thử nghiệm sớm |
|---|---|---|---|---|
| [AIP-010](AIP-010-conflict-vs-error.md) | Phân biệt mâu thuẫn thật với lỗi OCR/trích xuất | Bài toán | Must | Có |
| [AIP-011](AIP-011-temporal-numeric-reasoning.md) | Suy luận thời gian và số học trên dữ liệu trích xuất | Phương pháp | Must |  |
| [AIP-012](AIP-012-missing-document-detection.md) | Phát hiện thiếu giấy tờ | Bài toán | Must |  |
| [AIP-013](AIP-013-uncertainty-propagation.md) | Ước lượng độ bất định lan truyền | Phương pháp | Should |  |

> Lưu ý: Phần tính ngày tháng, số học ([AIP-011](AIP-011-temporal-numeric-reasoning.md)) chạy bằng code/rule engine, không giao LLM.

## 5. Lịch sử thay đổi

| Ngày | Người sửa | Nội dung | Đã rà tham chiếu |
|---|---|---|---|
| 2026-09-29 | binhnguyenSoftz | Tạo mới khi tổ chức lại bài toán AI thành 13 nhóm | Không cần |
