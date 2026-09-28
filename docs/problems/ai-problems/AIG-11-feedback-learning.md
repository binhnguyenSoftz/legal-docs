---
id: AIG-11
title: Học từ phản hồi và cải tiến liên tục
type: Xuyên suốt              # Luồng | Xuyên suốt
status: Draft            # Draft | Review | Approved | Deprecated
owner: <Tên người phụ trách>
updated: 2026-09-29
---

# AIG-11 - Học từ phản hồi và cải tiến liên tục

Nhóm bài toán AI (capability) trong luồng xử lý hồ sơ. Danh sách mọi nhóm và sơ đồ luồng xem [README](README.md).

## 1. Bài toán nghiệp vụ

Biến chỉnh sửa của cán bộ duyệt thành dữ liệu cải tiến, chọn đúng hồ sơ cần người xem, và quyết định cải tiến bằng prompt/retrieval hay fine-tune.

## 2. Vị trí trong luồng

**Bước:** Xuyên suốt: học từ phản hồi.

| | Nội dung |
|---|---|
| Đầu vào | Chỉnh sửa và quyết định của cán bộ duyệt |
| Đầu ra | Dữ liệu huấn luyện/đánh giá mới, danh sách hồ sơ cần duyệt, đề xuất cải tiến |
| Nhận từ | [AIG-08](AIG-08-legal-generation.md), cán bộ duyệt |
| Chuyển cho | [AIG-09](AIG-09-evaluation-qa.md), các nhóm luồng |

## 3. Đánh giá cấp nhóm

Chỉ số cho biết cả nhóm có đạt không, đo trên golden set [AIP-026](AIP-026-layered-golden-set.md). Chỉ số chi tiết nằm trong từng bài toán con.

| Chỉ số | Ngưỡng chấp nhận |
|---|---|
| Mức cải thiện metric sau mỗi vòng | `[CẦN XÁC NHẬN]` |
| Tỉ lệ lỗi bị bỏ sót khi không chọn duyệt | `[CẦN XÁC NHẬN]` |

## 4. Bài toán con

Mỗi bài toán con là một file `AIP` riêng, có mức ưu tiên, giai đoạn và nhật ký thử nghiệm riêng. Ý nghĩa cột "Loại" xem [README](README.md) mục 3.

| Mã | Bài toán | Loại | Ưu tiên | Thử nghiệm sớm |
|---|---|---|---|---|
| [AIP-032](AIP-032-reviewer-feedback-learning.md) | Học từ chỉnh sửa của cán bộ duyệt | Hỗ trợ | Should |  |
| [AIP-033](AIP-033-review-sample-selection.md) | Chọn hồ sơ cần người duyệt | Bài toán | Could |  |

## 5. Lịch sử thay đổi

| Ngày | Người sửa | Nội dung | Đã rà tham chiếu |
|---|---|---|---|
| 2026-09-29 | binhnguyenSoftz | Tạo mới khi tổ chức lại bài toán AI thành 13 nhóm | Không cần |
