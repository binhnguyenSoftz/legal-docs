---
id: AIP-028
title: Regression test khi đổi model, prompt hoặc luật
group: AIG-09
kind: enabler            # problem | method | concern | enabler
status: Draft            # Draft | Review | Approved | Deprecated
stage: Defined           # Defined | Exploring | Decided | In production
priority: Should         # Must | Should | Could
early_test: false        # true: nằm trong nhóm khó nhất, thử nghiệm sớm
owner: <Tên người phụ trách>
updated: 2026-09-29
---

# AIP-028 - Regression test khi đổi model, prompt hoặc luật

## 1. Định nghĩa

### 1.1. Phát biểu bài toán

Mỗi lần đổi model, prompt, cấu hình retrieval hoặc khi luật thay đổi, tự động chạy lại golden set và so với phiên bản trước theo từng tầng. Chỉ số nào giảm quá ngưỡng thì chặn thay đổi.

**Ví dụ:** đổi prompt trích xuất làm F1 trường `ngay_sinh` tăng 2% nhưng F1 trường `so_thua` giảm 6%. Báo cáo regression chỉ ra đúng trường giảm và các hồ sơ bị ảnh hưởng; thay đổi bị chặn cho tới khi xử lý.

**Phạm vi:**

- Gồm: chạy lại golden set; so theo tầng; chặn khi giảm quá ngưỡng.
- Không gồm: phát hiện thay đổi ở dữ liệu thật khi chạy (AIP-036).

### 1.2. Vị trí trong luồng

**Bước:** Xuyên suốt: đánh giá (nhóm [AIG-09](AIG-09-evaluation-qa.md) - Đánh giá và bảo đảm chất lượng AI). Sơ đồ luồng xem [README](README.md).

- Dựa vào: [AIP-026](AIP-026-layered-golden-set.md) - Golden set và metric theo từng tầng
- Được dùng bởi: không có.

### 1.3. Đầu vào và đầu ra

| | Nội dung | Ví dụ |
|---|---|---|
| Đầu vào | Golden set (AIP-026), phiên bản mới | - |
| Đầu ra | Báo cáo so sánh với phiên bản trước | - |

### 1.4. Ràng buộc bắt buộc

Chưa có. Bổ sung khi đi sâu vào bài toán, đánh mã `AIP-028-R01`, `R02`...

## 2. Vì sao khó

### 2.1. Thách thức

- Luật thay đổi làm nhãn cũ trong golden set không còn đúng.

### 2.2. Chi phí khi sai

Lỗi mới lọt vào hệ thống đang chạy.

## 3. Đánh giá

| Chỉ số | Cách đo | Ngưỡng chấp nhận |
|---|---|---|
| `[CẦN XÁC NHẬN]` | `[CẦN XÁC NHẬN]` | `[CẦN XÁC NHẬN]` |

## 4. Hướng tiếp cận và thử nghiệm

### 4.1. Hướng tiếp cận ứng viên

| Hướng | Ưu điểm | Nhược điểm |
|---|---|---|
| `[CẦN XÁC NHẬN]` Chưa khảo sát thêm | | |

### 4.2. Dữ liệu cần chuẩn bị

- `[CẦN XÁC NHẬN]`

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
| `AIP-026` | [Golden set và metric theo từng tầng](AIP-026-layered-golden-set.md) | Dựa vào | Chạy lại golden set khi đổi model, prompt, luật |

## 7. Lịch sử thay đổi

| Ngày | Người sửa | Nội dung | Đã rà tham chiếu |
|---|---|---|---|
| 2026-09-28 | <Tên> | Tạo mới, định nghĩa ban đầu từ danh sách bài toán AI của luồng | Không cần |
| 2026-09-29 | binhnguyenSoftz | Tổ chức lại: đổi mã từ AIP-039 cũ; nhóm `AIG-09`, thêm `kind`; viết lại phát biểu bài toán | Có |
