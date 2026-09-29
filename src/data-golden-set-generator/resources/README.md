# Dữ liệu tham chiếu

Faker `vi_VN` có ít tên và địa chỉ, nên generator ưu tiên dữ liệu ở đây. File mẫu hiện có chỉ là danh sách khởi đầu, cần bổ sung từ nguồn công khai.

| Thư mục/file | Nội dung | Trạng thái | Nguồn gợi ý |
|---|---|---|---|
| `names/ho.txt` | Họ, dạng `họ<TAB>trọng số` (64 họ, gồm họ đặc trưng dân tộc thiểu số và họ kép) | Có | Thống kê họ phổ biến |
| `names/ten_dem_nam.txt`, `ten_dem_nu.txt` | Tên đệm theo giới (khoảng 45 mỗi giới) | Có | |
| `names/ten_nam.txt`, `ten_nu.txt` | Tên riêng theo giới (80-110 mỗi giới) | Có | |
| `names/ten_nam_xua.txt`, `ten_nu_xua.txt` | Tên thường gặp ở thế hệ sinh trước 1970 (Tư, Sáu, Nở, Lành...) | Có | |
| `admin/cccd_province_codes.csv` | Mã tỉnh trong số CCCD (63 tỉnh cũ), đầu số CMND 9 số | Đủ 63 tỉnh; `[CẦN XÁC NHẬN]` cột `cmnd_prefix` mới có 5 tỉnh, còn lại tạm dùng mã thống kê | Thông tư 59/2021/TT-BCA |
| `admin/units_2025.csv` | 3.321 xã sau sắp xếp 01/7/2025 (2 cấp) | Có, dựng bằng `admin/build_units.py` | [vietnamese-provinces-database](https://github.com/thanglequoc/vietnamese-provinces-database) (MIT) |
| `admin/units_pre2025.csv` | 9.817 cặp xã cũ (tỉnh, huyện, xã trước 01/7/2025) -> xã mới, toàn quốc. Generator lấy địa chỉ từ file này | Có, dựng bằng `admin/build_units.py`; bỏ 730 xã cũ trùng tên không phân biệt được | Như trên: dữ liệu v2.4.1 + bảng sáp nhập từ sapnhap.bando.com.vn |
| `fonts/handwriting/*.ttf` | Font viết tay có dấu tiếng Việt | Có 4 font (xem `fonts/LICENSE.md`) | Thêm font mở, hoặc render từ UIT-HWDB |
| `fonts/print/*.ttf` | Font in: Tinos (thay Times), Cousine (máy chữ), Arimo (thẻ) | Có | google/fonts |
| `stamps/*.png` | Ảnh dấu mộc giả (nền trong suốt), chèn ở bước nhiễu | Tùy chọn: template đã tự vẽ dấu "MẪU GIẢ LẬP" bằng SVG | Tự vẽ, **không** dùng dấu thật của cơ quan |
| `signatures/*.png` | Ảnh chữ ký giả (nền trong suốt), chèn ở bước nhiễu | Tùy chọn: template đã tự vẽ chữ ký SVG | Tự vẽ |
| `backgrounds/*.jpg` | Ảnh nền bàn cho giả lập chụp điện thoại | `[CẦN BỔ SUNG]` | Ảnh tự chụp |

> Lưu ý về địa chỉ: từ 01/7/2025 bỏ cấp huyện. Giấy tờ lập trước mốc này ghi địa chỉ 3 cấp, sau mốc ghi 2 cấp. Một hồ sơ có thể chứa cả hai dạng cho cùng một nơi, đây là ca thật cần sinh cho [AIP-008](../../../docs/problems/ai-problems/AIP-008-address-normalization.md), không phải lỗi mâu thuẫn.
