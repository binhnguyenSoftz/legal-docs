# 03 - Văn phong

Mục tiêu: người mới vào dự án đọc một lần là hiểu và làm theo được.

## 1. Nguyên tắc

1. **Viết như đang giải thích cho đồng nghiệp ngồi bên cạnh.** Gần gũi, rõ ràng, không cần trang trọng.
2. **Một câu một ý.** Câu quá 25 từ thì tách đôi.
3. **Nói cái gì, vì sao, rồi làm thế nào.** Đừng chỉ liệt kê bước mà không nói lý do.
4. **Ưu tiên ví dụ cụ thể** (có số liệu, có giá trị mẫu) hơn mô tả chung chung.
5. **Dùng liên từ để nối ý:** vì vậy, do đó, tuy nhiên, ngoài ra, sau đó, nếu... thì, trong trường hợp.
6. **Dùng thuật ngữ nhất quán.** Một khái niệm chỉ có một tên. Ghi vào bảng thuật ngữ của tài liệu.
7. **Viết chủ động.** "Hệ thống gửi OTP" thay cho "OTP sẽ được gửi bởi hệ thống".

## 2. Từ nên tránh và cách thay

| Tránh | Thay bằng |
|---|---|
| tận dụng sức mạnh của | dùng |
| đóng vai trò then chốt | quan trọng vì... (nói rõ lý do) |
| giải pháp toàn diện, tối ưu | nói cụ thể giải quyết vấn đề gì |
| mượt mà, liền mạch, đột phá | bỏ, hoặc nêu số liệu (nhanh hơn bao nhiêu) |
| đảm bảo tính nhất quán và toàn vẹn | dữ liệu hai bên luôn khớp nhau |
| triển khai một cách hiệu quả | nói triển khai thế nào |
| hệ sinh thái, cảnh quan, hành trình | bỏ hoặc gọi đúng tên |
| Lưu ý rằng / Điều quan trọng cần nhớ | Đặt trong khối `> Lưu ý:` và nói thẳng nội dung |

Quy tắc chung: nếu bỏ một từ đi mà câu vẫn đủ nghĩa, hãy bỏ.

## 3. Ví dụ viết lại

Chưa tốt:

> Hệ thống tận dụng cơ chế bất đồng bộ để đảm bảo trải nghiệm thanh toán mượt mà và toàn diện.

Tốt hơn:

> Sau khi khách bấm thanh toán, hệ thống trả kết quả "đang xử lý" ngay. Việc gọi sang ngân hàng chạy nền. Nhờ vậy khách không phải chờ màn hình quay khi ngân hàng phản hồi chậm.

## 4. Cách viết các phần thường gặp

**Mô tả bước làm.** Đánh số, mỗi bước bắt đầu bằng động từ, nói rõ ai làm.

```markdown
1. Khách bấm "Thanh toán" trên màn hình giỏ hàng.
2. Hệ thống kiểm tra số dư. Nếu không đủ, hiện thông báo lỗi `PAY-E004` và dừng.
3. Nếu đủ, hệ thống tạo giao dịch với trạng thái `PENDING`.
```

**Mô tả điều kiện.** Viết dạng "Nếu ... thì ...", mỗi nhánh một dòng.

**Mô tả lỗi.** Dùng bảng: mã lỗi, khi nào xảy ra, hệ thống làm gì, người dùng thấy gì.

**Ghi chú quan trọng.** Dùng khối trích dẫn và bắt đầu bằng nhãn cố định:

```markdown
> Lưu ý: ...
> Cảnh báo: ...   (có thể mất dữ liệu hoặc tiền)
> Ví dụ: ...
```

## 5. Ngôn ngữ

- Viết tiếng Việt có dấu. Tên kỹ thuật, tên biến, lệnh, endpoint giữ nguyên tiếng Anh và đặt trong dấu backtick.
- Lần đầu dùng từ viết tắt thì viết đầy đủ: "One-Time Password (OTP)".
- Không trộn tiếng Anh vào câu văn khi đã có từ tiếng Việt quen thuộc ("yêu cầu" thay cho "requirement", trừ khi cả nhóm quen dùng từ gốc).

## 6. Định dạng

- Tiêu đề: `#` một lần cho tên tài liệu, `##` cho mục chính, `###` cho mục con. Không nhảy cấp.
- Đánh số mục chính: `## 1. ...`, `## 2. ...` để dễ nhắc ("xem mục 3").
- Danh sách: dùng khi có từ 3 ý ngang hàng trở lên. Ít hơn thì viết thành câu.
- Bảng: dùng cho dữ liệu có nhiều cột (lỗi, tham số, trạng thái).
- Mã, JSON, lệnh: đặt trong khối code có ghi loại (` ```json `, ` ```bash `).
- Độ dài đoạn: tối đa khoảng 5 câu.
