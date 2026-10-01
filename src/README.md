# Mã nguồn

Mỗi thư mục con của `src/` là một module độc lập (ứng dụng, service, thư viện, công cụ), có README, file phụ thuộc và test riêng.

## 1. Đặt tên module

Cú pháp: `<tầng>-<miền>-<vai-trò>`. Tiếng Anh, chữ thường, nối bằng gạch ngang, giống quy tắc đặt tên thư mục trong `docs/standards/01-folder-structure.md`.

| Phần | Ý nghĩa | Giá trị |
|---|---|---|
| `<tầng>` | Loại module, để nhóm các module cùng loại khi sắp xếp theo tên | Xem bảng mục 2 |
| `<miền>` | Nghiệp vụ hoặc đối tượng module phục vụ, có thể nhiều từ | `dossier`, `citizen`, `officer`, `ocr`, `legal-retrieval`, `golden-set` |
| `<vai-trò>` | Module chạy dưới dạng gì | `web`, `mobile`, `api`, `worker`, `service`, `generator`, `sdk`, `cli` |

### Ví dụ

| Module | Nội dung |
|---|---|
| `fe-citizen-web` | Cổng nộp hồ sơ cho người dân |
| `fe-officer-web` | Màn hình duyệt hồ sơ cho cán bộ |
| `be-dossier-api` | API tiếp nhận, tra cứu hồ sơ |
| `be-dossier-worker` | Xử lý nền: điều phối luồng xử lý hồ sơ |
| `ai-ocr-service` | Đọc chữ in, chữ viết tay |
| `ai-extraction-service` | Trích xuất trường theo schema |
| `ai-legal-retrieval-service` | Truy xuất văn bản pháp luật |
| `data-golden-set-generator` | Sinh hồ sơ giả có ground truth cho golden set |
| `lib-common-python` | Tiện ích Python dùng chung |
| `infra-k8s` | Manifest triển khai |

## 2. Các tầng

| Tầng | Dùng cho |
|---|---|
| `fe` | Giao diện người dùng: web, mobile |
| `be` | Service nghiệp vụ, API, worker |
| `ai` | Service hoặc pipeline chạy model: OCR, trích xuất, suy luận, sinh văn bản |
| `data` | Công cụ và pipeline dữ liệu: sinh, gán nhãn, ẩn danh, chuẩn bị dataset |
| `lib` | Thư viện dùng chung, không tự chạy |
| `infra` | Hạ tầng, triển khai, CI/CD |
| `tool` | Công cụ nội bộ cho lập trình viên, không thuộc các tầng trên |

Cần tầng mới thì bổ sung vào bảng này trước khi tạo module.

## 3. Quy tắc

- Tên nói module **làm gì**, không nói **dùng công nghệ gì**: `ai-ocr-service`, không đặt `ai-paddle-ocr`.
- Không dùng tên chung chung như `common`, `utils`, `core` đứng một mình. Phải có tầng và miền: `lib-common-python`.
- Đổi tên module phải sửa mọi đường dẫn tham chiếu tới nó: tài liệu trong `docs/`, pipeline trong `.jenkins/`, và các module khác.

## 4. Danh sách module

| Module | Tầng | Mô tả | Tài liệu liên quan |
|---|---|---|---|
| [data-golden-set-generator](data-golden-set-generator/README.md) | `data` | Sinh hồ sơ hành chính giả có ground truth | `AIP-026`, `AIP-027` |
| [fe-citizen-assistant-web](fe-citizen-assistant-web/README.md) | `fe` | Chatbot hỏi đáp bồi thường, giải tỏa khi thu hồi đất, Phòng Kinh tế, Hạ tầng và Đô thị phường Bình Đông (Angular SSR, dữ liệu mẫu) | `AIP-027` |
