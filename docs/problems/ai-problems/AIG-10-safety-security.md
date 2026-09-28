---
id: AIG-10
title: An toàn và bảo mật AI
type: Xuyên suốt              # Luồng | Xuyên suốt
status: Draft            # Draft | Review | Approved | Deprecated
owner: <Tên người phụ trách>
updated: 2026-09-29
---

# AIG-10 - An toàn và bảo mật AI

Nhóm bài toán AI (capability) trong luồng xử lý hồ sơ. Danh sách mọi nhóm và sơ đồ luồng xem [README](README.md).

## 1. Bài toán nghiệp vụ

Bảo đảm hệ thống không bị nội dung giấy tờ điều khiển, không đối xử thiên lệch giữa các nhóm người dân, và được tấn công thử trước khi chạy thật.

## 2. Vị trí trong luồng

**Bước:** Xuyên suốt: an toàn, bảo mật.

| | Nội dung |
|---|---|
| Đầu vào | Prompt, đầu vào tài liệu, đầu ra quyết định của các nhóm luồng |
| Đầu ra | Biện pháp phòng vệ, báo cáo red-team, số liệu fairness |
| Nhận từ | Mọi nhóm |
| Chuyển cho | Mọi nhóm |

## 3. Đánh giá cấp nhóm

Chỉ số cho biết cả nhóm có đạt không, đo trên golden set [AIP-026](AIP-026-layered-golden-set.md). Chỉ số chi tiết nằm trong từng bài toán con.

| Chỉ số | Ngưỡng chấp nhận |
|---|---|
| Tỉ lệ tấn công thành công trong red-team | `[CẦN XÁC NHẬN]` |
| Chênh lệch kết quả giữa các nhóm người dân | `[CẦN XÁC NHẬN]` |

## 4. Bài toán con

Mỗi bài toán con là một file `AIP` riêng, có mức ưu tiên, giai đoạn và nhật ký thử nghiệm riêng. Ý nghĩa cột "Loại" xem [README](README.md) mục 3.

| Mã | Bài toán | Loại | Ưu tiên | Thử nghiệm sớm |
|---|---|---|---|---|
| [AIP-029](AIP-029-document-prompt-injection.md) | Chống prompt injection từ nội dung tài liệu | Rủi ro | Must |  |
| [AIP-030](AIP-030-bias-fairness.md) | Bias và fairness | Rủi ro | Should |  |
| [AIP-031](AIP-031-red-teaming.md) | Red-teaming | Hỗ trợ | Should |  |

## 5. Lịch sử thay đổi

| Ngày | Người sửa | Nội dung | Đã rà tham chiếu |
|---|---|---|---|
| 2026-09-29 | binhnguyenSoftz | Tạo mới khi tổ chức lại bài toán AI thành 13 nhóm | Không cần |
