# 02 - Quy tắc mã số

Mã số giúp tra cứu nhanh: gõ mã vào ô tìm kiếm là ra đúng tài liệu.

## 1. Mã module

3 đến 4 chữ cái viết hoa, đại diện cho một nhóm chức năng lớn.

| Mã | Module (ví dụ) |
|---|---|
| `PAY` | Thanh toán |
| `AUT` | Xác thực |
| `USR` | Người dùng |
| `RPT` | Báo cáo |
| `INF` | Hạ tầng |

Thêm module mới: ghi vào bảng ở `features/README.md` và báo với nhóm trước khi dùng.

## 2. Mã tính năng

Cú pháp: `<MODULE>-<NNN>`. Ví dụ `PAY-001`.

- `NNN` là 3 chữ số, tăng dần trong từng module.
- Mã đã cấp **không bao giờ đổi và không tái sử dụng**, kể cả khi tính năng bị xóa.
- Tính năng bị bỏ: giữ thư mục, đổi trạng thái thành `Deprecated`.

## 3. Mã tài liệu

Cú pháp: `<LOẠI>-<MODULE>-<NNN>`. Dùng trong phần thông tin đầu file.

| Loại | Ý nghĩa | Ví dụ |
|---|---|---|
| `BIZ` | Tài liệu nghiệp vụ | `BIZ-PAY-001` |
| `TECH` | Tài liệu kỹ thuật | `TECH-PAY-001` |
| `API` | Đặc tả API | `API-PAY-001` |
| `SEQ` | Sơ đồ sequence | `SEQ-PAY-001` |
| `TEST` | Kế hoạch/kịch bản test | `TEST-PAY-001` |

Nếu một tính năng có nhiều tài liệu cùng loại, thêm hậu tố: `TECH-PAY-001-a`, `TECH-PAY-001-b`.

## 4. Mã tài liệu kỹ thuật chung

Tài liệu trong `techs/` không thuộc module nào, nên đánh số chung toàn dự án. Mã `TEC` và `ADR` cấp trong `techs/README.md`, mã `AIG` và `AIP` cấp trong `problems/ai-problems/README.md`.

| Loại | Cú pháp | Ví dụ | Tên file |
|---|---|---|---|
| Tài liệu kỹ thuật chung | `TEC-NNN` | `TEC-003` | `techs/data/TEC-003-migration-rules.md` |
| Quy tắc trong tài liệu `TEC` | `TEC-NNN-R<NN>` | `TEC-003-R02` | - |
| Quyết định kiến trúc (ADR) | `ADR-NNNN` | `ADR-0007` | `techs/adr/ADR-0007-use-postgresql.md` |
| Nhóm bài toán AI (capability) | `AIG-NN` | `AIG-05` | `problems/ai-problems/AIG-05-cross-document-validation.md` |
| Bài toán AI (bài toán con trong nhóm) | `AIP-NNN` | `AIP-010` | `problems/ai-problems/AIP-010-conflict-vs-error.md` |
| Ràng buộc trong bài toán AI | `AIP-NNN-R<NN>` | `AIP-005-R02` | - |

> Lưu ý: `TEC-003` (tài liệu kỹ thuật chung) khác `TECH-PAY-003` (tài liệu kỹ thuật của tính năng `PAY-003`).

## 5. Mã khác

| Loại | Cú pháp | Ví dụ |
|---|---|---|
| Prompt | `PRM-NNN` | `PRM-002` |
| Việc cần làm (cách cấp mã: `todo/README.md` mục 5) | `TSK-NNN` | `TSK-013` |
| Yêu cầu nghiệp vụ trong tài liệu | `<MÃ TÍNH NĂNG>-R<NN>` | `PAY-001-R03` |
| Bước trong luồng | `S<NN>` | `S04` |
| Mã lỗi | `<MODULE>-E<NNN>` | `PAY-E012` |

Mã yêu cầu và mã bước giúp người khác nói chính xác: "sửa `PAY-001-R03`" thay vì "sửa cái yêu cầu thứ 3 ở dưới".

## 6. Cách tra cứu

- Tìm theo mã tính năng: gõ `PAY-001` vào ô tìm kiếm của repo.
- Tìm mọi tài liệu của một module: vào `features/PAY/`.
- Tìm theo tên: xem bảng trong `features/README.md` (tính năng), `techs/README.md` (tài liệu `TEC`, ADR) hoặc `problems/ai-problems/README.md` (nhóm và bài toán AI).
- Các bảng đó là **nguồn duy nhất** để cấp mã. Cấp mã xong phải cập nhật bảng ngay.
- Tìm mọi tài liệu đang dùng một tài liệu: gõ mã của nó (ví dụ `TEC-003`) vào ô tìm kiếm. Kết quả phải khớp với mục "Tài liệu tham chiếu" của tài liệu đó (xem `07-references.md`).
