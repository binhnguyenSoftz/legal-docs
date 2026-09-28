# 06 - Tài liệu kỹ thuật chung (`techs/`)

## 1. `techs/` dùng để làm gì?

`techs/` chứa tài liệu kỹ thuật **không thuộc riêng một tính năng nào**. Ví dụ: kiến trúc tổng thể, hạ tầng, quy ước cơ sở dữ liệu, cơ chế xác thực dùng chung, hướng dẫn cài môi trường dev.

Tài liệu kỹ thuật của một tính năng vẫn để trong `features/.../02-technical.md`. Vì vậy, trước khi viết, hỏi câu sau:

| Câu hỏi | Nếu "Có" thì viết ở |
|---|---|
| Nội dung chỉ đúng cho một tính năng? | `features/<MODULE>/<MÃ>-<short-name>/02-technical.md` |
| Nội dung dùng cho từ 2 tính năng trở lên, hoặc cho cả hệ thống? | `techs/<nhóm>/TEC-<NNN>-<short-name>.md` |
| Là một quyết định kiến trúc (chọn A thay vì B)? | `techs/adr/ADR-<NNNN>-<short-name>.md` |
| Là một bài toán AI cần nghiên cứu, thử nghiệm? | `problems/ai-problems/AIP-<NNN>-<short-name>.md`, thuộc một nhóm `AIG` |

> Ví dụ: "Cơ chế retry khi gọi ngân hàng" dùng cho cả thanh toán và hoàn tiền, nên viết ở `techs/integrations/`. Tài liệu kỹ thuật của `PAY-001` chỉ tóm tắt một dòng và trỏ liên kết tới đó.

`techs/` chỉ nói về kỹ thuật. Không viết quy tắc nghiệp vụ ở đây. Nếu cần nhắc tới nghiệp vụ, trỏ liên kết sang tài liệu nghiệp vụ của tính năng.

## 2. Cấu trúc thư mục

```text
docs/techs/
├── README.md              # Bảng tra cứu, nơi duy nhất cấp mã TEC và ADR
├── architecture/          # Kiến trúc tổng thể, danh sách service, cách các service gọi nhau
├── infrastructure/        # Môi trường, triển khai, CI/CD, giám sát, log
├── data/                  # Quy ước cơ sở dữ liệu, migration, sao lưu
├── security/              # Xác thực, phân quyền, mã hóa, quản lý secret
├── integrations/          # Hệ thống ngoài dùng chung (ngân hàng, SMS, email...)
├── guides/                # Hướng dẫn cho dev: cài môi trường, quy ước code, cách debug
├── ai-problems/           # Nhóm (AIG) và bài toán AI (AIP), hiện ở problems/ai-problems/ (xem mục 6)
└── adr/                   # Quyết định kiến trúc
```

- Chỉ tạo thư mục nhóm khi có tài liệu đầu tiên thuộc nhóm đó.
- Cần nhóm mới thì thêm vào bảng nhóm trong `techs/README.md` và báo với nhóm trước khi dùng.
- Một tài liệu chỉ thuộc một nhóm. Nếu phân vân, chọn nhóm mà người đọc sẽ tìm đến đầu tiên.

## 3. Đặt tên và mã

- Tài liệu chủ đề: `TEC-<NNN>-<short-name>.md`. Ví dụ `techs/data/TEC-003-migration-rules.md`.
- ADR: `ADR-<NNNN>-<short-name>.md`. Ví dụ `techs/adr/ADR-0007-use-postgresql.md`.
- Nhóm bài toán AI: `AIG-<NN>-<short-name>.md`. Ví dụ `problems/ai-problems/AIG-01-document-vision-ocr.md`.
- Bài toán AI: `AIP-<NNN>-<short-name>.md`. Ví dụ `problems/ai-problems/AIP-001-document-ocr.md`.
- Mã `TEC` đánh số chung toàn dự án, không theo nhóm. Nhờ vậy, chuyển tài liệu sang nhóm khác không phải đổi mã.
- Cấp mã trong `techs/README.md` trước khi tạo file, giống cách cấp mã tính năng.

> Lưu ý: `TEC-003` là tài liệu kỹ thuật chung. `TECH-PAY-001` là tài liệu kỹ thuật của tính năng `PAY-001`. Hai mã khác nhau, đừng nhầm.

Chi tiết mã số xem `02-id-conventions.md`.

## 4. Nội dung bắt buộc

Mọi tài liệu `TEC` viết theo `templates/TPL-TEC-topic.md` và phải có:

