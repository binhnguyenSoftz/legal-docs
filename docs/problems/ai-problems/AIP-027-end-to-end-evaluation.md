---
id: AIP-027
title: Đánh giá end-to-end và chấm văn bản sinh ra
group: AIG-09
kind: enabler            # problem | method | concern | enabler
status: Draft            # Draft | Review | Approved | Deprecated
stage: Defined           # Defined | Exploring | Decided | In production
priority: Must           # Must | Should | Could
early_test: false        # true: nằm trong nhóm khó nhất, thử nghiệm sớm
owner: <Tên người phụ trách>
updated: 2026-09-29
---

# AIP-027 - Đánh giá end-to-end và chấm văn bản sinh ra

## 1. Định nghĩa

### 1.1. Phát biểu bài toán

Chạy toàn luồng trên golden set (AIP-026), so quyết định cuối và văn bản kết quả với nhãn của chuyên viên, rồi truy ngược mỗi lỗi cuối về tầng gây ra nó (OCR, phân loại, trích xuất, khớp thực thể, đối chiếu, truy xuất pháp luật, suy luận, sinh văn bản). Với văn bản sinh ra, dùng LLM làm người chấm (LLM-as-judge) và đo độ tin cậy của chính người chấm đó.

**Ví dụ:** hồ sơ thừa kế bị hệ thống đề xuất "từ chối" trong khi chuyên viên "chấp thuận". Truy vết cho thấy OCR đọc năm mất `2019` thành `2018` (AIP-001), làm AIP-010 báo mâu thuẫn thật. Lỗi được quy về tầng OCR, không phải tầng quyết định.

**Phạm vi:**

- Gồm: chỉ số end-to-end; truy vết lỗi lan truyền giữa các tầng; LLM-as-judge cho văn bản sinh ra.
- Không gồm: xây golden set và metric từng tầng (AIP-026), regression khi đổi model/prompt/luật (AIP-028).

### 1.2. Vị trí trong luồng

**Bước:** Xuyên suốt: đánh giá (nhóm [AIG-09](AIG-09-evaluation-qa.md) - Đánh giá và bảo đảm chất lượng AI). Sơ đồ luồng xem [README](README.md).

- Dựa vào: [AIP-026](AIP-026-layered-golden-set.md) - Golden set và metric theo từng tầng; [AIP-023](AIP-023-controlled-generation.md) - Sinh văn bản kết quả có kiểm soát
- Được dùng bởi: không có.

### 1.3. Đầu vào và đầu ra

| | Nội dung | Ví dụ |
|---|---|---|
| Đầu vào | Golden set (AIP-026), log từng tầng, văn bản sinh ra (AIP-023), tiêu chí chấm | - |
| Đầu ra | Chỉ số end-to-end; phân tích nguyên nhân lỗi theo tầng; điểm và nhận xét cho văn bản sinh ra | `{hồ sơ: 17, lỗi cuối: "từ chối oan", tầng gây lỗi: "OCR"}` |

### 1.4. Ràng buộc bắt buộc

Chưa có. Bổ sung khi đi sâu vào bài toán, đánh mã `AIP-027-R01`, `R02`...

### 1.5. Bài toán con

| Bài toán con | Mã cũ | Ưu tiên | Nội dung |
|---|---|---|---|
| Đánh giá end-to-end và lỗi lan truyền | AIP-037 cũ | Must | Chỉ số toàn luồng, quy lỗi về tầng gây ra |
| LLM-as-judge cho văn bản sinh ra | AIP-038 cũ | Could | Chấm văn bản bằng LLM, đo độ khớp với chuyên viên |

## 2. Vì sao khó

### 2.1. Thách thức

- Lỗi tầng trước làm nhiễu đánh giá tầng sau.
- Judge có thể thiên lệch hoặc không khớp với chuyên viên.

### 2.2. Chi phí khi sai

- Không biết lỗi từ đâu thì cải tiến sai chỗ.
- Judge sai thì văn bản kém vẫn được cho qua.

## 3. Đánh giá

| Chỉ số | Cách đo | Ngưỡng chấp nhận |
|---|---|---|
| Độ khớp quyết định cuối với chuyên viên | `[CẦN XÁC NHẬN]` | `[CẦN XÁC NHẬN]` |
| Độ khớp judge với chuyên viên | Trên mẫu văn bản đã được chuyên viên chấm | `[CẦN XÁC NHẬN]` |

## 4. Hướng tiếp cận và thử nghiệm

### 4.1. Hướng tiếp cận ứng viên

| Hướng | Ưu điểm | Nhược điểm |
|---|---|---|
| `[CẦN XÁC NHẬN]` Chưa khảo sát thêm | | |

