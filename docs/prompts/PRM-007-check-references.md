---
id: PRM-007
title: Rà tài liệu tham chiếu khi cập nhật
status: Approved
updated: <YYYY-MM-DD>
---

# PRM-007 - Rà tài liệu tham chiếu

## 1. Mục đích

Sau khi sửa một tài liệu, tìm ra các tài liệu tham chiếu cần sửa theo và nói rõ sửa chỗ nào. Làm theo quy trình ở `standards/07-references.md` mục 4.

## 2. Khi nào dùng

Sửa nội dung một tài liệu trong `features/` hoặc `techs/`, nhất là khi đổi quy tắc, dữ liệu, API hoặc luồng xử lý. Sửa chính tả, định dạng thì không cần.

## 3. Đầu vào cần chuẩn bị

- Diff của tài liệu vừa sửa (hoặc bản cũ và bản mới).
- Mục "Tài liệu tham chiếu" của tài liệu đó.
- Kết quả tìm mã tài liệu trong repo: `grep -rn "<MÃ>" docs/`.
- Nội dung các tài liệu tham chiếu. Chỉ dán phần ghi trong cột "Nội dung liên quan", không cần dán cả file.

## 4. Prompt

```text
Tôi vừa sửa tài liệu <MÃ> - <TÊN>. Hãy rà các tài liệu tham chiếu theo quy tắc chung (PRM-000). Chỉ phân tích, không viết lại tài liệu.

Cách làm:
1. Tóm tắt thay đổi trong diff: mục nào, mã quy tắc/bảng/API/bước nào đổi, đổi thế nào.
2. So kết quả grep với bảng tham chiếu. Liệt kê tài liệu có trỏ tới <MÃ> nhưng chưa có trong bảng, và dòng trong bảng mà grep không thấy (có thể đã hết liên quan).
3. Với từng tài liệu trong bảng và danh sách bổ sung:
   - Chiều "Được dùng bởi": phần đã sửa có đụng tới nội dung tài liệu kia đang dùng không? Có thì chỉ rõ đoạn nào sai và cần đổi thành gì.
   - Chiều "Dựa vào": thay đổi có còn khớp với tài liệu gốc không? Không khớp thì nói rõ vi phạm quy tắc nào, đề xuất sửa tài liệu gốc hoặc viết ADR.
4. Kiểm tra tham chiếu hai chiều: dòng nào đang thiếu ở phía tài liệu kia.
5. Viết sẵn nội dung cho cột "Đã rà tham chiếu" của lịch sử thay đổi.

Định dạng kết quả là bảng với các cột: Mã tài liệu, Chiều, Kết luận (Phải sửa / Không ảnh hưởng / Cần xác nhận), Vị trí cần sửa, Đề xuất sửa.
Sau bảng, liệt kê: các dòng tham chiếu cần thêm hoặc xóa, và dòng ghi cho cột "Đã rà tham chiếu".
Tài liệu nào tôi chưa dán nội dung thì kết luận "Cần xác nhận", không đoán.

Diff:
<DÁN DIFF>

Mục "Tài liệu tham chiếu" hiện tại:
<DÁN BẢNG>

Kết quả grep:
<DÁN KẾT QUẢ>

Nội dung tài liệu tham chiếu:
<DÁN TỪNG PHẦN, GHI RÕ MÃ>
```

## 5. Kết quả mong đợi

Một bảng cho biết tài liệu nào phải sửa, sửa ở đâu, sửa thành gì. Kèm danh sách dòng tham chiếu cần bổ sung và nội dung cột "Đã rà tham chiếu" để dán vào lịch sử thay đổi.

## 6. Ví dụ

> Ví dụ: sửa `TEC-003-R02` từ "tên bảng số ít" thành "tên bảng số nhiều". Kết quả: `PAY-001` phải sửa mục 4.1 (`transaction` thành `transactions`); `PAY-002` không ảnh hưởng vì chỉ đọc bảng; grep thấy `AUT-003` có nhắc `TEC-003` nhưng chưa có trong bảng, cần bổ sung ở cả hai phía. Dòng lịch sử: `PAY-001: đã sửa; PAY-002: không ảnh hưởng; AUT-003: cần xác nhận`.

## 7. Lịch sử thay đổi

| Ngày | Người sửa | Nội dung |
|---|---|---|
| <YYYY-MM-DD> | <Tên> | Tạo mới |
