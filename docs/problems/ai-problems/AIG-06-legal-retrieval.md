---
id: AIG-06
title: Truy xuất pháp luật theo hiệu lực
type: Luồng              # Luồng | Xuyên suốt
status: Draft            # Draft | Review | Approved | Deprecated
owner: <Tên người phụ trách>
updated: 2026-09-29
---

# AIG-06 - Truy xuất pháp luật theo hiệu lực

Nhóm bài toán AI (capability) trong luồng xử lý hồ sơ. Danh sách mọi nhóm và sơ đồ luồng xem [README](README.md).

## 1. Bài toán nghiệp vụ

Tìm đúng điều, khoản, điểm áp dụng cho hồ sơ và có hiệu lực tại thời điểm phát sinh hồ sơ, kể cả khi văn bản đã bị sửa đổi, thay thế.

## 2. Vị trí trong luồng

**Bước:** Truy xuất pháp luật.

| | Nội dung |
|---|---|
| Đầu vào | Thủ tục, dữ kiện hồ sơ, thời điểm phát sinh; kho văn bản pháp luật |
| Đầu ra | Các điều khoản có hiệu lực, kèm phiên bản và quan hệ sửa đổi |
| Nhận từ | - |
| Chuyển cho | [AIG-05](AIG-05-cross-document-validation.md), [AIG-07](AIG-07-legal-decision.md), [AIG-08](AIG-08-legal-generation.md) |

## 3. Đánh giá cấp nhóm

Chỉ số cho biết cả nhóm có đạt không, đo trên golden set [AIP-026](AIP-026-layered-golden-set.md). Chỉ số chi tiết nằm trong từng bài toán con.

| Chỉ số | Ngưỡng chấp nhận |
|---|---|
| Recall@k, MRR trên bộ câu hỏi pháp lý | `[CẦN XÁC NHẬN]` |
| Tỉ lệ trả về văn bản hết hiệu lực | `[CẦN XÁC NHẬN]` |

## 4. Bài toán con

Mỗi bài toán con là một file `AIP` riêng, có mức ưu tiên, giai đoạn và nhật ký thử nghiệm riêng. Ý nghĩa cột "Loại" xem [README](README.md) mục 3.

| Mã | Bài toán | Loại | Ưu tiên | Thử nghiệm sớm |
|---|---|---|---|---|
| [AIP-014](AIP-014-legal-retrieval.md) | Truy xuất điều khoản pháp luật tiếng Việt | Bài toán | Must |  |
| [AIP-015](AIP-015-temporal-validity-retrieval.md) | Truy xuất theo hiệu lực thời gian | Bài toán | Must | Có |
| [AIP-016](AIP-016-legal-document-relations.md) | Quan hệ giữa văn bản pháp luật | Bài toán | Must |  |
| [AIP-017](AIP-017-legal-conflict-resolution.md) | Giải quyết xung đột giữa văn bản | Bài toán | Should |  |
| [AIP-018](AIP-018-retrieval-evaluation.md) | Đánh giá retrieval | Hỗ trợ | Must |  |

> Lưu ý: Chunking và embedding là cách làm, nằm trong [AIP-014](AIP-014-legal-retrieval.md). Bài toán nghiệp vụ chính là "tìm đúng điều luật có hiệu lực" ([AIP-015](AIP-015-temporal-validity-retrieval.md)).

## 5. Lịch sử thay đổi

| Ngày | Người sửa | Nội dung | Đã rà tham chiếu |
|---|---|---|---|
| 2026-09-29 | binhnguyenSoftz | Tạo mới khi tổ chức lại bài toán AI thành 13 nhóm | Không cần |
