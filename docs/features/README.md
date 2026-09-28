# Bảng tra cứu tính năng

Đây là nơi **duy nhất** để cấp mã. Trước khi viết tài liệu mới, thêm một dòng vào bảng, rồi mới tạo thư mục.

## 1. Danh sách module

| Mã module | Tên | Người phụ trách |
|---|---|---|
| `PAY` | Thanh toán | |
| `AUT` | Xác thực | |

## 2. Danh sách tính năng

| Mã | Tên tính năng | Module | Trạng thái | Người phụ trách | Thư mục |
|---|---|---|---|---|---|
| `PAY-001` | Thanh toán QR (ví dụ) | PAY | Draft | | [PAY/PAY-001-qr-payment](PAY/PAY-001-qr-payment/00-index.md) |

## 3. Cách thêm một tính năng mới

1. Tìm mã lớn nhất của module trong bảng, cộng thêm 1. Ví dụ `PAY-001` thì tiếp theo là `PAY-002`.
2. Thêm dòng mới vào bảng. Trạng thái `Draft`.
3. Tạo thư mục `features/<MODULE>/<MÃ>-<short-name>/`.
4. Copy `templates/TPL-FEATURE-index.md` thành `00-index.md` trong thư mục đó.
5. Mở merge request. Việc cấp mã và tạo thư mục nên đi cùng nhau để hai người không lấy trùng mã.