1. **Phạm vi áp dụng**: áp dụng cho service, repo, môi trường nào. Không áp dụng cho đâu.
2. **Sơ đồ tổng quan** có diễn giải, nếu tài liệu mô tả nhiều thành phần (theo `04-diagrams.md`).
3. **Quy tắc bắt buộc** đánh mã `TEC-<NNN>-R<NN>`, để tài liệu khác trỏ chính xác. Ví dụ `TEC-003-R02`.
4. **Ví dụ cụ thể**: lệnh, cấu hình, đoạn code mẫu chạy được.
5. **Tài liệu tham chiếu** theo `07-references.md`. Tài liệu `TEC` thường được nhiều tính năng dùng, nên cột "Được dùng bởi" phải đầy đủ.
6. **Lịch sử thay đổi**.

## 5. Giữ tài liệu `TEC` đúng với hệ thống

- Tài liệu `TEC` có một người phụ trách (`owner`). Thay đổi nội dung cần người đó duyệt.
- Mỗi khi đổi hạ tầng, quy ước chung hoặc thư viện dùng chung, sửa tài liệu `TEC` trong **cùng merge request** với code.
- Đổi hoặc bỏ một quy tắc `TEC-<NNN>-R<NN>` là thay đổi có ảnh hưởng rộng. Bắt buộc rà mọi tài liệu ở cột "Được dùng bởi" (xem `07-references.md`).
- Tài liệu không còn đúng thì đổi trạng thái thành `Deprecated` và ghi tài liệu thay thế. Không xóa file, không tái sử dụng mã.

## 6. Bài toán AI (`problems/ai-problems/`)

Mỗi bài toán AI trong luồng xử lý hồ sơ được định nghĩa riêng một file. Mục đích: đi sâu, thử nghiệm và theo dõi từng bài toán độc lập, nhưng vẫn thấy bài toán nào phụ thuộc bài toán nào.

- Bài toán chia hai tầng, mọi file nằm chung một thư mục, không chia thư mục con:
  - **Nhóm** `AIG-<NN>`: một năng lực AI (capability) cần có để hoàn thành luồng, ví dụ "Truy xuất pháp luật theo hiệu lực". Có bài toán nghiệp vụ, đầu vào/đầu ra, chỉ số cấp nhóm và danh sách bài toán con. Viết theo `templates/TPL-AIG-group.md`.
  - **Bài toán con** `AIP-<NNN>`: một vấn đề cụ thể trong nhóm, đủ nhỏ để thử nghiệm và theo dõi riêng. Trường `group` ghi nhóm, trường `kind` ghi loại: `problem`, `method`, `concern` hoặc `enabler` (ý nghĩa xem `problems/ai-problems/README.md` mục 3.1).
- Mã `AIG` và `AIP` cấp trong `problems/ai-problems/README.md`. Mã `AIP` đánh số chung, không theo nhóm, nên chuyển nhóm không đổi mã. Ràng buộc trong bài toán có mã `AIP-<NNN>-R<NN>`.
- Một phương pháp (`method`) không có giá trị riêng thì ghi vào "Hướng tiếp cận" của bài toán nó phục vụ, không cấp mã `AIP` mới.
- Bài toán con viết theo `templates/TPL-AIP-problem.md`, gồm: định nghĩa (phát biểu, vị trí trong luồng, đầu vào/đầu ra, ràng buộc), vì sao khó, đánh giá, hướng tiếp cận và nhật ký thử nghiệm, câu hỏi còn mở, tài liệu tham chiếu.
- Ngoài `status`, mỗi bài toán có `stage` (`Defined`, `Exploring`, `Decided`, `In production`) và `priority` theo thang MoSCoW (`Must`, `Should`, `Could`). Bài toán `Must` xử lý trước, theo thứ tự giai đoạn. Tiêu chí xếp mức và ý nghĩa `stage` xem `problems/ai-problems/README.md` mục 2 và mục 4. Nhóm `AIG` không có mức ưu tiên riêng.
- Chốt ngưỡng chấp nhận ở mục "Đánh giá" **trước** khi thử nghiệm. Nhờ vậy, thử nghiệm có tiêu chí dừng rõ ràng.
- Hướng tiếp cận đã chốt và có ảnh hưởng lâu dài thì ghi thành ADR. Khi đưa vào chạy thật, cách triển khai viết ở tài liệu `TEC` hoặc tài liệu kỹ thuật của tính năng. File `AIP` chỉ trỏ liên kết tới đó.
