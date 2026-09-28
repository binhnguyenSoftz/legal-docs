# Tài liệu kỹ thuật chung

Thư mục này chứa tài liệu kỹ thuật dùng cho nhiều tính năng hoặc cả hệ thống: kiến trúc, hạ tầng, dữ liệu, bảo mật, tích hợp, hướng dẫn cho dev và quyết định kiến trúc (ADR). Tài liệu kỹ thuật của riêng một tính năng để trong `features/`.

Đây là nơi **duy nhất** để cấp mã `TEC` và `ADR`. Mã `AIG` (nhóm bài toán AI) và `AIP` (bài toán AI) cấp trong [ai-problems/README.md](ai-problems/README.md). Thêm một dòng vào bảng trước, rồi mới tạo file. Quy chuẩn chi tiết xem [06 - Tài liệu kỹ thuật chung](../standards/06-tech-docs.md).

## 1. Danh sách nhóm

| Thư mục | Nội dung | Người phụ trách |
|---|---|---|
| `architecture/` | Kiến trúc tổng thể, danh sách service, cách các service gọi nhau | |
| `infrastructure/` | Môi trường, triển khai, CI/CD, giám sát, log | |
| `data/` | Quy ước cơ sở dữ liệu, migration, sao lưu | |
| `security/` | Xác thực, phân quyền, mã hóa, quản lý secret | |
| `integrations/` | Hệ thống ngoài dùng chung | |
| `guides/` | Hướng dẫn cho dev: cài môi trường, quy ước code, cách debug | |
| [`ai-problems/`](ai-problems/README.md) | Nhóm (`AIG`) và bài toán AI (`AIP`) của luồng xử lý hồ sơ. Mã cấp trong README của thư mục này | |
| `adr/` | Quyết định kiến trúc | |

## 2. Danh sách tài liệu `TEC`

| Mã | Tên | Nhóm | Trạng thái | Người phụ trách | Liên kết |
|---|---|---|---|---|---|
| | | | | | |

## 3. Danh sách ADR

| Mã | Quyết định | Trạng thái | Ngày | Liên kết |
|---|---|---|---|---|
| | | | | |

## 4. Cách thêm một tài liệu mới

1. Kiểm tra nội dung có đúng thuộc `problems/` không (bảng ở mục 1 của `standards/06-tech-docs.md`).
2. Tìm mã lớn nhất trong bảng, cộng thêm 1. Ví dụ đang có `TEC-004` thì mã mới là `TEC-005`. ADR làm tương tự với `ADR-NNNN`.
3. Thêm dòng mới vào bảng. Trạng thái `Draft` (ADR là `Proposed`).
4. Copy `templates/TPL-TEC-topic.md` (hoặc `templates/TPL-ADR-decision.md`) vào thư mục nhóm, đặt tên `TEC-<NNN>-<short-name>.md`.
5. Điền mục "Tài liệu tham chiếu" và thêm dòng `Được dùng bởi` ở các tài liệu liên quan, theo `standards/07-references.md`.
6. Mở merge request. Cấp mã và tạo file đi cùng nhau để hai người không lấy trùng mã.
