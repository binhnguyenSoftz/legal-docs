---
id: AIP-009
title: Suy ra quan hệ hộ
group: AIG-04
kind: problem            # problem | method | concern | enabler
status: Draft            # Draft | Review | Approved | Deprecated
stage: Defined           # Defined | Exploring | Decided | In production
priority: Should         # Must | Should | Could
early_test: false        # true: nằm trong nhóm khó nhất, thử nghiệm sớm
owner: <Tên người phụ trách>
updated: 2026-09-29
---

# AIP-009 - Suy ra quan hệ hộ

## 1. Định nghĩa

### 1.1. Phát biểu bài toán

Từ nhiều giấy tờ, suy ra ai thuộc hộ nào, ai là chủ hộ, và quan hệ giữa các thành viên (vợ, chồng, con, cha mẹ). Quan hệ dùng để xác định người thừa kế, người đồng sở hữu. Mỗi quan hệ phải chỉ ra giấy tờ làm nguồn.

**Ví dụ:** sổ hộ khẩu ghi ông An là chủ hộ, bà Hương là "vợ", anh Bình là "con". Giấy chứng tử cho biết ông An đã mất năm 2019. Kết quả: hộ gồm bà Hương và anh Bình, là người thừa kế hàng thứ nhất của ông An, nguồn là sổ hộ khẩu trang 2 và giấy chứng tử.

**Phạm vi:**

- Gồm: suy ra thành viên hộ, chủ hộ, quan hệ gia đình từ giấy tờ.
- Không gồm: xác định hàng thừa kế theo luật (AIP-019).

### 1.2. Vị trí trong luồng

**Bước:** Chuẩn hóa, khớp thực thể (nhóm [AIG-04](AIG-04-entity-resolution.md) - Khớp thực thể và suy ra quan hệ). Sơ đồ luồng xem [README](README.md).

- Dựa vào: [AIP-007](AIP-007-person-matching.md) - Khớp cùng một người qua nhiều giấy tờ; [AIP-008](AIP-008-address-normalization.md) - Chuẩn hóa địa chỉ hành chính Việt Nam
- Được dùng bởi: không có.

### 1.3. Đầu vào và đầu ra

| | Nội dung | Ví dụ |
|---|---|---|
| Đầu vào | Danh tính đã khớp (AIP-007), địa chỉ đã chuẩn hóa (AIP-008) | - |
| Đầu ra | Danh sách hộ, chủ hộ, thành viên và nguồn của từng quan hệ | - |

### 1.4. Ràng buộc bắt buộc

Chưa có. Bổ sung khi đi sâu vào bài toán, đánh mã `AIP-009-R01`, `R02`...

## 2. Vì sao khó

### 2.1. Thách thức

- Thông tin quan hệ nằm rải rác ở nhiều giấy tờ và có thể lệch nhau.

### 2.2. Chi phí khi sai

Sai quan hệ hộ ảnh hưởng trực tiếp tới điều kiện áp dụng của thủ tục.

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
| `AIP-007` | [Khớp cùng một người qua nhiều giấy tờ](AIP-007-person-matching.md) | Dựa vào | Dùng danh tính đã khớp |
| `AIP-008` | [Chuẩn hóa địa chỉ hành chính Việt Nam](AIP-008-address-normalization.md) | Dựa vào | Dùng địa chỉ đã chuẩn hóa |

## 7. Lịch sử thay đổi

| Ngày | Người sửa | Nội dung | Đã rà tham chiếu |
|---|---|---|---|
| 2026-09-28 | <Tên> | Tạo mới, định nghĩa ban đầu từ danh sách bài toán AI của luồng | Không cần |
| 2026-09-29 | binhnguyenSoftz | Tổ chức lại: đổi mã từ AIP-015 cũ; nhóm `AIG-04`, thêm `kind`; viết lại phát biểu bài toán | Có |
