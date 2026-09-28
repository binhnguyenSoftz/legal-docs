---
id: PRM-001
title: Viết tài liệu nghiệp vụ
status: Approved
updated: <YYYY-MM-DD>
---

# PRM-001 - Viết tài liệu nghiệp vụ

## 1. Mục đích

Biến mô tả thô hoặc yêu cầu của bên nghiệp vụ thành tài liệu theo `templates/TPL-BIZ-business.md`.

## 2. Khi nào dùng

Có ghi chú cuộc họp, email, hoặc mô tả miệng về tính năng và cần một bản nghiệp vụ đầy đủ.

## 3. Đầu vào cần chuẩn bị

- Mã và tên tính năng.
- Mô tả thô: mục tiêu, ai dùng, luồng chính, các trường hợp đặc biệt đã biết.
- Quy tắc cụ thể đã biết (hạn mức, thời gian, điều kiện).
- Nội dung template `TPL-BIZ-business.md` (dán kèm).

## 4. Prompt

```text
Hãy viết tài liệu nghiệp vụ cho tính năng <MÃ> - <TÊN> theo đúng template tôi dán bên dưới. Tuân thủ quy tắc chung (PRM-000).

Cách làm:
1. Đọc mô tả thô và liệt kê các yêu cầu, gán mã <MÃ>-R01, R02, ...
2. Xác định các đối tượng tham gia và vai trò của từng đối tượng.
3. Viết luồng chính thành các bước đánh số (S01, S02, ...). Mỗi bước nói rõ ai làm, làm gì, và điều kiện rẽ nhánh nếu có.
4. Với mỗi bước có thể lỗi hoặc rẽ nhánh, thêm một dòng vào bảng luồng ngoại lệ.
5. Viết ít nhất một ví dụ có số liệu cụ thể.
6. Những điểm mô tả chưa rõ, ghi vào mục "Câu hỏi còn mở" dưới dạng câu hỏi cụ thể, kèm `[CẦN XÁC NHẬN]` tại chỗ liên quan.
7. Thêm sơ đồ tổng quan (flowchart) nếu có từ 3 đối tượng tham gia trở lên.

Mô tả thô:
<DÁN MÔ TẢ>

Quy tắc đã biết:
<DÁN QUY TẮC, hoặc ghi "chưa có">

Template:
<DÁN TEMPLATE>
```

## 5. Kết quả mong đợi

- Một file Markdown đầy đủ các mục của template, không bỏ mục nào (mục không áp dụng ghi "Không áp dụng" kèm lý do).
- Mỗi yêu cầu có mã. Mỗi bước có mã.
- Các chỗ thiếu thông tin được đánh dấu rõ, không bị đoán.

## 6. Ví dụ đoạn kết quả tốt

```markdown
## 6. Luồng xử lý chính

1. (S01) Khách chọn "Thanh toán QR" trên màn hình giỏ hàng.
2. (S02) Hệ thống kiểm tra đơn hàng còn hiệu lực. Nếu đơn đã hủy thì dừng và báo lỗi `PAY-E002`.
3. (S03) Nếu đơn hợp lệ, hệ thống tạo mã QR có hiệu lực 15 phút.
```

## 7. Lịch sử thay đổi

| Ngày | Người sửa | Nội dung |
|---|---|---|
| <YYYY-MM-DD> | <Tên> | Tạo mới |
