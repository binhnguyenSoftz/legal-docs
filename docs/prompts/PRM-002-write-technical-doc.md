---
id: PRM-002
title: Viết tài liệu kỹ thuật và API
status: Approved
updated: <YYYY-MM-DD>
---

# PRM-002 - Viết tài liệu kỹ thuật và API

## 1. Mục đích

Từ code, thiết kế hoặc tài liệu nghiệp vụ, tạo ra `02-technical.md`, `03-api.md` và `04-sequence.md`.

## 2. Khi nào dùng

Tính năng đã có code (hoặc bản thiết kế) và cần tài liệu để người khác bảo trì, tích hợp.

## 3. Đầu vào cần chuẩn bị

- Mã và tên tính năng, link tới tài liệu nghiệp vụ (nếu có).
- Code liên quan: controller, service, entity, cấu hình. Dán đúng đoạn cần, không dán cả repo.
- Template cần dùng: `TPL-TECH-technical.md`, `TPL-API.md`, `TPL-SEQ-sequence-flow.md`.
- Danh sách tài liệu `TEC` và ADR liên quan (mã, tên, tóm tắt một dòng), lấy từ `techs/README.md`.

## 4. Prompt

```text
Hãy viết tài liệu kỹ thuật cho tính năng <MÃ> - <TÊN> từ code tôi cung cấp, theo các template đính kèm. Tuân thủ quy tắc chung (PRM-000).

Cách làm:
1. Đọc code và xác định: thành phần nào tham gia, gọi nhau qua giao thức gì, dữ liệu nào được đọc hoặc ghi.
2. Viết mục "Tóm tắt giải pháp" (3-5 câu), nói rõ làm theo cách nào và vì sao.
3. Vẽ sơ đồ kiến trúc (flowchart) và diễn giải từng thành phần.
4. Viết bảng dữ liệu (bảng, cột, kiểu, bắt buộc, ghi chú) từ entity/migration. Nếu có trạng thái, vẽ stateDiagram.
5. Viết sequence cho luồng chính (có autonumber) và luồng lỗi chính. Sau mỗi sơ đồ có bảng diễn giải theo bước.
6. Liệt kê cấu hình (tên, mặc định, ý nghĩa, ví dụ) từ file cấu hình trong code.
7. Liệt kê các lỗi mà code có thể trả về: điều kiện xảy ra, cách xử lý, có thử lại không.
8. Với từng API: bảng tham số, JSON request mẫu, JSON response mẫu, bảng lỗi, lệnh curl mẫu.
9. Bước "Cách chạy thử": viết các lệnh cụ thể, theo thứ tự, kèm kết quả mong đợi.

Yêu cầu bổ sung:
- Chỉ dùng thông tin có trong code tôi cung cấp. Chỗ code không cho biết (ví dụ giá trị cấu hình ở môi trường thật), ghi `[CẦN XÁC NHẬN]`.
- Tên lớp, hàm, bảng, cột phải khớp code, không đổi tên.
- Nếu tài liệu kỹ thuật vượt 300 dòng, dừng lại và đề xuất cách tách theo PRM-005.
- Phần nào đã có trong tài liệu TEC tôi liệt kê thì chỉ tóm tắt một dòng và trỏ liên kết, không viết lại. Ghi tài liệu đó vào mục "Tài liệu tham chiếu" với chiều "Dựa vào".
- Nếu code làm khác quy tắc trong tài liệu TEC, không sửa cho khớp mà ghi `[CẦN XÁC NHẬN: code làm khác TEC-<NNN>-R<NN>]`.
- Cuối cùng, liệt kê các tài liệu TEC cần thêm dòng "Được dùng bởi" trỏ về tài liệu này.

Code:
<DÁN CODE>

Tài liệu nghiệp vụ (nếu có):
<DÁN HOẶC GHI "không có">

Tài liệu TEC và ADR liên quan:
<DANH SÁCH HOẶC GHI "không có">

Template:
<DÁN CÁC TEMPLATE>
```

## 5. Kết quả mong đợi

- `02-technical.md`, `03-api.md`, `04-sequence.md` đủ mục theo template.
- Sơ đồ chạy được trên trình xem Mermaid, mỗi sơ đồ có diễn giải.
- Không có tên lớp, bảng hay cột mà code không có.

## 6. Cách kiểm tra kết quả

1. Đối chiếu từng tên lớp, bảng, cột, endpoint với code.
2. Chạy thử lệnh curl trong mục "Cách chạy thử".
3. Dán sơ đồ Mermaid vào trình xem để chắc chắn hiển thị được.

## 7. Lịch sử thay đổi

| Ngày | Người sửa | Nội dung |
|---|---|---|
| <YYYY-MM-DD> | <Tên> | Tạo mới |
