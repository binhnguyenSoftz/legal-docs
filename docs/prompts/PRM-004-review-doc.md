---
id: PRM-004
title: Review tài liệu
status: Approved
updated: <YYYY-MM-DD>
---

# PRM-004 - Review tài liệu

## 1. Mục đích

Kiểm tra một tài liệu có đúng cấu trúc, văn phong và đủ nội dung trước khi mở merge request.

## 2. Khi nào dùng

Sau khi viết xong bản nháp, hoặc khi được giao review tài liệu của người khác.

## 3. Đầu vào cần chuẩn bị

- Nội dung tài liệu cần review.
- Loại tài liệu (nghiệp vụ, kỹ thuật, API, sequence).
- Template tương ứng.
- Code liên quan (nếu là tài liệu kỹ thuật) để đối chiếu.

## 4. Prompt

```text
Hãy review tài liệu bên dưới theo quy tắc chung (PRM-000) và template <LOẠI>. Chỉ liệt kê vấn đề, không viết lại cả tài liệu.

Kiểm tra theo thứ tự:
1. Cấu trúc: có đủ mọi mục của template không? Thứ tự và đánh số đúng không? Tiêu đề có nhảy cấp không?
2. Thông tin đầu file: mã tài liệu, mã tính năng, trạng thái, người phụ trách, ngày cập nhật.
3. Đầy đủ nội dung: có luồng chính, luồng ngoại lệ, mã lỗi, ví dụ cụ thể? Có nói rõ phạm vi "không làm"?
4. Nhất quán: một khái niệm có bị gọi bằng nhiều tên không? Mã bước, mã yêu cầu, mã lỗi có trùng hoặc nhảy số không?
5. Văn phong: tìm câu dài trên 25 từ, câu bị động, từ hoa mỹ hoặc mơ hồ, liên từ thiếu khiến ý bị rời rạc.
6. Sơ đồ: mỗi sơ đồ có tiêu đề và diễn giải? Số bước trong diễn giải khớp sơ đồ? Có vượt 10 đối tượng hoặc 15 bước?
7. Độ dài: file có vượt 300 dòng hoặc hơn 7 mục lớn? Nếu có, đề xuất tách.
8. Đối chiếu code (nếu có): tên lớp, bảng, cột, endpoint, giá trị cấu hình có khớp không?
9. Tài liệu tham chiếu: có mục này không? Mỗi dòng có đủ Mã, liên kết, Chiều, Nội dung liên quan cụ thể? Nội dung kỹ thuật dùng chung có bị chép lại thay vì trỏ tới tài liệu TEC? Dòng mới nhất của "Lịch sử thay đổi" đã điền cột "Đã rà tham chiếu"?

Định dạng kết quả là bảng với các cột: Mức độ (Sai / Thiếu / Nên sửa), Vị trí (mục hoặc dòng), Vấn đề, Đề xuất sửa.
Sau bảng, ghi một dòng kết luận: có thể mở merge request chưa, và cần sửa những gì trước.
Nếu không thấy vấn đề ở một hạng mục, ghi "Đạt" cho hạng mục đó.

Tài liệu:
<DÁN TÀI LIỆU>

Template:
<DÁN TEMPLATE>

Code (nếu có):
<DÁN CODE>
```

## 5. Kết quả mong đợi

Một bảng vấn đề rõ vị trí, rõ cách sửa, xếp theo mức độ. Người viết sửa được ngay mà không cần hỏi lại.

## 6. Lịch sử thay đổi

| Ngày | Người sửa | Nội dung |
|---|---|---|
| <YYYY-MM-DD> | <Tên> | Tạo mới |