### 4.2. Dữ liệu cần chuẩn bị

- Mẫu văn bản kết quả đã được chuyên viên chấm, để hiệu chỉnh judge.

Các loại giấy tờ đã biết cần nhận dạng OCR. Danh sách chưa đầy đủ.

| # | Loại giấy tờ | Đặc điểm hình thức ảnh hưởng tới OCR | Bài toán liên quan |
|---|---|---|---|
| 1 | Giấy chứng nhận quyền sở hữu nhà ở và quyền sử dụng đất ở | Mẫu cũ, nhiều trang. Có sơ đồ thửa đất, bảng thông tin, trang ghi biến động viết tay kèm dấu | `AIP-001`, `AIP-004` |
| 2 | Bản vẽ hiện trạng | Bản vẽ kỹ thuật: sơ đồ, kích thước, bảng diện tích. Chữ nằm rải rác trong hình vẽ, ít văn bản liền mạch | `AIP-001` |
| 3 | Giấy chứng tử | Biểu mẫu hộ tịch, mẫu thay đổi theo thời kỳ. Bản cũ điền tay | `AIP-001`, `AIP-004` |
| 4 | Căn cước công dân | Thẻ 2 mặt, thường là ảnh chụp. Nhiều thế hệ: CMND 9 số, CCCD mã vạch, CCCD gắn chip, thẻ căn cước | `AIP-003`, `AIP-004` |
| 5 | Tờ đăng ký nhà - đất | Giấy tờ cũ, đánh máy hoặc viết tay, giấy ố, mực phai | `AIP-001`, `AIP-003` |
| 6 | Giấy chứng nhận hộ khẩu thường trú | Giấy tờ cũ (sổ hộ khẩu hết giá trị từ 01/01/2023). Nhiều trang, ghi biến động nhân khẩu bằng tay | `AIP-001`, `AIP-009` |
| 7 | Giấy sang đất | Giấy viết tay giữa các bên, **không có mẫu**. Bố cục và nội dung tự do | `AIP-001`, `AIP-005` |

Nhận xét cho việc sinh dữ liệu ([AIP-026](AIP-026-layered-golden-set.md)):

- Phần lớn là giấy tờ cũ hoặc viết tay. Bộ sinh cần thêm kiểu hiển thị chữ đánh máy, giấy cũ, mực phai, ngoài kiểu biểu mẫu A4 hiện có.
- Căn cước công dân là thẻ, cần template riêng theo khổ thẻ và từng thế hệ thẻ.
- Giấy sang đất không có mẫu cố định, nên không dựng template được. Phải sinh bố cục tự do và nội dung bằng LLM, giữ các trường có cấu trúc (họ tên, diện tích, số tiền, ngày) do generator quy tắc sinh.
- Hồ sơ có nhiều người: người đã mất (giấy chứng tử), người đứng tên trên giấy tờ nhà đất, các thành viên hộ. Persona cần mở rộng từ một người thành một nhóm người có quan hệ.

### 4.3. Nhật ký thử nghiệm

| Ngày | Thử nghiệm | Kết quả | Kết luận |
|---|---|---|---|
| | | | |

## 5. Câu hỏi còn mở

- [ ] Các giấy tờ ở mục 4.2 thuộc thủ tục nào? Bộ giấy tờ gợi ý thủ tục về thừa kế hoặc đăng ký biến động nhà đất `[CẦN XÁC NHẬN]`.
- [ ] Danh sách giấy tờ ở mục 4.2 còn thiếu loại nào?

## 6. Tài liệu tham chiếu

Quy tắc ghi: `standards/07-references.md`.

| Mã | Tài liệu | Chiều | Nội dung liên quan |
|---|---|---|---|
| `AIP-026` | [Golden set và metric theo từng tầng](AIP-026-layered-golden-set.md) | Dựa vào | Chạy đánh giá trên golden set |
| `AIP-023` | [Sinh văn bản kết quả có kiểm soát](AIP-023-controlled-generation.md) | Dựa vào | Chấm văn bản sinh ra |

## 7. Lịch sử thay đổi

| Ngày | Người sửa | Nội dung | Đã rà tham chiếu |
|---|---|---|---|
| 2026-09-28 | <Tên> | Tạo mới, định nghĩa ban đầu từ danh sách bài toán AI của luồng | Không cần |
| 2026-09-29 | <Tên> | Bổ sung danh sách giấy tờ cần nhận dạng ở mục 4.2 | Không cần |
| 2026-09-29 | binhnguyenSoftz | Tổ chức lại: gộp AIP-037 cũ (end-to-end) và AIP-038 cũ (LLM-as-judge); nhóm `AIG-09`; viết lại phát biểu bài toán | Có |
