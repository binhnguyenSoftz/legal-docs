---
id: AIP-030
title: Bias và fairness
group: AIG-10
kind: concern            # problem | method | concern | enabler
status: Draft            # Draft | Review | Approved | Deprecated
stage: Defined           # Defined | Exploring | Decided | In production
priority: Should         # Must | Should | Could
early_test: false        # true: nằm trong nhóm khó nhất, thử nghiệm sớm
owner: <Tên người phụ trách>
updated: 2026-09-29
---

# AIP-030 - Bias và fairness

## 1. Định nghĩa

### 1.1. Phát biểu bài toán

Kiểm tra hệ thống có kém hơn với một nhóm người (người cao tuổi viết tay, dân tộc thiểu số có tên đặc thù, vùng có mẫu giấy tờ cũ) khiến nhóm đó bị chuyển người hoặc từ chối oan nhiều hơn.

**Ví dụ:** CER của OCR trên tên người dân tộc thiểu số cao gấp 3 lần trung bình, làm tỉ lệ "mâu thuẫn họ tên" của nhóm này cao hơn hẳn. Báo cáo fairness chỉ ra chênh lệch và tầng gây ra.

**Phạm vi:**

- Gồm: chia nhóm; đo chênh lệch chất lượng từng tầng và tỉ lệ từ chối.
- Không gồm: sửa model cho từng nhóm (thuộc các bài toán tầng tương ứng).

### 1.2. Vị trí trong luồng

**Bước:** Xuyên suốt: an toàn, bảo mật (nhóm [AIG-10](AIG-10-safety-security.md) - An toàn và bảo mật AI). Sơ đồ luồng xem [README](README.md).

- Dựa vào: [AIP-001](AIP-001-document-ocr.md) - Đọc bố cục và chữ tiếng Việt trên giấy tờ; [AIP-020](AIP-020-three-way-decision-abstention.md) - Quyết định ba lớp, abstention và ngưỡng theo chi phí lỗi
- Được dùng bởi: không có.

### 1.3. Đầu vào và đầu ra

| | Nội dung | Ví dụ |
|---|---|---|
| Đầu vào | Kết quả theo nhóm người | - |
| Đầu ra | Chênh lệch chất lượng và tỉ lệ từ chối giữa các nhóm | - |

### 1.4. Ràng buộc bắt buộc

Chưa có. Bổ sung khi đi sâu vào bài toán, đánh mã `AIP-030-R01`, `R02`...

## 2. Vì sao khó

### 2.1. Thách thức

- OCR/model có thể kém hơn với nét chữ người lớn tuổi, vùng miền, dân tộc thiểu số.
- Thu thập thông tin nhóm để đo có thể đụng tới dữ liệu nhạy cảm.

### 2.2. Chi phí khi sai

Một nhóm người bị từ chối oan có hệ thống.

## 3. Đánh giá

| Chỉ số | Cách đo | Ngưỡng chấp nhận |
|---|---|---|
| Chênh lệch CER và tỉ lệ từ chối giữa các nhóm | `[CẦN XÁC NHẬN]` | `[CẦN XÁC NHẬN]` |

## 4. Hướng tiếp cận và thử nghiệm

### 4.1. Hướng tiếp cận ứng viên

| Hướng | Ưu điểm | Nhược điểm |
|---|---|---|
| `[CẦN XÁC NHẬN]` Chưa khảo sát thêm | | |

### 4.2. Dữ liệu cần chuẩn bị

- Mẫu đại diện cho các nhóm cần đo.

### 4.3. Nhật ký thử nghiệm

| Ngày | Thử nghiệm | Kết quả | Kết luận |
|---|---|---|---|
| | | | |

## 5. Câu hỏi còn mở

- [ ] Được phép dùng thông tin nào để chia nhóm khi đo?

## 6. Tài liệu tham chiếu

Quy tắc ghi: `standards/07-references.md`.

| Mã | Tài liệu | Chiều | Nội dung liên quan |
|---|---|---|---|
| `AIP-001` | [Đọc bố cục và chữ tiếng Việt trên giấy tờ](AIP-001-document-ocr.md) | Dựa vào | Đo chênh lệch chất lượng OCR theo nhóm người |
| `AIP-020` | [Quyết định ba lớp, abstention và ngưỡng theo chi phí lỗi](AIP-020-three-way-decision-abstention.md) | Dựa vào | Đo tỉ lệ từ chối theo nhóm |

## 7. Lịch sử thay đổi

| Ngày | Người sửa | Nội dung | Đã rà tham chiếu |
|---|---|---|---|
| 2026-09-28 | <Tên> | Tạo mới, định nghĩa ban đầu từ danh sách bài toán AI của luồng | Không cần |
| 2026-09-29 | binhnguyenSoftz | Tổ chức lại: đổi mã từ AIP-040 cũ; nhóm `AIG-10`, thêm `kind`; viết lại phát biểu bài toán | Có |
