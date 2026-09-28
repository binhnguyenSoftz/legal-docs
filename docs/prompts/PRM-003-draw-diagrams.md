---
id: PRM-003
title: Vẽ sơ đồ Mermaid
status: Approved
updated: <YYYY-MM-DD>
---

# PRM-003 - Vẽ sơ đồ Mermaid

## 1. Mục đích

Tạo sơ đồ tổng quan, sequence hoặc trạng thái bằng Mermaid, kèm diễn giải theo bước.

## 2. Khi nào dùng

Cần sơ đồ cho một luồng đã mô tả bằng lời hoặc bằng code.

## 3. Đầu vào cần chuẩn bị

- Loại sơ đồ: tổng quan (flowchart), sequence, trạng thái (stateDiagram-v2), dữ liệu (erDiagram).
- Danh sách đối tượng tham gia và tên ngắn của từng đối tượng.
- Luồng chính bằng lời hoặc bằng code, kèm các nhánh lỗi.

## 4. Prompt

```text
Hãy vẽ sơ đồ <LOẠI> bằng Mermaid cho luồng "<TÊN LUỒNG>". Tuân thủ quy tắc chung (PRM-000).

Quy tắc vẽ:
- Sequence phải có `autonumber`. Dùng `actor` cho người, `participant` cho hệ thống.
- Tên đối tượng ngắn, giống tên dùng trong tài liệu.
- Tối đa 10 đối tượng và 15 bước. Nhiều hơn thì tách thành nhiều sơ đồ và nói rõ cách tách.
- Vẽ luồng thành công trước. Nhánh lỗi dùng `alt`/`else`, hoặc tách sơ đồ riêng nếu phức tạp.
- Nhãn có ký tự đặc biệt thì đặt trong dấu nháy kép.

Kết quả gồm 3 phần theo thứ tự:
1. Tiêu đề sơ đồ (một dòng).
2. Khối code Mermaid.
3. Bảng diễn giải theo bước với các cột: Bước, Ai làm, Việc gì, Vì sao.

Đầu vào:
- Đối tượng tham gia: <LIỆT KÊ>
- Luồng: <MÔ TẢ HOẶC DÁN CODE>
- Nhánh lỗi cần thể hiện: <LIỆT KÊ>
```

## 5. Kết quả mong đợi

Tiêu đề, sơ đồ hiển thị được, bảng diễn giải. Số bước trong bảng khớp số bước trong sơ đồ.

## 6. Lịch sử thay đổi

| Ngày | Người sửa | Nội dung |
|---|---|---|
| <YYYY-MM-DD> | <Tên> | Tạo mới |
