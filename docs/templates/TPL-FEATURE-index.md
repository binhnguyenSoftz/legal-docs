---
id: <MÃ TÍNH NĂNG, ví dụ PAY-001>
title: <Tên tính năng>
module: <PAY>
status: Draft            # Draft | Review | Approved | Deprecated
owner: <Tên người phụ trách>
updated: <YYYY-MM-DD>
---

# <MÃ> - <Tên tính năng>

## 1. Tóm tắt

<2-3 câu: tính năng làm gì, cho ai dùng, giải quyết vấn đề gì.>

## 2. Sơ đồ tổng quan

<Tiêu đề sơ đồ>

```mermaid
flowchart LR
    A[Người dùng] --> B[Thành phần 1]
    B --> C[Thành phần 2]
    C --> D[Hệ thống ngoài]
```

**Diễn giải:** <Mô tả ngắn các thành phần và vai trò của từng cái.>

## 3. Danh sách tài liệu

| Mã tài liệu | Nội dung | Trạng thái | Liên kết |
|---|---|---|---|
| BIZ-<MÃ> | Nghiệp vụ | Draft | [01-business.md](01-business.md) |
| TECH-<MÃ> | Kỹ thuật | Draft | [02-technical.md](02-technical.md) |
| API-<MÃ> | API | Draft | [03-api.md](03-api.md) |
| SEQ-<MÃ> | Sequence | Draft | [04-sequence.md](04-sequence.md) |

## 4. Tài liệu tham chiếu

Quy tắc ghi: `standards/07-references.md`. Ở file index, ghi quan hệ ở mức tính năng: tính năng khác, tài liệu `TEC`, ADR mà tính năng này dựa vào hoặc được dùng bởi. Chi tiết từng phần ghi ở mục tham chiếu của từng file con.

| Mã | Tài liệu | Chiều | Nội dung liên quan |
|---|---|---|---|
| <PAY-002> | [<Tên>](../PAY-002-refund/00-index.md) | <Dựa vào / Được dùng bởi> | <Gọi tới / được gọi từ / dùng chung dữ liệu gì> |
| <TEC-001> | [<Tên>](../../../techs/architecture/TEC-001-<short-name>.md) | Dựa vào | <Phần kiến trúc chung nào tính năng này dùng> |

## 5. Lịch sử thay đổi

| Ngày | Người sửa | Nội dung | Đã rà tham chiếu |
|---|---|---|---|
| <YYYY-MM-DD> | <Tên> | Tạo mới | Không cần |
