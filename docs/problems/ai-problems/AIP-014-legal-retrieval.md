---
id: AIP-014
title: Truy xuất điều khoản pháp luật tiếng Việt
group: AIG-06
kind: problem            # problem | method | concern | enabler
status: Draft            # Draft | Review | Approved | Deprecated
stage: Defined           # Defined | Exploring | Decided | In production
priority: Must           # Must | Should | Could
early_test: false        # true: nằm trong nhóm khó nhất, thử nghiệm sớm
owner: <Tên người phụ trách>
updated: 2026-09-29
---

# AIP-014 - Truy xuất điều khoản pháp luật tiếng Việt

## 1. Định nghĩa

### 1.1. Phát biểu bài toán

Đưa kho văn bản pháp luật liên quan tới các thủ tục vào chỉ mục, cắt theo đơn vị điều, khoản, điểm. Với một câu hỏi hoặc một sự kiện trong hồ sơ, trả về danh sách điều khoản liên quan xếp theo mức độ liên quan, mỗi kết quả giữ nguyên định danh điều/khoản/điểm và văn bản gốc.

**Ví dụ** (minh họa, cần chuyên viên pháp lý xác nhận số điều): câu truy vấn "điều kiện để người thừa kế đăng ký biến động quyền sử dụng đất" trả về: Điều 45 khoản 1 Luật Đất đai (điều kiện thực hiện quyền), điều khoản về hồ sơ đăng ký biến động trong nghị định hướng dẫn, và điều khoản về khai nhận di sản trong Bộ luật Dân sự.

**Phạm vi:**

- Gồm: chunking theo cấu trúc pháp lý; embedding, tìm kiếm từ khóa (BM25), hybrid search, reranking.
- Không gồm: lọc theo hiệu lực tại thời điểm hồ sơ (AIP-015), dựng quan hệ sửa đổi/thay thế (AIP-016), đo chất lượng retrieval (AIP-018).

### 1.2. Vị trí trong luồng

**Bước:** Truy xuất pháp luật (nhóm [AIG-06](AIG-06-legal-retrieval.md) - Truy xuất pháp luật theo hiệu lực). Sơ đồ luồng xem [README](README.md).

- Dựa vào: không có.
- Được dùng bởi: [AIP-015](AIP-015-temporal-validity-retrieval.md) - Truy xuất theo hiệu lực thời gian; [AIP-018](AIP-018-retrieval-evaluation.md) - Đánh giá retrieval

### 1.3. Đầu vào và đầu ra

| | Nội dung | Ví dụ |
|---|---|---|
| Đầu vào | Kho văn bản pháp luật gốc; câu truy vấn hoặc sự kiện trong hồ sơ | "Điều kiện đăng ký biến động do thừa kế" |
| Đầu ra | Danh sách chunk xếp hạng, mỗi chunk gắn định danh điều/khoản/điểm và metadata văn bản (số hiệu, ngày ban hành) | `[{doc: "31/2024/QH15", article: 45, clause: 1, score: 0,91}, ...]` |

### 1.4. Ràng buộc bắt buộc

Chưa có. Bổ sung khi đi sâu vào bài toán, đánh mã `AIP-014-R01`, `R02`...

### 1.5. Bài toán con

| Bài toán con | Mã cũ | Ưu tiên | Nội dung |
|---|---|---|---|
| Chunking theo cấu trúc pháp lý | AIP-020 cũ | Must | Cắt theo điều, khoản, điểm thay vì theo độ dài |
| Embedding và retrieval tiếng Việt pháp lý | AIP-021 cũ | Must | Tìm và xếp hạng điều khoản liên quan |

## 2. Vì sao khó

### 2.1. Thách thức

- Định dạng văn bản nguồn không đồng nhất.
- Khoản, điểm tham chiếu lẫn nhau ("trừ trường hợp quy định tại khoản 3 Điều này").
- Chọn hoặc fine-tune embedding model cho tiếng Việt pháp lý.
- Kết hợp hybrid search (BM25 + vector) và reranking.

### 2.2. Chi phí khi sai

- Chunk sai ranh giới làm mất điều kiện hoặc ngoại lệ của một điều.
- Không tìm ra điều luật cần thiết thì suy luận thiếu căn cứ.

## 3. Đánh giá

| Chỉ số | Cách đo | Ngưỡng chấp nhận |
|---|---|---|
| Tỉ lệ chunk đúng ranh giới | `[CẦN XÁC NHẬN]` | `[CẦN XÁC NHẬN]` |
| recall@k | Đo ở AIP-018 | `[CẦN XÁC NHẬN]` |

## 4. Hướng tiếp cận và thử nghiệm

### 4.1. Hướng tiếp cận ứng viên

| Hướng | Ưu điểm | Nhược điểm |
|---|---|---|
| Cắt theo cấu trúc điều/khoản/điểm | Giữ trọn ý pháp lý | `[CẦN XÁC NHẬN]` |
| Hybrid search BM25 + vector | `[CẦN XÁC NHẬN]` | `[CẦN XÁC NHẬN]` |
| Reranking | `[CẦN XÁC NHẬN]` | `[CẦN XÁC NHẬN]` |
| Fine-tune embedding | `[CẦN XÁC NHẬN]` | `[CẦN XÁC NHẬN]` |
| `[CẦN XÁC NHẬN]` Chưa khảo sát thêm | | |

### 4.2. Dữ liệu cần chuẩn bị

- Kho văn bản pháp luật liên quan tới các thủ tục.
- Cặp câu hỏi và điều luật đúng.

### 4.3. Nhật ký thử nghiệm

| Ngày | Thử nghiệm | Kết quả | Kết luận |
|---|---|---|---|
| | | | |

## 5. Câu hỏi còn mở

- [ ] Nguồn văn bản pháp luật lấy từ đâu và định dạng gì?

## 6. Tài liệu tham chiếu

Quy tắc ghi: `standards/07-references.md`.

| Mã | Tài liệu | Chiều | Nội dung liên quan |
|---|---|---|---|
| `AIP-015` | [Truy xuất theo hiệu lực thời gian](AIP-015-temporal-validity-retrieval.md) | Được dùng bởi | Lọc kết quả retrieval theo hiệu lực |
| `AIP-018` | [Đánh giá retrieval](AIP-018-retrieval-evaluation.md) | Được dùng bởi | Đo recall@k của retrieval |

## 7. Lịch sử thay đổi

| Ngày | Người sửa | Nội dung | Đã rà tham chiếu |
|---|---|---|---|
| 2026-09-28 | <Tên> | Tạo mới, định nghĩa ban đầu từ danh sách bài toán AI của luồng | Không cần |
| 2026-09-29 | binhnguyenSoftz | Tổ chức lại: gộp AIP-020 cũ (chunking) và AIP-021 cũ (embedding, retrieval); nhóm `AIG-06`; viết lại phát biểu bài toán | Có |
