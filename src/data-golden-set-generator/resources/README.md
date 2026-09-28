# Dữ liệu tham chiếu

Faker `vi_VN` có ít tên và địa chỉ, nên generator ưu tiên dữ liệu ở đây. File mẫu hiện có chỉ là danh sách khởi đầu, cần bổ sung từ nguồn công khai.

| Thư mục/file | Nội dung | Trạng thái | Nguồn gợi ý |
|---|---|---|---|
| `names/ho.txt` | Họ, dạng `họ<TAB>trọng số` | Khởi đầu | Thống kê họ phổ biến |
| `names/ten_dem_nam.txt`, `ten_dem_nu.txt` | Tên đệm theo giới | Khởi đầu | |
| `names/ten_nam.txt`, `ten_nu.txt` | Tên riêng theo giới | Khởi đầu | |
| `admin/cccd_province_codes.csv` | Mã nơi đăng ký khai sinh trong số CCCD (63 tỉnh cũ), đầu số CMND 9 số | `[CẦN BỔ SUNG]` đủ 63 dòng; `[CẦN XÁC NHẬN]` cột `cmnd_prefix` | Thông tư 59/2021/TT-BCA, Phụ lục |
| `admin/units_2025.csv` | Tỉnh, xã sau sắp xếp 01/7/2025 (2 cấp) | `[CẦN BỔ SUNG]` | Danh mục đơn vị hành chính của Cục Thống kê |
| `admin/units_pre2025.csv` | Tỉnh, huyện, xã trước 01/7/2025 (3 cấp) và xã mới tương ứng. Generator lấy địa chỉ từ file này | Khởi đầu, `[CẦN XÁC NHẬN]` ánh xạ xã cũ -> xã mới | Nghị quyết sắp xếp đơn vị hành chính cấp xã 2025 của từng tỉnh |
| `fonts/handwriting/*.ttf` | Font viết tay có dấu tiếng Việt | Có 4 font (xem `fonts/LICENSE.md`) | Thêm font mở, hoặc render từ UIT-HWDB |
| `fonts/print/*.ttf` | Font in: Tinos (thay Times), Cousine (máy chữ), Arimo (thẻ) | Có | google/fonts |
| `stamps/*.png` | Ảnh dấu mộc giả (nền trong suốt), chèn ở bước nhiễu | Tùy chọn: template đã tự vẽ dấu "MẪU GIẢ LẬP" bằng SVG | Tự vẽ, **không** dùng dấu thật của cơ quan |
| `signatures/*.png` | Ảnh chữ ký giả (nền trong suốt), chèn ở bước nhiễu | Tùy chọn: template đã tự vẽ chữ ký SVG | Tự vẽ |
| `backgrounds/*.jpg` | Ảnh nền bàn cho giả lập chụp điện thoại | `[CẦN BỔ SUNG]` | Ảnh tự chụp |

> Lưu ý về địa chỉ: từ 01/7/2025 bỏ cấp huyện. Giấy tờ lập trước mốc này ghi địa chỉ 3 cấp, sau mốc ghi 2 cấp. Một hồ sơ có thể chứa cả hai dạng cho cùng một nơi, đây là ca thật cần sinh cho [AIP-008](../../../docs/problems/ai-problems/AIP-008-address-normalization.md), không phải lỗi mâu thuẫn.
