---
id: API-<MODULE>-<NNN>
feature: <MODULE>-<NNN>
title: <Tên tính năng> - API
status: Draft
owner: <Tên>
updated: <YYYY-MM-DD>
---

# API-<MODULE>-<NNN> - <Tên tính năng> (API)

## 1. Danh sách API

| Mã | Method | Đường dẫn | Mô tả ngắn |
|---|---|---|---|
| API-<MODULE>-<NNN>.1 | POST | `/v1/<resource>` | <Tạo ...> |
| API-<MODULE>-<NNN>.2 | GET | `/v1/<resource>/{id}` | <Xem ...> |

## 2. Chung cho mọi API

- Xác thực: <Bearer token trong header `Authorization`>.
- Định dạng: `application/json`.
- Header bắt buộc: <`X-Tenant-Id`, `X-Request-Id`>.

## 3. API-<MODULE>-<NNN>.1 - <Tên API>

**Khi nào gọi:** <Một câu.>

### Request

| Tham số | Vị trí | Kiểu | Bắt buộc | Mô tả | Ví dụ |
|---|---|---|---|---|---|
| `amount` | body | number | Có | <Số tiền, đơn vị đồng> | `500000` |

```json
{
  "amount": 500000,
  "currency": "VND"
}
```

### Response thành công (200)

```json
{
  "id": "b7f1...",
  "status": "PENDING"
}
```

| Trường | Kiểu | Mô tả |
|---|---|---|
| `id` | string | <Mã giao dịch> |
| `status` | string | <PENDING, SUCCESS, FAILED> |

### Response lỗi

| HTTP | Mã lỗi | Khi nào | Thông điệp |
|---|---|---|---|
| 400 | <MODULE>-E001 | <Thiếu tham số> | <...> |
| 422 | <MODULE>-E002 | <Vi phạm quy tắc nghiệp vụ> | <...> |

### Ví dụ gọi

```bash
curl -X POST https://<host>/v1/<resource> \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{"amount":500000,"currency":"VND"}'
```

## 4. Tài liệu tham chiếu

Quy tắc ghi: `standards/07-references.md`. Không liệt kê các file cùng thư mục tính năng.

| Mã | Tài liệu | Chiều | Nội dung liên quan |
|---|---|---|---|
| <TEC-002> | [<Tên>](<đường dẫn tương đối>) | <Dựa vào / Được dùng bởi> | <Mục, mã quy tắc, bảng hoặc API liên quan> |

## 5. Lịch sử thay đổi

| Ngày | Người sửa | Nội dung | Đã rà tham chiếu |
|---|---|---|---|
| <YYYY-MM-DD> | <Tên> | Tạo mới | Không cần |
