---
id: AIP-026
title: Golden set và metric theo từng tầng
group: AIG-09
kind: enabler            # problem | method | concern | enabler
status: Draft            # Draft | Review | Approved | Deprecated
stage: Defined           # Defined | Exploring | Decided | In production
priority: Must           # Must | Should | Could
early_test: false        # true: nằm trong nhóm khó nhất, thử nghiệm sớm
owner: <Tên người phụ trách>
updated: 2026-09-29
---

# AIP-026 - Golden set và metric theo từng tầng

## 1. Định nghĩa

### 1.1. Phát biểu bài toán

Xây bộ hồ sơ mẫu có nhãn đúng ở từng tầng (chữ OCR, loại giấy, giá trị trường, người trùng khớp, mâu thuẫn, điều khoản, quyết định) và bảng chỉ số đo cho từng tầng. Mọi bài toán khác dùng bộ này để chốt ngưỡng và nghiệm thu.

**Ví dụ:** một hồ sơ thừa kế trong golden set gồm 7 giấy tờ. Nhãn gồm: text đúng từng vùng, loại từng giấy, giá trị từng trường, "bà Hương trên CCCD và trên sổ hộ khẩu là một người", mâu thuẫn cài sẵn về ngày sinh, điều khoản áp dụng và quyết định của chuyên viên. Bộ sinh dữ liệu giả ở `src/data-golden-set-generator` sinh sẵn các nhãn này.

**Phạm vi:**

- Gồm: nhãn theo tầng; bảng metric theo tầng; bộ sinh hồ sơ giả có ground truth.
- Không gồm: đo toàn luồng (AIP-027), regression (AIP-028).

### 1.2. Vị trí trong luồng

**Bước:** Xuyên suốt: đánh giá (nhóm [AIG-09](AIG-09-evaluation-qa.md) - Đánh giá và bảo đảm chất lượng AI). Sơ đồ luồng xem [README](README.md).

- Dựa vào: không có.
- Được dùng bởi: [AIP-018](AIP-018-retrieval-evaluation.md) - Đánh giá retrieval; [AIP-027](AIP-027-end-to-end-evaluation.md) - Đánh giá end-to-end và chấm văn bản sinh ra; [AIP-028](AIP-028-regression-testing.md) - Regression test khi đổi model, prompt hoặc luật; [AIP-032](AIP-032-reviewer-feedback-learning.md) - Học từ chỉnh sửa của cán bộ duyệt

### 1.3. Đầu vào và đầu ra

| | Nội dung | Ví dụ |
|---|---|---|
| Đầu vào | Hồ sơ mẫu đã được chuyên viên gán nhãn | - |
| Đầu ra | Golden set và bảng metric theo tầng | - |

### 1.4. Ràng buộc bắt buộc

Chưa có. Bổ sung khi đi sâu vào bài toán, đánh mã `AIP-026-R01`, `R02`...

## 2. Vì sao khó

### 2.1. Thách thức

- Gán nhãn nhiều tầng tốn công chuyên viên.
- Dữ liệu cá nhân trong hồ sơ mẫu.

### 2.2. Chi phí khi sai

Không có golden set thì không đo được bài toán nào, kể cả ba bài toán ưu tiên.

## 3. Đánh giá

| Chỉ số | Cách đo | Ngưỡng chấp nhận |
|---|---|---|
| CER/WER | Tầng OCR | `[CẦN XÁC NHẬN]` |
| Field-level accuracy / F1 | Tầng trích xuất | `[CẦN XÁC NHẬN]` |
| recall@k | Tầng truy xuất | `[CẦN XÁC NHẬN]` |
| Độ khớp quyết định với chuyên viên | Tầng suy luận | `[CẦN XÁC NHẬN]` |

## 4. Hướng tiếp cận và thử nghiệm

### 4.1. Hướng tiếp cận ứng viên

| Hướng | Ưu điểm | Nhược điểm |
|---|---|---|
| `[CẦN XÁC NHẬN]` Chưa khảo sát thêm | | |

### 4.2. Dữ liệu cần chuẩn bị

- Hồ sơ mẫu đại diện cho các loại giấy tờ và thủ tục.

### 4.3. Nhật ký thử nghiệm

| Ngày | Thử nghiệm | Kết quả | Kết luận |
|---|---|---|---|
| | | | |

## 5. Câu hỏi còn mở

- [ ] Ai gán nhãn và mất bao lâu?

## 6. Tài liệu tham chiếu

Quy tắc ghi: `standards/07-references.md`.

| Mã | Tài liệu | Chiều | Nội dung liên quan |
|---|---|---|---|
| `AIP-018` | [Đánh giá retrieval](AIP-018-retrieval-evaluation.md) | Được dùng bởi | Bộ câu hỏi nằm trong golden set |
| `AIP-027` | [Đánh giá end-to-end và chấm văn bản sinh ra](AIP-027-end-to-end-evaluation.md) | Được dùng bởi | Chạy đánh giá trên golden set |
| `AIP-028` | [Regression test khi đổi model, prompt hoặc luật](AIP-028-regression-testing.md) | Được dùng bởi | Chạy lại golden set khi đổi model, prompt, luật |
| `AIP-032` | [Học từ chỉnh sửa của cán bộ duyệt](AIP-032-reviewer-feedback-learning.md) | Được dùng bởi | Bổ sung chỉnh sửa của cán bộ vào golden set |

## 7. Lịch sử thay đổi

| Ngày | Người sửa | Nội dung | Đã rà tham chiếu |
|---|---|---|---|
| 2026-09-28 | <Tên> | Tạo mới, định nghĩa ban đầu từ danh sách bài toán AI của luồng | Không cần |
| 2026-09-29 | binhnguyenSoftz | Tổ chức lại: đổi mã từ AIP-036 cũ; nhóm `AIG-09`, thêm `kind`; viết lại phát biểu bài toán | Có |
