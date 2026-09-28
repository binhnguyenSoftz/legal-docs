---
id: AIP-015
title: Truy xuất theo hiệu lực thời gian
group: AIG-06
kind: problem            # problem | method | concern | enabler
status: Draft            # Draft | Review | Approved | Deprecated
stage: Defined           # Defined | Exploring | Decided | In production
priority: Must           # Must | Should | Could
early_test: true         # true: nằm trong nhóm khó nhất, thử nghiệm sớm
owner: <Tên người phụ trách>
updated: 2026-09-29
---

# AIP-015 - Truy xuất theo hiệu lực thời gian

## 1. Định nghĩa

### 1.1. Phát biểu bài toán

Với thời điểm phát sinh hồ sơ (ngày mở thừa kế, ngày ký hợp đồng, ngày nộp), chỉ trả về phiên bản điều khoản có hiệu lực tại thời điểm đó, tính cả sửa đổi, thay thế và điều khoản chuyển tiếp.

**Ví dụ:** người để lại di sản mất năm 2019 nhưng hồ sơ nộp năm 2026. Với câu hỏi về điều kiện thừa kế, hệ thống phải lấy đúng quy định áp dụng theo điều khoản chuyển tiếp, không lấy mặc định văn bản mới nhất.

**Phạm vi:**

- Gồm: lọc theo hiệu lực; xử lý điều khoản chuyển tiếp.
- Không gồm: tìm điều khoản liên quan (AIP-014), dựng quan hệ văn bản (AIP-016).

### 1.2. Vị trí trong luồng

**Bước:** Truy xuất pháp luật (nhóm [AIG-06](AIG-06-legal-retrieval.md) - Truy xuất pháp luật theo hiệu lực). Sơ đồ luồng xem [README](README.md).

- Dựa vào: [AIP-014](AIP-014-legal-retrieval.md) - Truy xuất điều khoản pháp luật tiếng Việt; [AIP-016](AIP-016-legal-document-relations.md) - Quan hệ giữa văn bản pháp luật
- Được dùng bởi: [AIP-012](AIP-012-missing-document-detection.md) - Phát hiện thiếu giấy tờ; [AIP-018](AIP-018-retrieval-evaluation.md) - Đánh giá retrieval; [AIP-019](AIP-019-legal-reasoning.md) - Suy luận pháp lý; [AIP-024](AIP-024-citation-grounding.md) - Grounding trích dẫn pháp lý; [AIP-036](AIP-036-drift-detection.md) - Drift detection

### 1.3. Đầu vào và đầu ra

| | Nội dung | Ví dụ |
|---|---|---|
| Đầu vào | Truy vấn, thời điểm phát sinh hồ sơ, quan hệ văn bản (AIP-016) | - |
| Đầu ra | Chunk đúng phiên bản có hiệu lực | - |

### 1.4. Ràng buộc bắt buộc

| Mã | Ràng buộc | Lý do |
|---|---|---|
| AIP-015-R01 | Chỉ dùng phiên bản văn bản có hiệu lực tại thời điểm phát sinh hồ sơ. | Áp văn bản sai thời điểm là sai căn cứ pháp lý. |

## 2. Vì sao khó

### 2.1. Thách thức

- Văn bản bị sửa đổi, thay thế nhiều lần.
- Có quy định chuyển tiếp.

### 2.2. Chi phí khi sai

Áp văn bản hết hiệu lực hoặc chưa có hiệu lực dẫn tới quyết định sai căn cứ.

## 3. Đánh giá

| Chỉ số | Cách đo | Ngưỡng chấp nhận |
|---|---|---|
| Tỉ lệ lấy đúng phiên bản | Trên bộ câu hỏi có nhãn thời điểm | `[CẦN XÁC NHẬN]` |

## 4. Hướng tiếp cận và thử nghiệm

### 4.1. Hướng tiếp cận ứng viên

| Hướng | Ưu điểm | Nhược điểm |
|---|---|---|
| `[CẦN XÁC NHẬN]` Chưa khảo sát thêm | | |

### 4.2. Dữ liệu cần chuẩn bị

- Metadata hiệu lực của từng văn bản và từng điều.

### 4.3. Nhật ký thử nghiệm

| Ngày | Thử nghiệm | Kết quả | Kết luận |
|---|---|---|---|
| | | | |

## 5. Câu hỏi còn mở

- [ ] Thời điểm phát sinh hồ sơ được xác định theo mốc nào?

## 6. Tài liệu tham chiếu

Quy tắc ghi: `standards/07-references.md`.

| Mã | Tài liệu | Chiều | Nội dung liên quan |
|---|---|---|---|
| `AIP-014` | [Truy xuất điều khoản pháp luật tiếng Việt](AIP-014-legal-retrieval.md) | Dựa vào | Lọc kết quả retrieval theo hiệu lực |
| `AIP-016` | [Quan hệ giữa văn bản pháp luật](AIP-016-legal-document-relations.md) | Dựa vào | Dùng quan hệ sửa đổi, thay thế để xác định phiên bản |
| `AIP-012` | [Phát hiện thiếu giấy tờ](AIP-012-missing-document-detection.md) | Được dùng bởi | Lấy danh mục giấy tờ theo quy định có hiệu lực |
| `AIP-018` | [Đánh giá retrieval](AIP-018-retrieval-evaluation.md) | Được dùng bởi | Đo tỉ lệ lấy đúng phiên bản |
| `AIP-019` | [Suy luận pháp lý](AIP-019-legal-reasoning.md) | Được dùng bởi | Áp dụng điều khoản có hiệu lực |
| `AIP-024` | [Grounding trích dẫn pháp lý](AIP-024-citation-grounding.md) | Được dùng bởi | Chỉ trích dẫn điều luật từ kết quả truy xuất |
| `AIP-036` | [Drift detection](AIP-036-drift-detection.md) | Được dùng bởi | Theo dõi thay đổi quy định |

## 7. Lịch sử thay đổi

| Ngày | Người sửa | Nội dung | Đã rà tham chiếu |
|---|---|---|---|
| 2026-09-28 | <Tên> | Tạo mới, định nghĩa ban đầu từ danh sách bài toán AI của luồng | Không cần |
| 2026-09-29 | binhnguyenSoftz | Tổ chức lại: đổi mã từ AIP-022 cũ; nhóm `AIG-06`, thêm `kind`; viết lại phát biểu bài toán | Có |
