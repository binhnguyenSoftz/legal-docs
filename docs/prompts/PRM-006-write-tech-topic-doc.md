---
id: PRM-006
title: Viết tài liệu kỹ thuật chung
status: Approved
updated: <YYYY-MM-DD>
---

# PRM-006 - Viết tài liệu kỹ thuật chung

## 1. Mục đích

Tạo tài liệu `TEC` trong `techs/` cho một chủ đề kỹ thuật dùng chung: kiến trúc, hạ tầng, quy ước dữ liệu, bảo mật, tích hợp, hướng dẫn cho dev.

## 2. Khi nào dùng

Nội dung dùng cho từ 2 tính năng trở lên hoặc cho cả hệ thống (xem `standards/06-tech-docs.md` mục 1). Nếu nội dung chỉ đúng cho một tính năng, dùng PRM-002.

## 3. Đầu vào cần chuẩn bị

- Mã `TEC` đã cấp trong `techs/README.md`, tên chủ đề và nhóm (`architecture`, `infrastructure`...).
- Nguồn thông tin: code, file cấu hình, script triển khai, ghi chú họp, ADR liên quan. Dán đúng đoạn cần.
- Danh sách tính năng hoặc tài liệu đang dùng chủ đề này (nếu biết).
- Template `TPL-TEC-topic.md`.

## 4. Prompt

```text
Hãy viết tài liệu kỹ thuật chung TEC-<NNN> - <TÊN CHỦ ĐỀ> thuộc nhóm <NHÓM>, theo template đính kèm. Tuân thủ quy tắc chung (PRM-000).

Cách làm:
1. Viết "Phạm vi áp dụng": áp dụng cho service, repo, môi trường nào và không áp dụng cho đâu.
2. Viết "Bối cảnh" 3-5 câu: vấn đề gì dẫn tới tài liệu này. Có ADR liên quan thì trỏ liên kết.
3. Nếu có từ 2 thành phần trở lên, vẽ flowchart tổng quan và diễn giải từng thành phần.
4. Rút ra các quy tắc bắt buộc, đánh mã TEC-<NNN>-R01, R02... Mỗi quy tắc có lý do.
5. Viết hướng dẫn thực hiện: các bước đánh số, lệnh cụ thể chạy được, kết quả mong đợi.
6. Liệt kê cấu hình và bảng xử lý sự cố (dấu hiệu, nguyên nhân, cách xử lý).
7. Viết mục "Tài liệu tham chiếu": tài liệu nguồn ở chiều "Dựa vào", tính năng đang dùng ở chiều "Được dùng bởi". Cột "Nội dung liên quan" nói rõ mã quy tắc nào được dùng.

Yêu cầu bổ sung:
- Chỉ viết kỹ thuật. Không viết quy tắc nghiệp vụ.
- Chỉ dùng thông tin có trong đầu vào. Thiếu thì ghi `[CẦN XÁC NHẬN]`.
- Không viết chi tiết riêng của một tính năng. Nếu đầu vào có phần đó, liệt kê riêng ở cuối và đề xuất chuyển sang tài liệu tính năng.
- Cuối cùng, liệt kê các tài liệu cần thêm dòng "Dựa vào TEC-<NNN>" trong mục tham chiếu của chúng.

Nguồn thông tin:
<DÁN CODE, CẤU HÌNH, GHI CHÚ>

Tài liệu đang dùng chủ đề này (nếu biết):
<DANH SÁCH HOẶC GHI "chưa biết">

Template:
<DÁN TPL-TEC-topic.md>
```

## 5. Kết quả mong đợi

- File `TEC-<NNN>-<short-name>.md` đủ mục theo template.
- Quy tắc có mã, có lý do, tài liệu khác trỏ tới được.
- Danh sách tài liệu cần bổ sung tham chiếu ngược.

## 6. Cách kiểm tra kết quả

1. Chạy thử các lệnh trong "Hướng dẫn thực hiện".
2. Đối chiếu tên cấu hình, service, bảng với code.
3. Thêm dòng "Dựa vào TEC-<NNN>" vào các tài liệu đã liệt kê, trong cùng merge request.

## 7. Lịch sử thay đổi

| Ngày | Người sửa | Nội dung |
|---|---|---|
| <YYYY-MM-DD> | <Tên> | Tạo mới |
