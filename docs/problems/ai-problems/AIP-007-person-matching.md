---
id: AIP-007
title: Khớp cùng một người qua nhiều giấy tờ
group: AIG-04
kind: problem            # problem | method | concern | enabler
status: Draft            # Draft | Review | Approved | Deprecated
stage: Defined           # Defined | Exploring | Decided | In production
priority: Must           # Must | Should | Could
early_test: false        # true: nằm trong nhóm khó nhất, thử nghiệm sớm
owner: <Tên người phụ trách>
updated: 2026-09-29
---

# AIP-007 - Khớp cùng một người qua nhiều giấy tờ

## 1. Định nghĩa

### 1.1. Phát biểu bài toán

Xác định các bản ghi người trên nhiều giấy tờ có phải cùng một người không, dù họ tên viết khác (có dấu/không dấu, viết tắt), số giấy tờ khác thế hệ (CMND 9 số, CCCD 12 số) hoặc thiếu ngày sinh.

**Ví dụ:** tờ khai ghi `Nguyễn Thị Hương, 1985`, CCCD ghi `NGUYỄN THỊ HƯƠNG, 12/03/1985, 0791850xxxxx`, sổ hộ khẩu cũ ghi `Ng. T. Hương`, CMND 9 số. Kết quả: ba bản ghi là cùng một người, điểm 0,93, căn cứ họ tên và năm sinh.

**Phạm vi:**

- Gồm: khớp người qua họ tên, ngày sinh, số giấy tờ, quan hệ ghi trên giấy.
- Không gồm: chuẩn hóa địa chỉ (AIP-008), suy ra quan hệ hộ (AIP-009).

### 1.2. Vị trí trong luồng

**Bước:** Chuẩn hóa, khớp thực thể (nhóm [AIG-04](AIG-04-entity-resolution.md) - Khớp thực thể và suy ra quan hệ). Sơ đồ luồng xem [README](README.md).

- Dựa vào: [AIP-005](AIP-005-schema-extraction.md) - Trích xuất theo schema và sửa lỗi OCR
- Được dùng bởi: [AIP-009](AIP-009-household-inference.md) - Suy ra quan hệ hộ; [AIP-010](AIP-010-conflict-vs-error.md) - Phân biệt mâu thuẫn thật với lỗi OCR/trích xuất

### 1.3. Đầu vào và đầu ra

| | Nội dung | Ví dụ |
|---|---|---|
| Đầu vào | Họ tên, ngày sinh, số giấy tờ đã trích xuất (AIP-005) | `Nguyễn Thị Hương` và `Nguyen Thi Huong` |
| Đầu ra | Nhóm bản ghi cùng một người, kèm điểm tin cậy | - |

### 1.4. Ràng buộc bắt buộc

Chưa có. Bổ sung khi đi sâu vào bài toán, đánh mã `AIP-007-R01`, `R02`...

## 2. Vì sao khó

### 2.1. Thách thức

- Họ tên viết khác nhau, có hoặc không dấu, sai chính tả.
- Hai người khác nhau có thể trùng tên.

### 2.2. Chi phí khi sai

Gộp nhầm hai người thành một, hoặc tách một người thành hai, đều làm sai kết quả đối chiếu.

## 3. Đánh giá

| Chỉ số | Cách đo | Ngưỡng chấp nhận |
|---|---|---|
| Precision / recall khi khớp | `[CẦN XÁC NHẬN]` | `[CẦN XÁC NHẬN]` |

## 4. Hướng tiếp cận và thử nghiệm

### 4.1. Hướng tiếp cận ứng viên

| Hướng | Ưu điểm | Nhược điểm |
|---|---|---|
| `[CẦN XÁC NHẬN]` Chưa khảo sát thêm | | |

### 4.2. Dữ liệu cần chuẩn bị

- Cặp bản ghi có nhãn cùng người / khác người.

### 4.3. Nhật ký thử nghiệm

| Ngày | Thử nghiệm | Kết quả | Kết luận |
|---|---|---|---|
| | | | |

## 5. Câu hỏi còn mở

Chưa có.

## 6. Tài liệu tham chiếu

Quy tắc ghi: `standards/07-references.md`.

| Mã | Tài liệu | Chiều | Nội dung liên quan |
|---|---|---|---|
| `AIP-005` | [Trích xuất theo schema và sửa lỗi OCR](AIP-005-schema-extraction.md) | Dựa vào | Dùng họ tên, ngày sinh, số giấy tờ đã trích xuất |
| `AIP-009` | [Suy ra quan hệ hộ](AIP-009-household-inference.md) | Được dùng bởi | Dùng danh tính đã khớp |
| `AIP-010` | [Phân biệt mâu thuẫn thật với lỗi OCR/trích xuất](AIP-010-conflict-vs-error.md) | Được dùng bởi | So sánh dữ liệu của cùng một người |

## 7. Lịch sử thay đổi

| Ngày | Người sửa | Nội dung | Đã rà tham chiếu |
|---|---|---|---|
| 2026-09-28 | <Tên> | Tạo mới, định nghĩa ban đầu từ danh sách bài toán AI của luồng | Không cần |
| 2026-09-29 | binhnguyenSoftz | Tổ chức lại: đổi mã từ AIP-013 cũ; nhóm `AIG-04`, thêm `kind`; viết lại phát biểu bài toán | Có |
