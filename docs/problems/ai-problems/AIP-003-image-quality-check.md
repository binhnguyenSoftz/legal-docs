---
id: AIP-003
title: Đánh giá chất lượng ảnh
group: AIG-01
kind: problem            # problem | method | concern | enabler
status: Draft            # Draft | Review | Approved | Deprecated
stage: Defined           # Defined | Exploring | Decided | In production
priority: Should         # Must | Should | Could
early_test: false        # true: nằm trong nhóm khó nhất, thử nghiệm sớm
owner: <Tên người phụ trách>
updated: 2026-09-29
---

# AIP-003 - Đánh giá chất lượng ảnh

## 1. Định nghĩa

### 1.1. Phát biểu bài toán

Kiểm tra ảnh người dân nộp ngay khi nhận: mờ, lóa, nghiêng, thiếu góc, độ phân giải thấp, chụp màn hình. Ảnh không đủ để đọc thì yêu cầu chụp lại ngay, kèm lý do cụ thể, thay vì để lỗi đi xuống các bước sau.

**Ví dụ:** ảnh CCCD mặt trước bị lóa đèn đúng vùng số CCCD. Hệ thống trả `{ok: false, reason: "glare", region: "id_number"}` và nhắn người dân "Ảnh bị lóa ở vùng số CCCD, vui lòng chụp lại tránh đèn".

**Phạm vi:**

- Gồm: phát hiện lỗi chụp, lỗi scan; lý do cụ thể để người dân sửa.
- Không gồm: đọc chữ (AIP-001).

### 1.2. Vị trí trong luồng

**Bước:** Đọc ảnh (nhóm [AIG-01](AIG-01-document-vision-ocr.md) - Đọc ảnh và OCR). Sơ đồ luồng xem [README](README.md).

- Dựa vào: không có.
- Được dùng bởi: [AIP-001](AIP-001-document-ocr.md) - Đọc bố cục và chữ tiếng Việt trên giấy tờ; [AIP-036](AIP-036-drift-detection.md) - Drift detection

### 1.3. Đầu vào và đầu ra

| | Nội dung | Ví dụ |
|---|---|---|
| Đầu vào | Ảnh hoặc file scan người dân nộp | Ảnh chụp CCCD bị lóa |
| Đầu ra | Đạt / không đạt kèm lý do | `{ok: false, reason: "glare"}` |

### 1.4. Ràng buộc bắt buộc

Chưa có. Bổ sung khi đi sâu vào bài toán, đánh mã `AIP-003-R01`, `R02`...

## 2. Vì sao khó

### 2.1. Thách thức

- Ảnh "trông rõ" chưa chắc OCR đọc được, nên tiêu chí phải gắn với kết quả OCR thật.

### 2.2. Chi phí khi sai

Cho qua ảnh xấu thì lỗi OCR lan xuống sau. Chặn nhầm ảnh tốt thì người dân phải chụp lại không cần thiết.

## 3. Đánh giá

| Chỉ số | Cách đo | Ngưỡng chấp nhận |
|---|---|---|
| Tỉ lệ ảnh bị chặn nhầm | `[CẦN XÁC NHẬN]` | `[CẦN XÁC NHẬN]` |
| Tỉ lệ ảnh xấu lọt qua | `[CẦN XÁC NHẬN]` | `[CẦN XÁC NHẬN]` |

## 4. Hướng tiếp cận và thử nghiệm

### 4.1. Hướng tiếp cận ứng viên

| Hướng | Ưu điểm | Nhược điểm |
|---|---|---|
| `[CẦN XÁC NHẬN]` Chưa khảo sát thêm | | |

### 4.2. Dữ liệu cần chuẩn bị

- Ảnh có nhãn đạt/không đạt, kèm kết quả OCR tương ứng.

### 4.3. Nhật ký thử nghiệm

| Ngày | Thử nghiệm | Kết quả | Kết luận |
|---|---|---|---|
| | | | |

## 5. Câu hỏi còn mở

- [ ] Yêu cầu chụp lại hiển thị ở kênh nào và ngay lúc nộp hay sau?

## 6. Tài liệu tham chiếu

Quy tắc ghi: `standards/07-references.md`.

| Mã | Tài liệu | Chiều | Nội dung liên quan |
|---|---|---|---|
| `AIP-001` | [Đọc bố cục và chữ tiếng Việt trên giấy tờ](AIP-001-document-ocr.md) | Được dùng bởi | Chỉ OCR ảnh đạt ngưỡng chất lượng |
| `AIP-036` | [Drift detection](AIP-036-drift-detection.md) | Được dùng bởi | Theo dõi chất lượng ảnh scan theo thời gian |

## 7. Lịch sử thay đổi

| Ngày | Người sửa | Nội dung | Đã rà tham chiếu |
|---|---|---|---|
| 2026-09-28 | <Tên> | Tạo mới, định nghĩa ban đầu từ danh sách bài toán AI của luồng | Không cần |
| 2026-09-29 | binhnguyenSoftz | Tổ chức lại: đổi mã từ AIP-004 cũ; nhóm `AIG-01`, thêm `kind`; viết lại phát biểu bài toán | Có |
| 2026-09-30 | binhnguyenSoftz | Bỏ bài toán phát hiện giả mạo (AIP-037, AIG-13): xóa AIP-037 khỏi phạm vi "Không gồm" | Có |
