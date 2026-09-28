---
id: AIG-12
title: Triển khai và vận hành model
type: Xuyên suốt              # Luồng | Xuyên suốt
status: Draft            # Draft | Review | Approved | Deprecated
owner: <Tên người phụ trách>
updated: 2026-09-29
---

# AIG-12 - Triển khai và vận hành model

Nhóm bài toán AI (capability) trong luồng xử lý hồ sơ. Danh sách mọi nhóm và sơ đồ luồng xem [README](README.md).

## 1. Bài toán nghiệp vụ

Chọn nơi chạy model đáp ứng ràng buộc dữ liệu cá nhân, phân tầng model theo độ khó, giữ chi phí và độ trễ trong ngưỡng, phát hiện dữ liệu thực tế trôi khỏi dữ liệu đã đánh giá.

## 2. Vị trí trong luồng

**Bước:** Xuyên suốt: triển khai, vận hành.

| | Nội dung |
|---|---|
| Đầu vào | Yêu cầu bảo mật dữ liệu, ngân sách, SLA; số liệu vận hành |
| Đầu ra | Kiến trúc triển khai, chính sách chọn model, cảnh báo drift |
| Nhận từ | Mọi nhóm |
| Chuyển cho | Mọi nhóm |

## 3. Đánh giá cấp nhóm

Chỉ số cho biết cả nhóm có đạt không, đo trên golden set [AIP-026](AIP-026-layered-golden-set.md). Chỉ số chi tiết nằm trong từng bài toán con.

| Chỉ số | Ngưỡng chấp nhận |
|---|---|
| Chi phí và độ trễ trên mỗi hồ sơ | `[CẦN XÁC NHẬN]` |
| Thời gian phát hiện drift | `[CẦN XÁC NHẬN]` |

## 4. Bài toán con

Mỗi bài toán con là một file `AIP` riêng, có mức ưu tiên, giai đoạn và nhật ký thử nghiệm riêng. Ý nghĩa cột "Loại" xem [README](README.md) mục 3.

| Mã | Bài toán | Loại | Ưu tiên | Thử nghiệm sớm |
|---|---|---|---|---|
| [AIP-034](AIP-034-data-privacy-hosting.md) | Model nội bộ hay API ngoài, bảo vệ dữ liệu cá nhân | Rủi ro | Must |  |
| [AIP-035](AIP-035-model-serving-cost-latency.md) | Phân tầng model, tối ưu chi phí và độ trễ | Hỗ trợ | Should |  |
| [AIP-036](AIP-036-drift-detection.md) | Drift detection | Hỗ trợ | Could |  |

## 5. Lịch sử thay đổi

| Ngày | Người sửa | Nội dung | Đã rà tham chiếu |
|---|---|---|---|
| 2026-09-29 | binhnguyenSoftz | Tạo mới khi tổ chức lại bài toán AI thành 13 nhóm | Không cần |
