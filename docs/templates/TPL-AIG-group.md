---
id: AIG-<NN>
title: <Tên nhóm, nói năng lực AI cần có>
type: Luồng              # Luồng | Xuyên suốt
status: Draft            # Draft | Review | Approved | Deprecated
owner: <Tên người phụ trách>
updated: <YYYY-MM-DD>
---

# AIG-<NN> - <Tên nhóm>

Nhóm bài toán AI (capability) trong luồng xử lý hồ sơ. Danh sách mọi nhóm và sơ đồ luồng xem [README](README.md).

## 1. Bài toán nghiệp vụ

<1-3 câu: hệ thống cần làm được gì, vì sao luồng cần năng lực này. Nói theo nghiệp vụ, không nói theo kỹ thuật.>

## 2. Vị trí trong luồng

**Bước:** <Bước trong luồng, hoặc "Xuyên suốt: ...">.

| | Nội dung |
|---|---|
| Đầu vào | <...> |
| Đầu ra | <...> |
| Nhận từ | <[AIG-xx](...)> |
| Chuyển cho | <[AIG-xx](...)> |

## 3. Đánh giá cấp nhóm

Chỉ số cho biết cả nhóm có đạt không, đo trên golden set [AIP-026](AIP-026-layered-golden-set.md). Chỉ số chi tiết nằm trong từng bài toán con.

| Chỉ số | Ngưỡng chấp nhận |
|---|---|
| <...> | `[CẦN XÁC NHẬN]` |

## 4. Bài toán con

Mỗi bài toán con là một file `AIP` riêng, có mức ưu tiên, giai đoạn và nhật ký thử nghiệm riêng. Ý nghĩa cột "Loại" xem [README](README.md) mục 3.

| Mã | Bài toán | Loại | Ưu tiên | Thử nghiệm sớm |
|---|---|---|---|---|
| [AIP-<NNN>](AIP-<NNN>-<short-name>.md) | <Tên> | <Bài toán / Phương pháp / Rủi ro / Hỗ trợ> | <Must / Should / Could> | <Có / để trống> |

## 5. Lịch sử thay đổi

| Ngày | Người sửa | Nội dung | Đã rà tham chiếu |
|---|---|---|---|
| <YYYY-MM-DD> | <Tên> | Tạo mới | Không cần |
