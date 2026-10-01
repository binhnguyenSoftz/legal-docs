# Bài toán AI của luồng xử lý hồ sơ đất đai - Giải thích cho người mới

Tài liệu này kể lại bằng lời thường hệ thống AI đang giải quyết việc gì. Chi tiết từng phần xem [README](README.md) và các file `AIG`, `AIP`.

## 1. Bài toán trong một câu

Người dân nộp ảnh chụp giấy tờ của một hồ sơ đất đai, ví dụ hồ sơ đăng ký biến động quyền sử dụng đất. Hệ thống đọc giấy tờ, đối chiếu với quy định pháp luật đang có hiệu lực, rồi đề xuất **chấp thuận**, **từ chối** hoặc **cần bổ sung**, kèm căn cứ và bản nháp văn bản trả lời. Khi không đủ chắc chắn, hệ thống không tự quyết mà **chuyển cho cán bộ**. Quyết định cuối cùng luôn do cán bộ duyệt.

> Lưu ý: Tài liệu chưa chốt danh sách thủ tục đất đai cụ thể mà hệ thống hỗ trợ `[CẦN XÁC NHẬN]`.

## 2. Giấy tờ thường gặp

Phần lớn giấy tờ là giấy cũ hoặc viết tay, vì vậy máy khó đọc:

- Giấy chứng nhận quyền sử dụng đất (sổ đỏ, sổ hồng): mẫu cũ, nhiều trang, có sơ đồ thửa đất, trang ghi biến động viết tay kèm dấu.
- Bản vẽ hiện trạng: sơ đồ, kích thước, bảng diện tích, chữ nằm rải rác trong hình vẽ.
- Tờ đăng ký nhà - đất: giấy cũ, đánh máy hoặc viết tay, mực phai.
- Giấy sang đất: giấy viết tay giữa các bên, không theo mẫu nào.
- Giấy tờ về người: căn cước công dân, sổ hộ khẩu cũ, giấy chứng tử.

## 3. Ví dụ: một hồ sơ đăng ký biến động đất đai

1. Người dân nộp ảnh sổ đỏ, bản vẽ hiện trạng, căn cước, tờ khai và một giấy sang đất viết tay, tất cả trong một file.
2. Hệ thống đọc chữ trên từng trang, kể cả chữ viết tay và chữ bị dấu đỏ đè lên. Mỗi chữ đọc được có kèm điểm cho biết máy chắc chắn đến đâu.
3. Hệ thống tách file thành từng giấy tờ riêng và nhận ra đâu là sổ đỏ, đâu là bản vẽ, đâu là căn cước.
4. Hệ thống lấy ra các thông tin cần thiết: chủ sử dụng, số thửa, diện tích, địa chỉ thửa đất. Mỗi thông tin phải chỉ được vị trí trên ảnh. Ví dụ, `số thửa = 125` lấy từ dòng "Thửa số: 125" ở trang 2. Nếu không tìm thấy trên ảnh thì không được điền.
5. Hệ thống nhận ra người đứng tên trên sổ đỏ và người trên căn cước là cùng một người. Sau đó hệ thống so thông tin giữa các giấy tờ. Ví dụ, tổng diện tích các thửa trên sổ đỏ là `98,5 + 45,0 = 143,5 m²`, và con số này phải khớp với bản vẽ hiện trạng. Khi hai giấy ghi khác nhau, hệ thống phải xét đó là khác nhau thật hay chỉ do máy đọc sai.
6. Hệ thống kiểm tra hồ sơ còn thiếu giấy tờ nào so với yêu cầu của thủ tục.
7. Hệ thống tìm điều luật đất đai áp dụng, đúng phiên bản có hiệu lực vào thời điểm phát sinh hồ sơ, không mặc định lấy luật mới nhất.
8. Hệ thống xét từng điều kiện: đạt, không đạt hay chưa rõ. Ví dụ, với điều kiện "đất không có tranh chấp", văn bản của UBND xã chỉ ghi "chưa phát hiện tranh chấp", nên hệ thống kết luận "chưa rõ" và chuyển cán bộ kèm lý do.
9. Nếu đủ chắc chắn, hệ thống soạn nháp văn bản trả lời. Mọi thông tin trong văn bản đều được kiểm tra lại. Ví dụ, văn bản ghi "thửa 126" trong khi dữ liệu là `125` thì bị chặn và phải soạn lại.

## 4. Các bước chính

| Bước | Máy làm gì | Vì sao khó |
|---|---|---|
| Đọc ảnh | Đọc chữ trên ảnh kèm mức độ chắc chắn | Giấy cũ, mực phai, chữ viết tay, dấu đè chữ; máy hay tự tin cả khi đọc sai |
| Phân loại, tách | Tách file thành từng giấy tờ và nhận loại giấy | Nhiều giấy tờ nằm lẫn trong một file, sổ đỏ có nhiều trang |
| Lấy thông tin | Lấy chủ sử dụng, số thửa, diện tích... kèm vị trí trên ảnh | Giấy sang đất không có mẫu; không được tự bịa khi chữ không rõ |
| Khớp người, địa chỉ | Nhận ra các giấy tờ nói về cùng một người, một hộ, một địa chỉ | Tên viết khác nhau, địa chỉ đổi theo đơn vị hành chính |
| Đối chiếu | So thông tin giữa các giấy tờ, tìm giấy tờ còn thiếu | Phải phân biệt giấy ghi khác nhau thật với máy đọc sai |
| Tìm luật | Tìm đúng điều luật đất đai, đúng phiên bản theo thời điểm | Luật bị sửa đổi, thay thế nhiều lần, có quy định chuyển tiếp |
| Ra đề xuất | Xét từng điều kiện rồi đề xuất kết quả, hoặc chuyển cán bộ | Phải biết khi nào mình không chắc |
| Soạn văn bản | Soạn văn bản trả lời đúng mẫu, trích dẫn đúng luật | Không được bịa thông tin hay điều luật |

Song song với các bước trên, nhóm còn phải làm thêm các việc sau:

- Đo chất lượng từng bước bằng một bộ hồ sơ mẫu đã có đáp án.
- Chống việc nội dung giấy tờ "ra lệnh" cho AI.
- Bảo vệ dữ liệu cá nhân của người dân.
- Học từ những chỗ cán bộ sửa lại.

## 5. Ba điều hệ thống luôn phải giữ

1. **Có nguồn:** mọi thông tin phải chỉ được lấy từ vùng ảnh nào, mọi điều luật phải có trong kết quả tìm kiếm. Không có nguồn thì không dùng.
2. **Không chắc thì chuyển người:** thà chuyển cán bộ còn hơn từ chối oan hoặc chấp thuận sai.
3. **Đúng luật, đúng thời điểm:** chỉ áp dụng quy định có hiệu lực vào lúc phát sinh hồ sơ.

## 6. Ba phần khó nhất, cần thử sớm

1. Đọc chữ viết tay trên giấy tờ đất cũ và biết chính xác máy chắc chắn đến đâu.
2. Phân biệt giấy tờ ghi khác nhau thật với việc máy đọc sai.
3. Tìm đúng luật đất đai theo thời điểm, và biết khi nào nên chuyển cán bộ thay vì tự quyết.

## 7. Giải pháp đề xuất

Luồng giải pháp cho bài toán này xem [Luồng giải pháp xử lý hồ sơ đất đai](../../solutions/00-solution-overview.md).
