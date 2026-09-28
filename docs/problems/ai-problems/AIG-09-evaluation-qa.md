---
id: AIG-09
title: Đánh giá và bảo đảm chất lượng AI
type: Xuyên suốt              # Luồng | Xuyên suốt
status: Draft            # Draft | Review | Approved | Deprecated
owner: <Tên người phụ trách>
updated: 2026-09-29
---

# AIG-09 - Đánh giá và bảo đảm chất lượng AI

Nhóm bài toán AI (capability) trong luồng xử lý hồ sơ. Danh sách mọi nhóm và sơ đồ luồng xem [README](README.md).

## 1. Bài toán nghiệp vụ

Đo được chất lượng từng tầng và toàn luồng, và phát hiện suy giảm khi đổi model, prompt hoặc luật. Không có nhóm này thì không nghiệm thu được nhóm nào khác.

## 2. Vị trí trong luồng

**Bước:** Xuyên suốt: đánh giá.

| | Nội dung |
|---|---|
| Đầu vào | Golden set, đầu ra của các nhóm AIG-01 đến AIG-08 |
| Đầu ra | Số liệu theo tầng, số liệu end-to-end, báo cáo regression |
| Nhận từ | Mọi nhóm |
| Chuyển cho | Mọi nhóm |

## 3. Đánh giá cấp nhóm

Chỉ số cho biết cả nhóm có đạt không, đo trên golden set [AIP-026](AIP-026-layered-golden-set.md). Chỉ số chi tiết nằm trong từng bài toán con.

| Chỉ số | Ngưỡng chấp nhận |
|---|---|
| Độ phủ golden set theo loại giấy tờ, thủ tục | `[CẦN XÁC NHẬN]` |
| Thời gian chạy một vòng đánh giá | `[CẦN XÁC NHẬN]` |

## 4. Bài toán con

Mỗi bài toán con là một file `AIP` riêng, có mức ưu tiên, giai đoạn và nhật ký thử nghiệm riêng. Ý nghĩa cột "Loại" xem [README](README.md) mục 3.

| Mã | Bài toán | Loại | Ưu tiên | Thử nghiệm sớm |
|---|---|---|---|---|
| [AIP-026](AIP-026-layered-golden-set.md) | Golden set và metric theo từng tầng | Hỗ trợ | Must |  |
| [AIP-027](AIP-027-end-to-end-evaluation.md) | Đánh giá end-to-end và chấm văn bản sinh ra | Hỗ trợ | Must |  |
| [AIP-028](AIP-028-regression-testing.md) | Regression test khi đổi model, prompt hoặc luật | Hỗ trợ | Should |  |

> Lưu ý: Phần an toàn nằm ở [AIG-10](AIG-10-safety-security.md), phát hiện drift nằm ở [AIG-12](AIG-12-model-operations.md).

## 5. Lịch sử thay đổi

| Ngày | Người sửa | Nội dung | Đã rà tham chiếu |
|---|---|---|---|
| 2026-09-29 | binhnguyenSoftz | Tạo mới khi tổ chức lại bài toán AI thành 13 nhóm | Không cần |
