# Hỏi đáp bồi thường, giải tỏa: Phòng Kinh tế, Hạ tầng và Đô thị phường Bình Đông (giao diện web)

Chatbot chỉ phục vụ **một mục đích**: giải đáp về bồi thường, hỗ trợ, tái định cư khi Nhà nước thu hồi đất trên địa bàn phường Bình Đông (TP.HCM). Gồm: hồ sơ cần chuẩn bị (kể cả khi người đứng tên đã mất), cách tính tiền bồi thường đất và nhà, thưởng bàn giao mặt bằng, tái định cư, tạm cư, chi trả và khiếu nại. Câu hỏi về thủ tục khác được hướng sang Bộ phận Một cửa.

Cùng thủ tục với bộ sinh dữ liệu [data-golden-set-generator](../data-golden-set-generator/README.md) (`giai-toa-den-bu`). Căn cứ pháp lý và số liệu lấy từ [đề xuất giấy tờ bồi thường](../data-golden-set-generator/specs/de-xuat-giay-to-boi-thuong.md). Angular 22 (standalone components, signals, zoneless, SSR + hydration), Angular Material/CDK cho menu, tooltip, snackbar, focus trap. Chạy ngay với dữ liệu mẫu, chưa cần backend.

## 1. Chạy

```bash
npm install
npm start          # dev server có SSR, http://localhost:4200
npm test           # unit test (Vitest)
npm run build      # build production: dist/.../browser và dist/.../server
npm run serve:ssr  # chạy server Node (Express) đã build, cổng 4000 (đổi bằng PORT)
```

### SSR

- Mọi route render trên server theo từng request (`RenderMode.Server` trong `app.routes.server.ts`), không prerender lúc build vì lịch sử trò chuyện và tài khoản là của từng người.
- Trình duyệt hydrate lại HTML từ server (`provideClientHydration(withEventReplay())`); thao tác của người dùng trước khi hydrate xong được phát lại.
- Ngày giờ luôn tính theo giờ Việt Nam (UTC+7, `core/utils/date.ts` và `DATE_PIPE_DEFAULT_OPTIONS`), để server chạy múi giờ nào cũng render giống trình duyệt.
- Server chỉ nhận request có header `Host` nằm trong danh sách cho phép (chống SSRF). Mặc định chỉ có `localhost` (`angular.json` → `security.allowedHosts`). Khi triển khai, khai báo tên miền thật qua biến môi trường:

```bash
NG_ALLOWED_HOSTS=trolyhoidap.example.vn PORT=4000 npm run serve:ssr
```

- Bố cục mobile/tablet do CSS media query xử lý nên HTML từ server đã đúng khung hình. Riêng tablet, sidebar được thu gọn sau khi hydrate (server không biết kích thước màn hình), nên có thể thấy sidebar co lại một nhịp lúc tải trang.

## 2. Cấu trúc

```text
src/app/
├── core/
│   ├── config/organization.ts       Tên đơn vị, nơi nộp hồ sơ, địa chỉ, hotline, giờ làm việc
│   ├── models/chat.models.ts        ChatMessage, Conversation, SourceReference, AdministrativeProcedure, SuggestedQuestion
│   ├── services/
│   │   ├── assistant-gateway.ts     Ranh giới với backend (ASSISTANT_GATEWAY) + MockAssistantGateway
│   │   ├── chat.service.ts          Một lượt hỏi đáp: gửi, chờ, nhận trả lời / lỗi, thử lại, đánh giá
│   │   ├── conversation.service.ts  Lịch sử: danh sách, chọn, tìm kiếm, nhóm theo ngày
│   │   └── voice-input.service.ts   Nhập giọng nói tiếng Việt (Web Speech API)
│   ├── mocks/                       Câu trả lời, nguồn, thủ tục, lịch sử mẫu
│   └── utils/
├── shared/
│   ├── components/
│   │   ├── government-header/       Header: logo đơn vị, tên đơn vị, menu, trạng thái, tài khoản
│   │   ├── source-card/             Thẻ nguồn trích dẫn (badge "Nguồn chính thức", trích dẫn mở/đóng)
│   │   ├── procedure-card/          Thẻ thủ tục hành chính
│   │   ├── suggested-question/      Chip câu hỏi gợi ý
│   │   ├── state-notice/            Trạng thái rỗng / lỗi / cảnh báo
│   │   ├── rich-text/               Hiển thị inline markup an toàn (không dùng innerHTML)
│   │   └── icon, org-logo, assistant-avatar
│   └── styles/                      Design token, mixin, nút dùng chung
└── features/chatbot/
    ├── chatbot-page/                Bố cục, responsive, phím tắt, điều phối
    ├── chat-sidebar/                + new-conversation-button, conversation-search, conversation-list
    ├── chat-welcome/
    ├── chat-conversation/           + typing-indicator
    ├── chat-message/                user-message, assistant-message, message-content
    └── chat-input/
```

