---
id: AIP-018
title: Đánh giá retrieval
group: AIG-06
kind: enabler            # problem | method | concern | enabler
status: Draft            # Draft | Review | Approved | Deprecated
stage: Defined           # Defined | Exploring | Decided | In production
priority: Must           # Must | Should | Could
early_test: false        # true: nằm trong nhóm khó nhất, thử nghiệm sớm
owner: <Tên người phụ trách>
updated: 2026-09-29
---

# AIP-018 - Đánh giá retrieval

## 1. Định nghĩa

### 1.1. Phát biểu bài toán

Xây bộ câu hỏi có nhãn điều khoản đúng (kể cả thời điểm áp dụng) và đo hệ thống truy xuất tìm đúng tới đâu, để so các cách chunking, embedding, reranking bằng số liệu.

**Ví dụ:** bộ 200 câu hỏi từ hồ sơ thật, mỗi câu gắn các điều khoản đúng và ngày áp dụng. Chạy hai cấu hình retrieval, so recall@5 và tỉ lệ trả về điều khoản hết hiệu lực.

**Phạm vi:**

- Gồm: bộ câu hỏi có nhãn; chỉ số recall@k, MRR, tỉ lệ trả về văn bản hết hiệu lực.
- Không gồm: đánh giá toàn luồng (AIP-027).

### 1.2. Vị trí trong luồng

**Bước:** Truy xuất pháp luật (nhóm [AIG-06](AIG-06-legal-retrieval.md) - Truy xuất pháp luật theo hiệu lực). Sơ đồ luồng xem [README](README.md).

- Dựa vào: [AIP-014](AIP-014-legal-retrieval.md) - Truy xuất điều khoản pháp luật tiếng Việt; [AIP-015](AIP-015-temporal-validity-retrieval.md) - Truy xuất theo hiệu lực thời gian; [AIP-026](AIP-026-layered-golden-set.md) - Golden set và metric theo từng tầng
- Được dùng bởi: không có.

### 1.3. Đầu vào và đầu ra

| | Nội dung | Ví dụ |
|---|---|---|
| Đầu vào | Bộ câu hỏi có nhãn điều luật đúng | - |
| Đầu ra | recall@k và các chỉ số liên quan | - |

### 1.4. Ràng buộc bắt buộc

Chưa có. Bổ sung khi đi sâu vào bài toán, đánh mã `AIP-018-R01`, `R02`...

## 2. Vì sao khó

### 2.1. Thách thức

- Gán nhãn điều luật đúng cần chuyên viên pháp lý.

### 2.2. Chi phí khi sai

Không đo thì không biết retrieval có đủ tốt để dùng cho suy luận hay không.

## 3. Đánh giá

| Chỉ số | Cách đo | Ngưỡng chấp nhận |
|---|---|---|
| recall@k của đúng điều luật cần thiết | Trên golden set AIP-026 | `[CẦN XÁC NHẬN]` |

## 4. Hướng tiếp cận và thử nghiệm

### 4.1. Hướng tiếp cận ứng viên

| Hướng | Ưu điểm | Nhược điểm |
|---|---|---|
| `[CẦN XÁC NHẬN]` Chưa khảo sát thêm | | |

### 4.2. Dữ liệu cần chuẩn bị

- Bộ câu hỏi và điều luật đúng do chuyên viên gán nhãn.

### 4.3. Nhật ký thử nghiệm

| Ngày | Thử nghiệm | Kết quả | Kết luận |
|---|---|---|---|
| | | | |

## 5. Câu hỏi còn mở

- [ ] Giá trị k dùng để đánh giá là bao nhiêu?

## 6. Tài liệu tham chiếu

Quy tắc ghi: `standards/07-references.md`.

| Mã | Tài liệu | Chiều | Nội dung liên quan |
|---|---|---|---|
| `AIP-014` | [Truy xuất điều khoản pháp luật tiếng Việt](AIP-014-legal-retrieval.md) | Dựa vào | Đo recall@k của retrieval |
| `AIP-015` | [Truy xuất theo hiệu lực thời gian](AIP-015-temporal-validity-retrieval.md) | Dựa vào | Đo tỉ lệ lấy đúng phiên bản |
| `AIP-026` | [Golden set và metric theo từng tầng](AIP-026-layered-golden-set.md) | Dựa vào | Bộ câu hỏi nằm trong golden set |

## 7. Lịch sử thay đổi

| Ngày | Người sửa | Nội dung | Đã rà tham chiếu |
|---|---|---|---|
| 2026-09-28 | <Tên> | Tạo mới, định nghĩa ban đầu từ danh sách bài toán AI của luồng | Không cần |
| 2026-09-29 | binhnguyenSoftz | Tổ chức lại: đổi mã từ AIP-025 cũ; nhóm `AIG-06`, thêm `kind`; viết lại phát biểu bài toán | Có |
