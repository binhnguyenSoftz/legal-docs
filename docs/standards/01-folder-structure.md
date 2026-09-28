# 01 - Cấu trúc thư mục

## 1. Cây thư mục chuẩn

```text
docs/
├── README.md
├── standards/                  # Quy chuẩn (ít thay đổi)
├── templates/                  # Mẫu tài liệu
├── prompts/                    # Prompt dự án
├── todo/                       # Việc cần làm của toàn dự án (mã TSK)
│   ├── README.md               # Chỉ chứa quy ước, không liệt kê việc
│   └── items/                  # Mỗi việc một file, trạng thái nằm trong file
│       └── TSK-001-target-procedures.md
├── techs/                      # Tài liệu kỹ thuật chung, ADR (xem 06-tech-docs.md)
│   ├── README.md               # Bảng tra cứu mã TEC và ADR
│   ├── architecture/
│   │   └── TEC-001-system-overview.md
│   ├── ai-problems/            # Hiện nằm ở problems/ai-problems/, không chia thư mục con
│   │   ├── README.md           # Sơ đồ luồng, bảng tra cứu mã AIG và AIP
│   │   ├── AIG-01-document-vision-ocr.md   # Nhóm bài toán (capability)
│   │   └── AIP-001-document-ocr.md      # Bài toán con
│   └── adr/
│       └── ADR-0001-use-postgresql.md
└── features/
    ├── README.md               # Bảng tra cứu mã tính năng
    └── PAY/                    # Thư mục module (mã module viết hoa)
        └── PAY-001-qr-payment/
            ├── 00-index.md     # Tóm tắt + liên kết tới các file khác
            ├── 01-business.md
            ├── 02-technical.md
            ├── 03-api.md
            ├── 04-sequence.md
            ├── 05-test.md      # Tùy chọn
            └── assets/         # Ảnh, file sơ đồ nguồn
```

## 2. Đặt tên

- Thư mục và file đặt tên bằng tiếng Anh, chữ thường, nối bằng dấu gạch ngang. Ví dụ: `qr-payment`.
- Thư mục tính năng bắt đầu bằng mã: `PAY-001-qr-payment`.
- Tài liệu trong `techs/` bắt đầu bằng mã: `TEC-001-system-overview.md`, `ADR-0001-use-postgresql.md`.
- File trong thư mục tính năng đánh số thứ tự `00-`, `01-`, ... để xếp đúng thứ tự đọc.
- Tên ngắn, nhìn vào biết nội dung. Không dùng tên như `final`, `new`, `v2-real`.

## 3. Để tài liệu ở `features/` hay `techs/`?

- Nội dung chỉ đúng cho một tính năng: để trong thư mục tính năng đó.
- Nội dung dùng cho từ 2 tính năng trở lên hoặc cả hệ thống: để trong `techs/`. Tài liệu tính năng chỉ tóm tắt một dòng và trỏ liên kết.
- Chi tiết và ví dụ xem `06-tech-docs.md`.

## 4. Khi nào tách thành thư mục con?

Tách khi gặp **một trong các dấu hiệu** sau:

| Dấu hiệu | Ví dụ |
|---|---|
| File dài hơn khoảng 300 dòng | `02-technical.md` đã 450 dòng |
| Có hơn 7 mục cấp 2 (`##`) | Khó cuộn tìm |
| Có nhiều luồng độc lập | Thanh toán thành công, hoàn tiền, hết hạn |
| Nhiều người cùng sửa một file, hay bị xung đột | - |

Cách tách:

1. Đổi file thành thư mục cùng tên: `02-technical.md` thành `02-technical/`.
2. Trong thư mục mới, tạo `00-index.md` để tóm tắt và liệt kê các file con.
3. Mỗi file con chỉ nói về một chủ đề: `01-architecture.md`, `02-data.md`, `03-error-handling.md`.
4. Cập nhật mọi liên kết cũ trỏ tới file gốc, kể cả trong mục "Tài liệu tham chiếu" của tài liệu khác. Chuyển từng dòng tham chiếu của file gốc sang file con có nội dung liên quan.
5. Ghi rõ trong `00-index.md` của tính năng rằng mục này đã được tách.

Ví dụ sau khi tách:

```text
PAY-001-qr-payment/
└── 02-technical/
    ├── 00-index.md
    ├── 01-architecture.md
    ├── 02-data.md
    └── 03-error-handling.md
```

## 5. Quy tắc liên kết

- Dùng đường dẫn tương đối, ví dụ `../PAY-002-refund/00-index.md`.
- Khi nhắc tính năng khác, ghi mã kèm liên kết: `[PAY-002](../PAY-002-refund/00-index.md)`.
- Không copy nội dung từ tài liệu khác. Chỉ tóm tắt một dòng và trỏ liên kết.
- Tài liệu nào dùng nội dung của tài liệu khác thì ghi vào mục "Tài liệu tham chiếu" ở cả hai phía, theo `07-references.md`.