Component trong `shared/` và `features/` chỉ nhận `input()` và phát `output()`; trạng thái nằm ở service trong `core/`. Riêng `chatbot-page` inject service.

## 3. Nội dung câu trả lời

Câu trả lời là danh sách block có cấu trúc (`ContentBlock`): `paragraph`, `heading`, `list` (có thứ tự / không), `table`, `callout` (info / success / warning), `procedure`. Trong text dùng inline markup:

| Cú pháp | Hiển thị |
|---|---|
| `**đậm**` | Chữ đậm |
| `==nổi bật==` | Đánh dấu vàng nhạt |
| `[nhãn](https://...)` | Liên kết, chỉ nhận `http(s)` |
| `[^1]` | Số trích dẫn, trỏ tới `sources[0]` |

Trạng thái (`AssistantStatus`): `complete`, `no-result` (không tìm thấy thông tin), `no-official-source` (hiện cảnh báo "Thông tin tham khảo"), `error` (lỗi kết nối, có nút thử lại).

## 4. Thông tin đơn vị

Sửa trong `src/app/core/config/organization.ts`. Các trường `address`, `hotline`, `email` đang để trống và sẽ không hiển thị cho tới khi điền. Logo hiện là chữ "BĐ" trong vòng tròn (`org-logo`), thay bằng logo chính thức khi có.

## 5. Dữ liệu mẫu

`MockAssistantGateway` chọn câu trả lời theo từ khóa (không phân biệt dấu, khớp trọn âm tiết, ý định đầu tiên khớp được chọn), độ trễ giả 0,9–1,8 giây.

| Câu hỏi chứa | Kết quả |
|---|---|
| "giấy tờ", "đã mất", "thừa kế" | Hồ sơ cần chuẩn bị: bảng 6 nhóm giấy tờ, cảnh báo thông tin phải khớp, các bước, thẻ thủ tục, 3 nguồn |
| "tính", "giá đất", "bao nhiêu" | Cách tính tiền bồi thường, có ví dụ 68,5 m² × 52.000.000 đ |
| "tiền thưởng", "bàn giao mặt bằng" | Mức thưởng bàn giao đúng hạn |
| "tái định cư", "căn hộ", "nền đất" | Điều kiện và hình thức tái định cư |
| "khiếu nại", "không đồng ý" | Khiếu nại, thời hạn 90 ngày |
| "giấy tay", "giấy sang" | Đất mua bằng giấy tay |
| "không phép" | Nhà xây không phép |
| "chi trả", "nhận tiền", "khi nào" | Tiến độ chi trả |
| "tạm cư", "thuê nhà" | Chỉ có nguồn không chính thức → cảnh báo |
| "bồi thường", "giải tỏa", "thu hồi" (chung) | Quy trình bồi thường |
| "khai sinh", "hộ kinh doanh", "giấy phép xây dựng"... | Ngoài phạm vi → hướng sang Bộ phận Một cửa |
| "mất kết nối", "lỗi kết nối" | Lỗi kết nối |
| Không khớp từ khóa nào | Không tìm thấy thông tin phù hợp |

Ý định được thử theo thứ tự, ý định cụ thể đứng trước (vd. "không đồng ý với mức bồi thường" vào khiếu nại, không vào cách tính). Test `assistant-gateway.spec.ts` kiểm tra mọi câu gợi ý trên màn hình chào đều ra đúng câu trả lời.

Văn bản dẫn chiếu (Luật Đất đai 2024, Nghị định 88/2024, Nghị định 151/2025, Quyết định 11/2026/QĐ-UBND TP.HCM, Luật Khiếu nại 2011) và các mức thưởng, sàn 60% giá xây mới lấy theo spec, trong đó nhiều mục còn `[CẦN XÁC NHẬN]`. URL, ngày cập nhật và trích dẫn chỉ để minh họa. Cần chuyên viên phường duyệt nội dung trước khi đưa vào sử dụng.

## 6. Nối backend

Viết một class implement `AssistantGateway` (gọi API, trả về `Observable<AssistantReply>`), rồi khai báo trong `app.config.ts`:

```ts
{ provide: ASSISTANT_GATEWAY, useExisting: HttpAssistantGateway }
```

UI không cần sửa.

## 7. Responsive và truy cập

| Màn hình | Bố cục |
|---|---|
| ≥ 1200px | Sidebar đầy đủ, thu gọn được thành thanh icon |
| 768–1199px | Sidebar mặc định thu gọn, menu header gom vào nút "…" từ 1100px |
| < 768px | Header gọn, sidebar thành drawer (focus trap, Esc để đóng), thẻ một cột, ô nhập cố định dưới |

Phím tắt: `Enter` gửi, `Shift+Enter` xuống dòng, `Ctrl/⌘+K` cuộc trò chuyện mới. Có skip link, `role="log"` cho khung chat, `aria-live` cho trạng thái đang xử lý, tôn trọng `prefers-reduced-motion`.
