---
id: TSK-<NNN>
title: "<Tên việc, bắt đầu bằng động từ>"
type: <Doc | Feature | Research | Infra | Bug | Chore>
priority: Should         # Must | Should | Could
status: Todo             # Todo | In progress | Blocked | Done | Cancelled
assignee:                # Bắt buộc khi In progress
due:                     # YYYY-MM-DD, bỏ trống nếu không có hạn thật
related: [<PAY-001>, <AIP-026>]
depends_on: [<TSK-xxx>]
created: <YYYY-MM-DD>
updated: <YYYY-MM-DD>
---

# TSK-<NNN> - <Tên việc>

## 1. Mục tiêu

<1-3 câu: làm việc này để được gì, ai cần kết quả.>

## 2. Phạm vi

**Làm:**

- <...>

**Không làm:**

- <...>

## 3. Tiêu chí hoàn thành

Việc chỉ được chuyển sang `Done` khi tick hết các mục dưới đây.

- [ ] <Kết quả kiểm tra được. Ví dụ: `03-api.md` của `PAY-001` đã `Approved`>
- [ ] <...>

## 4. Các bước

1. <Bước 1, bắt đầu bằng động từ>
2. <...>

## 5. Liên quan

| Mã | Tài liệu hoặc việc | Liên quan thế nào |
|---|---|---|
| <PAY-001> | [<Tên>](<đường dẫn tương đối>) | <Việc này viết/sửa mục nào, dùng nội dung gì> |
| <TSK-xxx> | [<Tên>](<TSK-xxx-short-name.md>) | <Phải xong trước: lý do> |

## 6. Vướng mắc và ghi chú

<Khi `Blocked`: ghi vướng gì, chờ ai hoặc chờ `TSK` nào. Câu hỏi chưa rõ ghi dạng `[CẦN XÁC NHẬN: ...]`. Không có thì ghi "Chưa có.".>

- [ ] <...>

## 7. Nhật ký

Ghi các mốc quan trọng: nhận việc, bị vướng, đổi phạm vi, xong (kèm liên kết merge request), huỷ (kèm lý do).

| Ngày | Người ghi | Nội dung |
|---|---|---|
| <YYYY-MM-DD> | <Tên> | Tạo việc |
