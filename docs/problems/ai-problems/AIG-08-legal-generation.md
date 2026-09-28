---
id: AIG-08
title: Sinh và kiểm chứng văn bản kết quả
type: Luồng              # Luồng | Xuyên suốt
status: Draft            # Draft | Review | Approved | Deprecated
owner: <Tên người phụ trách>
updated: 2026-09-29
---

# AIG-08 - Sinh và kiểm chứng văn bản kết quả

Nhóm bài toán AI (capability) trong luồng xử lý hồ sơ. Danh sách mọi nhóm và sơ đồ luồng xem [README](README.md).

## 1. Bài toán nghiệp vụ

Sinh văn bản kết quả gửi người dân đúng mẫu, đúng văn phong hành chính, mọi dữ kiện và trích dẫn đều kiểm chứng được trước khi chuyển cán bộ duyệt.

## 2. Vị trí trong luồng

**Bước:** Sinh văn bản.

| | Nội dung |
|---|---|
| Đầu vào | Quyết định và căn cứ (AIG-07), dữ kiện hồ sơ |
| Đầu ra | Văn bản kết quả đã kiểm chứng |
| Nhận từ | [AIG-07](AIG-07-legal-decision.md) |
| Chuyển cho | Cán bộ duyệt |

## 3. Đánh giá cấp nhóm

Chỉ số cho biết cả nhóm có đạt không, đo trên golden set [AIP-026](AIP-026-layered-golden-set.md). Chỉ số chi tiết nằm trong từng bài toán con.

| Chỉ số | Ngưỡng chấp nhận |
|---|---|
| Tỉ lệ văn bản có dữ kiện hoặc trích dẫn sai | `[CẦN XÁC NHẬN]` |
| Tỉ lệ cán bộ phải sửa | `[CẦN XÁC NHẬN]` |

## 4. Bài toán con

Mỗi bài toán con là một file `AIP` riêng, có mức ưu tiên, giai đoạn và nhật ký thử nghiệm riêng. Ý nghĩa cột "Loại" xem [README](README.md) mục 3.

| Mã | Bài toán | Loại | Ưu tiên | Thử nghiệm sớm |
|---|---|---|---|---|
| [AIP-023](AIP-023-controlled-generation.md) | Sinh văn bản kết quả có kiểm soát | Bài toán | Must |  |
| [AIP-024](AIP-024-citation-grounding.md) | Grounding trích dẫn pháp lý | Bài toán | Must |  |
| [AIP-025](AIP-025-post-generation-verification.md) | Kiểm chứng sau sinh | Bài toán | Must |  |

## 5. Lịch sử thay đổi

| Ngày | Người sửa | Nội dung | Đã rà tham chiếu |
|---|---|---|---|
| 2026-09-29 | binhnguyenSoftz | Tạo mới khi tổ chức lại bài toán AI thành 13 nhóm | Không cần |
