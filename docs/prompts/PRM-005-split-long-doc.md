---
id: PRM-005
title: Tách tài liệu dài thành thư mục con
status: Approved
updated: <YYYY-MM-DD>
---

# PRM-005 - Tách tài liệu dài

## 1. Mục đích

Chia một file quá dài thành thư mục con, mỗi file một chủ đề, có file index dẫn đường.

## 2. Khi nào dùng

File dài hơn khoảng 300 dòng, hoặc có hơn 7 mục cấp 2, hoặc chứa nhiều luồng độc lập.

## 3. Đầu vào cần chuẩn bị

- Nội dung file cần tách.
- Đường dẫn hiện tại của file.
- Danh sách các file khác đang trỏ liên kết tới file này (nếu biết).

## 4. Prompt

```text
Hãy tách tài liệu bên dưới thành thư mục con theo quy chuẩn `standards/01-folder-structure.md`. Tuân thủ quy tắc chung (PRM-000).

Cách làm:
1. Đọc và nhóm nội dung theo chủ đề. Mỗi nhóm thành một file, đặt tên `NN-short-name.md` (tiếng Anh, chữ thường, gạch ngang).
2. Trước khi viết, cho tôi xem kế hoạch tách dưới dạng bảng: tên file mới, nội dung gồm những mục nào, khoảng bao nhiêu dòng. Chờ tôi đồng ý rồi mới viết.
3. Sau khi được đồng ý, viết `00-index.md` gồm: tóm tắt 3-5 câu, sơ đồ tổng quan nếu cần, bảng danh sách file con (tên, nội dung, liên kết).
4. Giữ nguyên nội dung gốc. Chỉ thêm liên kết chuyển tiếp ở đầu và cuối mỗi file con (trước/sau), không viết lại ý.
5. Giữ nguyên mã bước, mã yêu cầu, mã lỗi. Không đánh số lại.
6. Cuối cùng, liệt kê các liên kết cũ cần cập nhật do đường dẫn thay đổi, gồm cả liên kết trong mục "Tài liệu tham chiếu" của các tài liệu khác. Chuyển mỗi dòng tham chiếu của file gốc về đúng file con có nội dung liên quan.

Đường dẫn file hiện tại: <ĐƯỜNG DẪN>

Nội dung:
<DÁN NỘI DUNG>
```

## 5. Kết quả mong đợi

- Bảng kế hoạch tách để duyệt trước.
- Sau khi duyệt: `00-index.md` và các file con, mỗi file dưới khoảng 300 dòng, một chủ đề.
- Danh sách liên kết cũ cần sửa.

## 6. Lịch sử thay đổi

| Ngày | Người sửa | Nội dung |
|---|---|---|
| <YYYY-MM-DD> | <Tên> | Tạo mới |
