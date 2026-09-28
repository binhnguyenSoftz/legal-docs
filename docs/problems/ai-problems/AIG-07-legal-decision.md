---
id: AIG-07
title: Suy luận pháp lý và hỗ trợ quyết định
type: Luồng              # Luồng | Xuyên suốt
status: Draft            # Draft | Review | Approved | Deprecated
owner: <Tên người phụ trách>
updated: 2026-09-29
---

# AIG-07 - Suy luận pháp lý và hỗ trợ quyết định

Nhóm bài toán AI (capability) trong luồng xử lý hồ sơ. Danh sách mọi nhóm và sơ đồ luồng xem [README](README.md).

## 1. Bài toán nghiệp vụ

Áp điều luật vào dữ kiện hồ sơ và đề xuất một trong các lớp: chấp thuận, từ chối, cần bổ sung, hoặc chuyển người khi không đủ tự tin. Mỗi đề xuất kèm căn cứ kiểm chứng được.

## 2. Vị trí trong luồng

**Bước:** Suy luận, ra quyết định.

| | Nội dung |
|---|---|
| Đầu vào | Dữ kiện đã đối chiếu (AIG-05), điều khoản có hiệu lực (AIG-06) |
| Đầu ra | Đề xuất quyết định, kết luận từng điều kiện, lời giải thích kèm căn cứ |
| Nhận từ | [AIG-05](AIG-05-cross-document-validation.md), [AIG-06](AIG-06-legal-retrieval.md) |
| Chuyển cho | [AIG-08](AIG-08-legal-generation.md) |

## 3. Đánh giá cấp nhóm

Chỉ số cho biết cả nhóm có đạt không, đo trên golden set [AIP-026](AIP-026-layered-golden-set.md). Chỉ số chi tiết nằm trong từng bài toán con.

| Chỉ số | Ngưỡng chấp nhận |
|---|---|
| Độ khớp với chuyên viên | `[CẦN XÁC NHẬN]` |
| Tỉ lệ quyết định sai khi đã tự quyết (không abstain) | `[CẦN XÁC NHẬN]` |
| Coverage | `[CẦN XÁC NHẬN]` |

## 4. Bài toán con

Mỗi bài toán con là một file `AIP` riêng, có mức ưu tiên, giai đoạn và nhật ký thử nghiệm riêng. Ý nghĩa cột "Loại" xem [README](README.md) mục 3.

| Mã | Bài toán | Loại | Ưu tiên | Thử nghiệm sớm |
|---|---|---|---|---|
| [AIP-019](AIP-019-legal-reasoning.md) | Suy luận pháp lý | Bài toán | Must |  |
| [AIP-020](AIP-020-three-way-decision-abstention.md) | Quyết định ba lớp, abstention và ngưỡng theo chi phí lỗi | Bài toán | Must | Có |
| [AIP-021](AIP-021-explainability-faithfulness.md) | Giải thích và faithfulness | Bài toán | Must |  |
| [AIP-022](AIP-022-decision-consistency.md) | Nhất quán kết quả | Rủi ro | Should |  |

> Lưu ý: Neuro-symbolic là phương pháp, nằm trong [AIP-019](AIP-019-legal-reasoning.md) mục 4.1.

## 5. Lịch sử thay đổi

| Ngày | Người sửa | Nội dung | Đã rà tham chiếu |
|---|---|---|---|
| 2026-09-29 | binhnguyenSoftz | Tạo mới khi tổ chức lại bài toán AI thành 13 nhóm | Không cần |
