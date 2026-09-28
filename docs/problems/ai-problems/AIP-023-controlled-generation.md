---
id: AIP-023
title: Sinh văn bản kết quả có kiểm soát
group: AIG-08
kind: problem            # problem | method | concern | enabler
status: Draft            # Draft | Review | Approved | Deprecated
stage: Defined           # Defined | Exploring | Decided | In production
priority: Must           # Must | Should | Could
early_test: false        # true: nằm trong nhóm khó nhất, thử nghiệm sớm
owner: <Tên người phụ trách>
updated: 2026-09-29
---

# AIP-023 - Sinh văn bản kết quả có kiểm soát

## 1. Định nghĩa

### 1.1. Phát biểu bài toán

Sinh văn bản kết quả gửi người dân (thông báo chấp thuận, văn bản từ chối, yêu cầu bổ sung) từ template cố định theo từng loại quyết định. LLM chỉ viết phần biến thiên, chủ yếu là lý do và danh sách việc người dân cần làm. Văn bản phải đúng văn phong hành chính, lý do từ chối phải cụ thể và nêu đúng căn cứ.

**Ví dụ:** quyết định "cần bổ sung" vì thiếu giấy chứng tử. Template cố định phần quốc hiệu, tiêu đề, người ký. LLM viết: "Hồ sơ còn thiếu bản sao Giấy chứng tử của ông Nguyễn Văn An, theo quy định tại điểm ... khoản ... Điều ... . Đề nghị ông/bà bổ sung trong thời hạn ... ngày."

**Phạm vi:**

- Gồm: chọn template; sinh phần biến thiên; chuẩn văn phong hành chính; lý do từ chối cụ thể.
- Không gồm: kiểm tra trích dẫn có thật và đúng (AIP-024), kiểm chứng dữ kiện sau sinh (AIP-025), chấm chất lượng văn bản (AIP-027).

### 1.2. Vị trí trong luồng

**Bước:** Sinh văn bản (nhóm [AIG-08](AIG-08-legal-generation.md) - Sinh và kiểm chứng văn bản kết quả). Sơ đồ luồng xem [README](README.md).

- Dựa vào: [AIP-020](AIP-020-three-way-decision-abstention.md) - Quyết định ba lớp, abstention và ngưỡng theo chi phí lỗi
- Được dùng bởi: [AIP-024](AIP-024-citation-grounding.md) - Grounding trích dẫn pháp lý; [AIP-025](AIP-025-post-generation-verification.md) - Kiểm chứng sau sinh; [AIP-027](AIP-027-end-to-end-evaluation.md) - Đánh giá end-to-end và chấm văn bản sinh ra

### 1.3. Đầu vào và đầu ra

| | Nội dung | Ví dụ |
|---|---|---|
| Đầu vào | Quyết định (AIP-020), dữ liệu đã duyệt, căn cứ pháp lý, template | Quyết định "cần bổ sung", thiếu giấy chứng tử |
| Đầu ra | Văn bản hoàn chỉnh theo mẫu, đúng văn phong | Thông báo yêu cầu bổ sung hồ sơ |

### 1.4. Ràng buộc bắt buộc

| Mã | Ràng buộc | Lý do |
|---|---|---|
| AIP-023-R01 | Dùng template cố định. LLM chỉ điền phần biến thiên. | Giảm rủi ro sinh nội dung sai. |
| AIP-023-R02 | Lý do từ chối phải cụ thể và nêu đúng căn cứ. (Trước đây là `AIP-035-R01` cũ.) | Người dân biết cần sửa gì. |

### 1.5. Bài toán con

| Bài toán con | Mã cũ | Ưu tiên | Nội dung |
|---|---|---|---|
| Sinh văn bản có kiểm soát | AIP-032 cũ | Must | Template cố định, LLM chỉ điền phần biến thiên |
| Văn phong hành chính và lý do từ chối | AIP-035 cũ | Should | Văn phong chuẩn, lý do cụ thể, đúng căn cứ |

## 2. Vì sao khó

### 2.1. Thách thức

- Giới hạn phần LLM được viết mà văn bản vẫn tự nhiên.
- Lý do chung chung không giúp người dân biết phải làm gì.

### 2.2. Chi phí khi sai

- Văn bản sai gửi tới người dân có giá trị pháp lý.
- Lý do mơ hồ gây khiếu nại và nộp lại nhiều lần.

## 3. Đánh giá

| Chỉ số | Cách đo | Ngưỡng chấp nhận |
|---|---|---|
| Tỉ lệ văn bản cán bộ phải sửa | `[CẦN XÁC NHẬN]` | `[CẦN XÁC NHẬN]` |
| Điểm văn phong | LLM-as-judge (AIP-027) kèm chuyên viên chấm mẫu | `[CẦN XÁC NHẬN]` |

## 4. Hướng tiếp cận và thử nghiệm

### 4.1. Hướng tiếp cận ứng viên

| Hướng | Ưu điểm | Nhược điểm |
|---|---|---|
| `[CẦN XÁC NHẬN]` Chưa khảo sát thêm | | |

### 4.2. Dữ liệu cần chuẩn bị

- Template văn bản theo từng loại quyết định.
- Mẫu văn bản chuẩn đã ban hành.

### 4.3. Nhật ký thử nghiệm

| Ngày | Thử nghiệm | Kết quả | Kết luận |
|---|---|---|---|
| | | | |

## 5. Câu hỏi còn mở

- [ ] Mẫu văn bản kết quả của từng thủ tục do đơn vị nào ban hành?

## 6. Tài liệu tham chiếu

Quy tắc ghi: `standards/07-references.md`.

| Mã | Tài liệu | Chiều | Nội dung liên quan |
|---|---|---|---|
| `AIP-020` | [Quyết định ba lớp, abstention và ngưỡng theo chi phí lỗi](AIP-020-three-way-decision-abstention.md) | Dựa vào | Sinh văn bản theo quyết định đã chốt |
| `AIP-024` | [Grounding trích dẫn pháp lý](AIP-024-citation-grounding.md) | Được dùng bởi | Trích dẫn nằm trong văn bản sinh ra |
| `AIP-025` | [Kiểm chứng sau sinh](AIP-025-post-generation-verification.md) | Được dùng bởi | Kiểm chứng dữ kiện trong văn bản |
| `AIP-027` | [Đánh giá end-to-end và chấm văn bản sinh ra](AIP-027-end-to-end-evaluation.md) | Được dùng bởi | Chấm văn bản sinh ra bằng LLM-as-judge |

## 7. Lịch sử thay đổi

| Ngày | Người sửa | Nội dung | Đã rà tham chiếu |
|---|---|---|---|
| 2026-09-28 | <Tên> | Tạo mới, định nghĩa ban đầu từ danh sách bài toán AI của luồng | Không cần |
| 2026-09-29 | binhnguyenSoftz | Tổ chức lại: gộp AIP-032 cũ (sinh có kiểm soát) và AIP-035 cũ (văn phong hành chính), `AIP-035-R01` cũ thành `AIP-023-R02`; nhóm `AIG-08`; viết lại phát biểu bài toán | Có |
