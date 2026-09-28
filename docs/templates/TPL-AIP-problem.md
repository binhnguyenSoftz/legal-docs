---
id: AIP-<NNN>
title: <Tên bài toán>
group: AIG-<NN>          # Nhóm chứa bài toán, xem problems/ai-problems/README.md mục 3.2
kind: problem            # problem | method | concern | enabler (xem README mục 3.1)
status: Draft            # Draft | Review | Approved | Deprecated
stage: Defined           # Defined | Exploring | Decided | In production
priority: Should         # Must | Should | Could (tiêu chí xem problems/ai-problems/README.md mục 2)
early_test: false        # true: nằm trong nhóm khó nhất, thử nghiệm sớm
owner: <Tên người phụ trách>
updated: <YYYY-MM-DD>
---

# AIP-<NNN> - <Tên bài toán>

## 1. Định nghĩa

### 1.1. Phát biểu bài toán

<1-3 câu: cần làm gì, cho ra kết quả gì, dùng vào đâu trong luồng.>

### 1.2. Vị trí trong luồng

**Bước:** <Bước trong luồng> (nhóm [AIG-<NN>](AIG-<NN>-<short-name>.md) - <Tên nhóm>). Sơ đồ luồng xem [README](README.md).

- Nhận đầu vào từ: <[AIP-xxx](...) - tên>
- Chuyển kết quả cho: <[AIP-xxx](...) - tên>

### 1.3. Đầu vào và đầu ra

| | Nội dung | Ví dụ |
|---|---|---|
| Đầu vào | <...> | <...> |
| Đầu ra | <...> | <...> |

### 1.4. Ràng buộc bắt buộc

| Mã | Ràng buộc | Lý do |
|---|---|---|
| AIP-<NNN>-R01 | <Phải / không được ...> | <Vì sao> |

## 2. Vì sao khó

### 2.1. Thách thức

- <...>

### 2.2. Chi phí khi sai

<Sai thì hậu quả gì cho người nộp hồ sơ và cán bộ duyệt. Sai kiểu nào đắt hơn.>

## 3. Đánh giá

| Chỉ số | Cách đo | Ngưỡng chấp nhận |
|---|---|---|
| <CER> | <Trên golden set AIP-026> | `[CẦN XÁC NHẬN]` |

## 4. Hướng tiếp cận và thử nghiệm

### 4.1. Hướng tiếp cận ứng viên

| Hướng | Ưu điểm | Nhược điểm |
|---|---|---|
| <...> | <...> | <...> |

### 4.2. Dữ liệu cần chuẩn bị

- <...>

### 4.3. Nhật ký thử nghiệm

| Ngày | Thử nghiệm | Kết quả | Kết luận |
|---|---|---|---|
| | | | |

## 5. Câu hỏi còn mở

- [ ] <...>

## 6. Tài liệu tham chiếu

Quy tắc ghi: `standards/07-references.md`.

| Mã | Tài liệu | Chiều | Nội dung liên quan |
|---|---|---|---|
| <AIP-xxx> | [<Tên>](<đường dẫn tương đối>) | <Dựa vào / Được dùng bởi> | <...> |

## 7. Lịch sử thay đổi

| Ngày | Người sửa | Nội dung | Đã rà tham chiếu |
|---|---|---|---|
| <YYYY-MM-DD> | <Tên> | Tạo mới | Không cần |
