---
id: BIZ-<MODULE>-<NNN>
feature: <MODULE>-<NNN>
title: <Tên tính năng> - Nghiệp vụ
status: Draft
owner: <Tên>
updated: <YYYY-MM-DD>
---

# BIZ-<MODULE>-<NNN> - <Tên tính năng> (Nghiệp vụ)

## 1. Mục tiêu

<Vì sao cần tính năng này? Ai được lợi? Viết 2-4 câu.>

## 2. Phạm vi

**Có làm:**
- <...>

**Không làm (để tránh hiểu nhầm):**
- <...>

## 3. Đối tượng tham gia

| Đối tượng | Vai trò trong tính năng |
|---|---|
| <Khách hàng> | <Bấm thanh toán> |
| <Hệ thống A> | <Tạo giao dịch> |

## 4. Thuật ngữ

| Thuật ngữ | Giải thích |
|---|---|
| <OTP> | <One-Time Password, mã dùng một lần> |

## 5. Yêu cầu nghiệp vụ

| Mã | Yêu cầu | Mức ưu tiên |
|---|---|---|
| <MÃ>-R01 | <Hệ thống phải...> | Bắt buộc |
| <MÃ>-R02 | <...> | Nên có |

## 6. Luồng xử lý chính

**Điều kiện trước:** <Người dùng đã đăng nhập, có số dư...>

1. <Ai> <làm gì>.
2. <Hệ thống> <kiểm tra gì>. Nếu <điều kiện> thì <kết quả>.
3. <...>

**Kết quả sau cùng:** <Trạng thái dữ liệu, thông báo người dùng thấy.>

## 7. Luồng ngoại lệ

| Mã bước | Tình huống | Hệ thống xử lý | Người dùng thấy |
|---|---|---|---|
| S02 | <Không đủ số dư> | <Dừng, không tạo giao dịch> | <Thông báo `XXX-E001`> |

## 8. Quy tắc nghiệp vụ

1. <Quy tắc tính toán, giới hạn, hạn mức. Kèm số cụ thể.>
2. <...>

## 9. Ví dụ minh họa

<Một tình huống thật với số liệu. Ví dụ: khách A thanh toán 500.000đ, số dư 800.000đ, kết quả...>

## 10. Câu hỏi còn mở

- [ ] <Điều cần hỏi bên nghiệp vụ>

## 11. Tài liệu tham chiếu

Quy tắc ghi: `standards/07-references.md`. Không liệt kê các file cùng thư mục tính năng.

| Mã | Tài liệu | Chiều | Nội dung liên quan |
|---|---|---|---|
| <PAY-002> | [<Tên>](<đường dẫn tương đối>) | <Dựa vào / Được dùng bởi> | <Mục, mã quy tắc, bảng hoặc API liên quan> |

## 12. Lịch sử thay đổi

| Ngày | Người sửa | Nội dung | Đã rà tham chiếu |
|---|---|---|---|
| <YYYY-MM-DD> | <Tên> | Tạo mới | Không cần |
