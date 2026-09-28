---
id: PRM-008
title: Tách và cập nhật việc cần làm
status: Draft
updated: 2026-09-28
---

# PRM-008 - Tách và cập nhật việc cần làm

## 1. Mục đích

Từ tài liệu, ghi chú họp hoặc kết quả rà tham chiếu, tách ra các việc cần làm theo đúng quy ước ở `todo/README.md`: mỗi việc một file theo `templates/TPL-TSK-task.md`.

## 2. Khi nào dùng

- Sau buổi họp, cần ghi lại các việc đã thống nhất.
- Đọc một tài liệu còn nhiều chỗ `[CẦN XÁC NHẬN]`, câu hỏi còn mở, hoặc `TODO`, cần biến thành việc có người làm.
- Rà tham chiếu (`PRM-007`) ra các tài liệu "Phải sửa" nhưng chưa sửa kịp trong merge request hiện tại.
- Cần cập nhật trạng thái hàng loạt từ danh sách merge request đã merge.

## 3. Đầu vào cần chuẩn bị

- Danh sách việc hiện có: kết quả lệnh `grep -H "^title:" docs/todo/items/*.md`. Cần danh sách để AI lấy mã tiếp theo và tránh tạo việc trùng.
- Khi cập nhật việc có sẵn: nội dung file của các việc đó.
- Nội dung nguồn: ghi chú họp, đoạn tài liệu, kết quả `PRM-007`, hoặc danh sách merge request.
- Tên người làm và hạn, nếu đã biết.

## 4. Prompt

```text
Hãy tách các việc cần làm từ nội dung bên dưới, theo quy tắc chung (PRM-000) và quy ước trong todo/README.md.

Quy ước:
- Mỗi việc một file docs/todo/items/TSK-<NNN>-<short-name>.md theo templates/TPL-TSK-task.md, kể cả việc nhỏ. Mục không có nội dung thì ghi "Chưa có.".
- Mã việc: TSK-<NNN>, đánh số tiếp theo mã lớn nhất trong danh sách việc hiện có. Không dùng lại mã đã có, kể cả việc Cancelled.
- Tên việc bắt đầu bằng động từ, đặt trong ngoặc kép ở `title`. Việc đủ nhỏ để một người làm xong và kiểm tra được. Việc quá lớn thì tách thành nhiều TSK, ghi quan hệ ở `depends_on`.
- type: Doc | Feature | Research | Infra | Bug | Chore.
- priority: Must | Should | Could. Không đủ thông tin để xếp thì ghi Should và thêm "[CẦN XÁC NHẬN: ưu tiên]" vào mục 6.
- status mặc định: Todo.
- related: mã tài liệu có trong nội dung (PAY-001, AIP-026, TEC-003, ADR-0007...). Không tự bịa mã.
- assignee và due: chỉ ghi khi nội dung nêu rõ. Không đoán.
- Mục "Tiêu chí hoàn thành" phải kiểm tra được (tài liệu nào Approved, API nào chạy, chỉ số nào đạt).

Cách làm:
1. Đọc nội dung nguồn, liệt kê mọi việc cần làm.
2. So với danh sách việc hiện có. Việc đã có thì không tạo mới, chỉ đề xuất sửa file của việc đó.
3. Với việc mới, viết đầy đủ file theo template.

Định dạng kết quả:
- Phần A: nội dung từng file mới, mỗi file ghi rõ tên file.
- Phần B: việc có sẵn cần sửa, ghi rõ mã, trường hoặc mục nào đổi, giá trị cũ và mới.
- Phần C: các điểm chưa rõ, dạng [CẦN XÁC NHẬN: câu hỏi cụ thể].

Danh sách việc hiện có:
<DÁN KẾT QUẢ LỆNH GREP>

Nội dung nguồn:
<DÁN GHI CHÚ HỌP / ĐOẠN TÀI LIỆU / KẾT QUẢ PRM-007>

Người làm và hạn đã biết (nếu có):
<...>
```

## 5. Kết quả mong đợi

Nội dung file cho từng việc mới, lưu được ngay vào `todo/items/`, danh sách sửa cho việc có sẵn, và danh sách điểm cần xác nhận. Người dùng tự đọc lại, sửa, rồi mở merge request.

## 6. Ví dụ

> Ví dụ: kết quả `PRM-007` cho `TEC-003` ghi `PAY-001: phải sửa mục 4.1` và `AUT-003: cần xác nhận`. Mã lớn nhất hiện có là `TSK-033`. Phần A của kết quả có hai file:
>
> - `TSK-034-fix-pay-001-table-name.md`: "Sửa tên bảng ở mục 4.1 tài liệu kỹ thuật `PAY-001` theo `TEC-003-R02`".
> - `TSK-035-check-aut-003-naming.md`: "Xác nhận `AUT-003` có dùng quy tắc `TEC-003-R02` không".
>
> Trong đó `TSK-034` có `priority: Must`, `related: [PAY-001, TEC-003]`; `TSK-035` với `priority: Should` và mục 6 ghi `[CẦN XÁC NHẬN: người phụ trách AUT-003]`.
>
> Dòng lịch sử của `TEC-003` ghi: `PAY-001: cần sửa, xem TSK-034; AUT-003: cần xác nhận, xem TSK-035`.

## 7. Lịch sử thay đổi

| Ngày | Người sửa | Nội dung |
|---|---|---|
| 2026-09-28 | <Tên> | Tạo mới |
