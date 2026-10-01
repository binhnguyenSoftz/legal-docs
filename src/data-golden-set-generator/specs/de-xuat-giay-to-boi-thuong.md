# Đề xuất 5 loại giấy tờ mới cho thủ tục giải tỏa đền bù

Tài liệu này dùng để **chốt nhãn và quy tắc gán** trước khi viết `schema.yaml`, template và sinh dữ liệu train. Các mục có `[CẦN XÁC NHẬN]` là giả định, cần đối chiếu hồ sơ thật hoặc chuyên viên trước khi code.

Trạng thái: bản nháp, chưa có code. Ngày lập: 2026-10-01.

## 1. Tổng quan

### 1.1. Năm loại giấy tờ

| # | `doc_type` đề xuất | Tên đầy đủ | Ai lập | Vai trò trong hồ sơ |
|---|---|---|---|---|
| 1 | `giay-xac-nhan-1131` | GXN 1131 `[CẦN XÁC NHẬN]` tên và mẫu, giả định ở mục 2 | UBND cấp xã | Đầu vào: xác nhận nguồn gốc, thời điểm sử dụng đất, tình trạng tranh chấp |
| 2 | `bt-dat` | Bảng chiết tính bồi thường, hỗ trợ về đất | Đơn vị bồi thường, UBND cấp xã phê duyệt | Kết quả: tiền bồi thường đất |
| 3 | `bt-cong-trinh` | Bảng chiết tính bồi thường nhà, công trình, vật kiến trúc | Như trên | Kết quả: tiền bồi thường tài sản trên đất |
| 4 | `khen-thuong` | Quyết định thưởng bàn giao mặt bằng trước thời hạn | UBND cấp xã | Kết quả: tiền thưởng tiến độ |
| 5 | `tai-dinh-cu` | Quyết định bố trí tái định cư (hoặc phiếu bốc thăm/giao suất TĐC) | UBND cấp xã | Kết quả: suất tái định cư hoặc tiền tự lo chỗ ở |

> Lưu ý: 7 giấy tờ hiện có đều là **giấy tờ đầu vào** người dân nộp. Bốn giấy tờ 2-5 là **giấy tờ đầu ra** do Nhà nước lập, dựa trên chính các giấy tờ đầu vào. Vì vậy số liệu trên giấy tờ đầu ra phải **tính ra được** từ hồ sơ. Đây là điểm khác lớn nhất so với 7 giấy tờ cũ, và quyết định cách gán nhãn (mục 1.3).

### 1.2. Căn cứ pháp lý dùng để dựng quy tắc

| Văn bản | Nội dung dùng | Trạng thái |
|---|---|---|
| Luật Đất đai 2024, Chương VII | Điều kiện bồi thường đất, tài sản; tái định cư | `[CẦN XÁC NHẬN]` điều khoản cụ thể |
| Nghị định 88/2024/NĐ-CP | Bồi thường, hỗ trợ, tái định cư; suất tái định cư tối thiểu | `[CẦN XÁC NHẬN]` |
| Nghị định 151/2025/NĐ-CP | Phân thẩm quyền chính quyền 2 cấp: UBND cấp xã ra quyết định thu hồi, phê duyệt phương án từ 01/7/2025 | `[CẦN XÁC NHẬN]` |
| Quyết định 11/2026/QĐ-UBND TP.HCM (06/3/2026) | Mức thưởng, sàn 60% giá xây mới, hỗ trợ tạm cư, suất TĐC tối thiểu | `[CẦN XÁC NHẬN]` áp dụng cho địa bàn nào |

Hồ sơ hiện sinh có `submit_date` trong 01/7/2025 - 30/6/2026. Nếu giấy tờ đầu ra lập trước 06/3/2026 thì phải áp quy định cũ của địa phương `[CẦN XÁC NHẬN]`. Đề xuất đơn giản hóa: cho mọi giấy tờ đầu ra lập từ 06/3/2026, chỉ áp một bộ quy định.

### 1.3. Hai lớp nhãn

1. **Nhãn trích xuất** (AIP-005): từng trường trên giấy tờ + bbox, giống 7 giấy tờ cũ. Khai báo trong `schema.yaml`.
2. **Nhãn suy luận** (AIP-011, AIP-027): số liệu đúng tính từ hồ sơ, ghi vào `ground_truth.json > compensation`. Mô hình phải tự tính lại rồi so với số in trên giấy tờ. Giấy tờ bị cài lỗi thì số in khác số đúng, và nhãn quyết định ghi rõ quy tắc vi phạm.

Ví dụ: hồ sơ có diện tích thu hồi 68,5 m², đơn giá đất 52.000.000 đ/m². Nhãn suy luận `tien_bt_dat = 3.562.000.000`. Ca lỗi M12 in trên bảng chiết tính `3.652.000.000` (đảo chữ số). Mô hình đúng phải trả `request_supplement`, lý do `R10`.

### 1.4. Ngữ cảnh mới cần thêm vào generator

Bảy giấy tờ cũ chỉ cần `people`, `property`, `timeline`. Năm giấy tờ mới cần thêm một đối tượng `thu_hoi` (dự án và đợt thu hồi), dùng chung cho cả 5 giấy tờ:

| Khóa | Ý nghĩa | Cách sinh đề xuất |
|---|---|---|
| `thu_hoi.ten_du_an` | Tên dự án | Chọn từ danh sách mẫu ("Mở rộng đường ...", "Chống ngập ...") |
| `thu_hoi.so_qd` / `ngay_qd` | Số, ngày quyết định thu hồi đất | Ngày trong [`ngay_mat` + 30, `submit_date` - 30] |
| `thu_hoi.pham_vi` | `toan-bo` hoặc `mot-phan` | Biến thể (coverage) |
| `thu_hoi.dien_tich` | Diện tích thu hồi | `toan-bo`: bằng diện tích đo thực tế; `mot-phan`: 20-80% |
| `thu_hoi.gia_dat` | Giá đất cụ thể tính bồi thường (đ/m²) | 15-150 triệu, làm tròn 1.000 |
| `thu_hoi.don_gia_xay_moi` | Đơn giá xây mới theo `ket_cau` (đ/m² sàn) | Bảng tra cố định trong code `[CẦN XÁC NHẬN]` số liệu |
| `thu_hoi.han_ban_giao` / `ngay_ban_giao` | Thời hạn và ngày bàn giao thực tế | Biến thể `ban_giao`: đúng hạn / trễ hạn |
| `thu_hoi.co_cho_o_khac` | Hộ còn chỗ ở khác trong địa bàn xã | Quyết định điều kiện tái định cư |

Thứ tự thời gian mở rộng từ dòng thời gian hiện có:

`ngay_mat` → GXN 1131 → `thu_hoi.ngay_qd` → bảng chiết tính (đất, công trình) → quyết định tái định cư → `ngay_ban_giao` → quyết định khen thưởng.

## 2. GXN 1131

> Cảnh báo: không tìm được văn bản công khai nào có số "1131" khớp với hồ sơ bồi thường. Mục này dựng theo **giả định**: đây là giấy UBND cấp xã xác nhận nguồn gốc, thời điểm sử dụng đất, vì đây là giấy xác nhận bắt buộc trong mọi hồ sơ bồi thường và khớp với trục `nguon_goc` hiện có. Cần mẫu thật để chốt (xem mục 7, câu 1).

### 2.1. Vì sao cần

Giấy chứng nhận chỉ ghi diện tích công nhận. Khi đo thực tế lớn hơn (bản vẽ hiện trạng), phần chênh lệch chỉ được bồi thường nếu UBND cấp xã xác nhận sử dụng ổn định, không tranh chấp, và thời điểm bắt đầu sử dụng trước mốc quy định. Mốc thời điểm (trước 18/12/1980, 1980-15/10/1993, từ 15/10/1993) quyết định tỷ lệ bồi thường phần chênh lệch.

### 2.2. Hình thức

A4, 1-2 trang, in máy, có phần điền tay. Có quốc hiệu, tên UBND xã/phường, số văn bản, chữ ký chủ tịch, dấu. Giấy mới (lập sau khi người đứng tên mất).

### 2.3. Trường đề xuất

| `name` | Nhãn | `type` | Nguồn | `fill` |
|---|---|---|---|---|
| `so_van_ban` | Số | `text` | `gen: pattern` "{n}/GXN-UBND" | printed |
| `co_quan` | UBND xã/phường | `text` | địa chỉ thửa đất, cấp xã 2 cấp | printed |
| `nguoi_su_dung` | Người sử dụng đất | `person_name` | `people.nguoi_mat.ho_ten` | printed |
| `nguoi_de_nghi` | Người đề nghị xác nhận | `person_name` | `people.nguoi_nop.ho_ten` | printed |
| `so_thua` / `to_ban_do` | Thửa, tờ bản đồ | `text` | `property` | printed |
| `dia_chi_thua_dat` | Địa chỉ thửa đất | `address` | `property.dia_chi_parts` (2 cấp) | printed |
| `dien_tich_gcn` | Diện tích theo giấy chứng nhận | `area` | `property.dien_tich` | printed |
| `dien_tich_thuc_te` | Diện tích đo thực tế | `area` | bản vẽ hiện trạng | printed |
| `nguon_goc` | Nguồn gốc sử dụng đất | `free_text` | `gen: template` từ `ben_ban`, `ngay_sang` | printed |
| `thoi_diem_su_dung` | Thời điểm bắt đầu sử dụng | `date` | `timeline.ngay_sang` | printed |
| `tinh_trang_tranh_chap` | Tình trạng tranh chấp | `checkbox` | "Không tranh chấp" (ca hợp lệ) | printed |
| `phu_hop_quy_hoach` | Phù hợp quy hoạch tại thời điểm sử dụng | `checkbox` | | printed |
| `ngay_ky` | Ngày ký | `date` | `doc.issue_date` | printed |
| `nguoi_ky` | Người ký | `person_name` | `gen: person_name` | printed |

`decorations`: chữ ký + dấu ở `nguoi_ky`.

### 2.4. Quy tắc gán

- `thoi_diem_su_dung` phải đúng mốc `nguon_goc` của kịch bản. Đây là nhãn chính, dùng tiếp ở bảng chiết tính đất.
- `dien_tich_thuc_te` khớp bản vẽ hiện trạng. Nếu bằng `dien_tich_gcn` thì GXN chỉ xác nhận nguồn gốc, không có phần chênh lệch.
- Ngày ký sau `ngay_mat`, trước `thu_hoi.ngay_qd`.

## 3. Bồi thường đất (`bt-dat`)

### 3.1. Hình thức

A4 ngang, 1-2 trang, in máy toàn bộ. Phần đầu là thông tin hộ, phần chính là bảng tính nhiều dòng, cuối là tổng cộng bằng số và bằng chữ, chữ ký người lập, người kiểm tra, người duyệt, dấu. Bảng là thách thức OCR chính: ô gộp, số dài, dấu chấm phân cách nghìn.

### 3.2. Trường đề xuất

Phần đầu:

| `name` | Nhãn | `type` | Nguồn |
|---|---|---|---|
| `ten_du_an` | Dự án | `text` | `thu_hoi.ten_du_an` |
| `can_cu_qd_thu_hoi` | Căn cứ quyết định thu hồi số, ngày | `text` | `thu_hoi.so_qd`, `ngay_qd` |
| `chu_su_dung` | Chủ sử dụng (đã mất) | `person_name` | `people.nguoi_mat.ho_ten` |
| `nguoi_nhan` | Người đại diện nhận tiền | `person_name` | `people.nguoi_nop.ho_ten` |
| `so_cccd_nguoi_nhan` | Số định danh | `id_number` | `persona.cccd` |
| `dia_chi_thua_dat`, `so_thua`, `to_ban_do` | | | `property` |

Bảng tính, mỗi dòng một nhóm trường lặp (`groups`, tiền tố `d1_`, `d2_`...):

| Trường trong dòng | Nhãn | `type` |
|---|---|---|
| `noi_dung` | Nội dung (VD "Đất ở có GCN", "Phần chênh lệch, sử dụng trước 15/10/1993") | `text` |
| `dien_tich` | Diện tích (m²) | `area` |
| `don_gia` | Đơn giá (đ/m²) | `money` |
| `ty_le` | Tỷ lệ bồi thường (%) | `percent` |
| `thanh_tien` | Thành tiền (đ) | `money` |

Cuối bảng: `tong_cong` (`money`), `tong_bang_chu` (`money_words`).

### 3.3. Quy tắc tính (nhãn suy luận)

```text
dong_gcn       = min(thu_hoi.dien_tich, dien_tich_gcn) × gia_dat × 100%
dong_chenh     = max(0, thu_hoi.dien_tich - dien_tich_gcn) × gia_dat × ty_le(nguon_goc)
tien_bt_dat    = dong_gcn + dong_chenh
```

`ty_le(nguon_goc)` `[CẦN XÁC NHẬN]` theo quy định địa phương. Đề xuất tạm: trước 18/12/1980 = 100%, 1980-15/10/1993 = 100% trong hạn mức, từ 15/10/1993 = 60%.

Quy tắc kiểm tra trên giấy tờ:

- Mỗi dòng: `thanh_tien = dien_tich × don_gia × ty_le`, làm tròn đến đồng.
- `tong_cong = Σ thanh_tien`; `tong_bang_chu` đọc ra đúng `tong_cong`.
- Tổng diện tích các dòng = `thu_hoi.dien_tich` ≤ diện tích đo thực tế.

## 4. Bồi thường công trình (`bt-cong-trinh`)

### 4.1. Hình thức

Giống bảng chiết tính đất (A4 ngang, in máy, bảng nhiều dòng). Có thể in chung một tờ với bảng đất ở ngoài thực tế `[CẦN XÁC NHẬN]`. Đề xuất tách riêng để mỗi `doc_type` có một bố cục.

### 4.2. Trường đề xuất

Phần đầu giống `bt-dat`. Bảng tính, mỗi dòng một hạng mục:

| Trường trong dòng | Nhãn | `type` | Ví dụ |
|---|---|---|---|
| `hang_muc` | Hạng mục | `text` | Nhà chính; Mái che; Tường rào; Sân xi măng; Giếng khoan |
| `ket_cau` | Kết cấu | `text` | `property.nha.ket_cau` |
| `don_vi` | Đơn vị | `text` | m², m, cái |
| `khoi_luong` | Khối lượng | `number` | Nhà chính: `dien_tich_san` |
| `don_gia_xay_moi` | Đơn giá xây mới | `money` | Tra theo `ket_cau` |
| `ty_le_con_lai` | Tỷ lệ chất lượng còn lại (%) | `percent` | Theo năm xây dựng |
| `gia_tri_hien_co` | Giá trị hiện có | `money` | |
| `bo_sung_san_60` | Bổ sung lên 60% giá xây mới | `money` | |
| `thanh_tien` | Thành tiền | `money` | |

Cuối bảng: `tong_cong`, `tong_bang_chu`.

### 4.3. Quy tắc tính

```text
gia_xay_moi     = khoi_luong × don_gia_xay_moi
gia_tri_hien_co = gia_xay_moi × ty_le_con_lai
bo_sung_san_60  = max(0, 60% × gia_xay_moi - gia_tri_hien_co)      # QĐ 11/2026 TP.HCM
thanh_tien      = gia_tri_hien_co + bo_sung_san_60
```

- `ty_le_con_lai` giảm theo tuổi nhà (`submit_date.year - property.nha.nam_xay_dung`) `[CẦN XÁC NHẬN]` bảng khấu hao. Nhà xây những năm 1980-1990 thường dưới 60%, nên dòng bổ sung sàn 60% xuất hiện thường xuyên. Đây là điểm dễ sai cho mô hình.
- Thu hồi `mot-phan`: chỉ tính phần nhà nằm trong ranh thu hồi; nếu phần còn lại không sử dụng được thì tính cả căn `[CẦN XÁC NHẬN]`.
- Khối lượng nhà chính khớp `dien_tich_san` và `so_tang` trên giấy chứng nhận, tờ đăng ký.

## 5. Khen thưởng (`khen-thuong`)

### 5.1. Hình thức

Quyết định hành chính A4 dọc, 1 trang, in máy: quốc hiệu, số quyết định, "Căn cứ ...", "QUYẾT ĐỊNH: Điều 1. Thưởng cho ...", số tiền bằng số và bằng chữ, chữ ký, dấu. Có thể kèm danh sách nhiều hộ `[CẦN XÁC NHẬN]`; đề xuất bản đầu chỉ một hộ.

### 5.2. Trường đề xuất

| `name` | Nhãn | `type` | Nguồn |
|---|---|---|---|
| `so_qd` / `ngay_qd` | Số, ngày quyết định | `text` / `date` | sau `ngay_ban_giao` |
| `can_cu_bien_ban_ban_giao` | Biên bản bàn giao mặt bằng ngày | `date` | `thu_hoi.ngay_ban_giao` |
| `nguoi_duoc_thuong` | Hộ/ông bà được thưởng | `person_name` | `people.nguoi_nop.ho_ten` (đại diện) |
| `dia_chi_thua_dat` | Địa chỉ | `address` | `property` |
| `pham_vi_thu_hoi` | Thu hồi toàn bộ / một phần | `text` | `thu_hoi.pham_vi` |
| `so_tien` | Số tiền thưởng | `money` | tính |
| `so_tien_bang_chu` | Bằng chữ | `money_words` | tính |
| `nguoi_ky` | Người ký | `person_name` | `gen: person_name` |

### 5.3. Quy tắc tính

```text
du_dieu_kien = ngay_ban_giao <= han_ban_giao
tien_thuong  = 0                                    nếu không đủ điều kiện (không có quyết định)
             = min(tien_bt_dat, 50.000.000)          nếu toan-bo
             = min(50% × tien_bt_dat, 25.000.000)    nếu mot-phan
```

Mức trần theo QĐ 11/2026 TP.HCM. Công thức gốc "thưởng bằng số tiền bồi thường, hỗ trợ về đất nhưng không quá ..." `[CẦN XÁC NHẬN]` cách hiểu. Với giá đất TP.HCM, gần như luôn chạm trần, nên nhãn thực tế là 50 triệu hoặc 25 triệu.

Quy tắc kiểm tra: ngày quyết định sau ngày bàn giao; bàn giao trễ hạn thì không được có quyết định khen thưởng.

## 6. Tái định cư (`tai-dinh-cu`)

### 6.1. Hình thức

Quyết định A4 dọc, 1-2 trang, in máy, kèm bảng thông tin suất tái định cư (khu, lô/căn, diện tích, giá). Một số nơi dùng phiếu bốc thăm căn hộ có điền tay số căn `[CẦN XÁC NHẬN]`.

### 6.2. Biến thể

| Biến thể | Khi nào | Nội dung chính |
|---|---|---|
| `can-ho` | Đủ điều kiện, nhận căn hộ chung cư | Block, tầng, số căn, diện tích sàn, giá bán |
| `nen-dat` | Đủ điều kiện, nhận nền đất | Lô, số nền, diện tích, giá thu tiền sử dụng đất |
| `tu-lo-cho-o` | Đủ điều kiện, tự lo chỗ ở | Số tiền hỗ trợ tự lo chỗ ở |
| (không có giấy) | Không đủ điều kiện | Hồ sơ không có `tai-dinh-cu` |

### 6.3. Trường đề xuất

| `name` | Nhãn | `type` | Biến thể |
|---|---|---|---|
| `so_qd` / `ngay_qd` | Số, ngày quyết định | `text` / `date` | tất cả |
| `nguoi_duoc_bo_tri` | Người được bố trí | `person_name` | tất cả |
| `so_nhan_khau` | Số nhân khẩu của hộ | `number` | tất cả |
| `khu_tdc` | Khu tái định cư | `text` | `can-ho`, `nen-dat` |
| `block` / `tang` / `so_can` | Block, tầng, số căn | `text` | `can-ho` |
| `lo` / `so_nen` | Lô, số nền | `text` | `nen-dat` |
| `dien_tich_tdc` | Diện tích | `area` | `can-ho`, `nen-dat` |
| `gia_tdc` | Giá bán / giá đất TĐC | `money` | `can-ho`, `nen-dat` |
| `ho_tro_suat_toi_thieu` | Hỗ trợ đủ suất TĐC tối thiểu | `money` | `can-ho`, `nen-dat` |
| `tien_chenh_lech` | Số tiền phải nộp thêm / được nhận lại | `money` | `can-ho`, `nen-dat` |
| `tien_tu_lo` | Hỗ trợ tự lo chỗ ở | `money` | `tu-lo-cho-o` |

### 6.4. Quy tắc gán

```text
du_dieu_kien_tdc   = (pham_vi == toan-bo hoặc phần còn lại không đủ để ở) và not co_cho_o_khac
ho_tro_suat_toi_thieu = max(0, gia_suat_toi_thieu - tien_bt_dat)          # QĐ 11/2026 TP.HCM
tien_chenh_lech       = gia_tdc - tien_bt_dat - ho_tro_suat_toi_thieu      # âm = được nhận lại
```

- `so_nhan_khau` khớp số nhân khẩu còn sống trong sổ hộ khẩu (đã có ở `compensation.nhan_khau`).
- Số suất: mặc định 1 suất/hộ. Hộ có con đã lập gia đình cùng ở (con dâu/rể trong hộ khẩu) có thể được xét thêm suất `[CẦN XÁC NHẬN]`. Đề xuất bản đầu luôn 1 suất.
- `gia_suat_toi_thieu` và `tien_tu_lo` `[CẦN XÁC NHẬN]` số liệu.

## 7. Nhãn hồ sơ, quy tắc và ca lỗi đề xuất

### 7.1. Bổ sung `ground_truth.json > compensation`

```json
{
  "gxn": {"thoi_diem_su_dung": "1988-04-12", "nguon_goc_dat": "1980-15-10-1993", "khong_tranh_chap": true},
  "thu_hoi": {"pham_vi": "toan-bo", "dien_tich": 68.5, "gia_dat": 52000000,
              "han_ban_giao": "2026-05-30", "ngay_ban_giao": "2026-05-20"},
  "tien_bt_dat": 3562000000,
  "tien_bt_cong_trinh": 845300000,
  "tien_thuong": 50000000,
  "tai_dinh_cu": {"du_dieu_kien": true, "hinh_thuc": "can-ho", "so_suat": 1, "tien_chenh_lech": -1250000000},
  "tong_nhan": 4457300000
}
```

Toàn bộ số liệu tính từ dữ liệu đúng, không bị ca lỗi sửa (giống `compensation` hiện có).

### 7.2. Quy tắc mới

| Mã | Quy tắc |
|---|---|
| R07 | GXN: thời điểm sử dụng đất, diện tích phải khớp giấy sang đất, giấy chứng nhận, bản vẽ hiện trạng |
| R08 | Giấy tờ đầu ra phải ghi đúng người: chủ sử dụng là người đứng tên đã mất, người nhận là người đại diện |
| R09 | Diện tích bồi thường không vượt diện tích thu hồi và diện tích đo thực tế |
| R10 | Số tiền trên bảng chiết tính phải đúng công thức: thành tiền từng dòng, tổng cộng, bằng chữ khớp bằng số |
| R11 | Thưởng chỉ khi bàn giao đúng hoặc trước hạn, không vượt mức trần |
| R12 | Tái định cư chỉ bố trí cho hộ đủ điều kiện; số nhân khẩu khớp sổ hộ khẩu |
| R13 | Thứ tự ngày: GXN → quyết định thu hồi → bảng chiết tính → bàn giao → khen thưởng |

### 7.3. Ca lỗi

| Mã | `kind` | Giấy tờ, trường | `perturb` | Kỳ vọng |
|---|---|---|---|---|
| M10 | `field_conflict` | `giay-xac-nhan-1131.thoi_diem_su_dung` | sang mốc khác | `request_supplement`, R07 |
| M11 | `field_conflict` | `bt-dat.chu_su_dung` | `typo_name` | `request_supplement`, R08 |
| M12 | `field_value` | `bt-dat.tong_cong` | `swap_digits` | `request_supplement`, R10 |
| M13 | `field_value` | `bt-dat.tong_bang_chu` | lệch một hàng đơn vị | `request_supplement`, R10 |
| M14 | `field_value` | `bt-dat.d1_dien_tich` | lớn hơn diện tích thu hồi | `request_supplement`, R09 |
| M15 | `field_value` | `bt-cong-trinh.bo_sung_san_60` | bỏ dòng bổ sung | `request_supplement`, R10 |
| M16 | `field_value` | `khen-thuong.so_tien` | vượt trần | `request_supplement`, R11 |
| M17 | `date_order` | `khen-thuong` khi `ngay_ban_giao > han_ban_giao` | | `request_supplement`, R11 |
| M18 | `field_conflict` | `tai-dinh-cu.so_nhan_khau` | ±1 | `request_supplement`, R12 |
| M19 | `date_order` | `bt-dat.ngay_lap` trước `thu_hoi.ngay_qd` | | `request_supplement`, R13 |

> Lưu ý: M12, M13, M15 sửa số trên giấy tờ nhưng các số khác vẫn đúng. Mô hình chỉ phát hiện được khi tự tính lại, không thể so khớp chuỗi giữa các giấy tờ. Đây là ca kiểm tra AIP-011.

### 7.4. Trục biến thể mới (`coverage`)

| Trục | Giá trị | Ảnh hưởng |
|---|---|---|
| `pham_vi` | `toan-bo`, `mot-phan` | Diện tích thu hồi, mức thưởng, điều kiện TĐC |
| `ban_giao` | `dung-han`, `tre-han` | Có hay không có `khen-thuong` |
| `tdc` | `can-ho`, `nen-dat`, `tu-lo-cho-o`, `khong` | Biến thể `tai-dinh-cu` |

Nhân thẳng vào 108 tổ hợp hiện có sẽ thành 1.728 tập mới phủ đủ. Đề xuất: ba trục mới xoay vòng độc lập với 5 trục cũ (lệch pha theo số thứ tự), để mỗi giá trị vẫn xuất hiện đều mà không cần phủ hết tích Descartes. Cần sửa `dossier.plan()`.

> Lưu ý: hiện README ghi "mỗi tập luôn đủ 7 giấy tờ, không có ca thiếu giấy tờ". Với `ban_giao: tre-han` và `tdc: khong`, hồ sơ hợp lệ sẽ **không có** `khen-thuong` hoặc `tai-dinh-cu`. Cần đổi `required` sang điều kiện, và nhãn cần phân biệt "không có vì không đủ điều kiện" với "thiếu giấy tờ".

## 8. Câu hỏi cần chốt trước khi code

1. **GXN 1131 là giấy gì?** Số 1131 là số mẫu, số quyết định, hay mã nội bộ? Cần một bản mẫu (đã che thông tin) để dựng template. Nếu không phải giấy xác nhận nguồn gốc đất, mục 2 và R07, M10 phải làm lại.
2. **Bốn giấy tờ đầu ra là đầu vào hay đầu ra của hệ thống?** Nếu hệ thống đọc chúng (thủ tục chi trả, khiếu nại) thì nhãn chính là trích xuất + kiểm tra số học. Nếu hệ thống phải *sinh ra* chúng (AIP-023) thì nhãn chính là số liệu ở mục 7.1, còn ảnh giấy tờ chỉ dùng làm ví dụ đầu ra.
3. **Bồi thường đất và công trình** là hai tờ riêng hay chung một bảng chiết tính? Có tách quyết định phê duyệt và bảng chi tiết không?
4. **Địa bàn và bộ quy định:** chỉ TP.HCM theo QĐ 11/2026, hay cần nhiều tỉnh? Đơn giá xây mới, bảng khấu hao, giá suất TĐC tối thiểu lấy từ đâu?
5. **Hỗ trợ** (tạm cư, di chuyển, ổn định đời sống) có cần làm thành giấy tờ hoặc dòng riêng không? Hiện chưa có trong danh sách.
6. **Khen thưởng và tái định cư** có lập theo danh sách nhiều hộ không? Nếu có, cần thêm hộ "nhiễu" để mô hình phải tìm đúng dòng của hộ mình.

## 9. Việc làm sau khi chốt

1. Thêm `generator/thu_hoi.py`: dựng đối tượng `thu_hoi`, bảng đơn giá, các hàm tính ở mục 3-6.
2. Thêm kiểu trường `money`, `money_words`, `percent` và `perturb` cho số tiền.
3. Viết `schema.yaml` + `template.html.j2` cho 5 giấy tờ dưới `templates/giai-toa-den-bu/`. Bảng chiết tính dùng `page: a4` ngang.
4. Mở rộng `procedure.yaml`: giấy tờ, rule R07-R13, mutation M10-M19, trục coverage.
5. Viết test: hồ sơ hợp lệ thì mọi phép tính ở mục 3-6 khớp; mỗi mutation đổi đúng một trường.
6. Sinh thử 5 hồ sơ, so với mẫu thật, nhờ chuyên viên duyệt.

## 10. Tài liệu tham chiếu

- [Quy định về bồi thường khi thu hồi đất theo Luật Đất đai 2024](https://xaydungchinhsach.chinhphu.vn/chinh-sach-moi-ve-boi-thuong-thu-hoi-dat-theo-luat-dat-dai-2024-119240227145829751.htm)
- [Toàn văn Nghị định quy định về bồi thường, hỗ trợ, tái định cư](https://xaydungchinhsach.chinhphu.vn/toan-van-nghi-dinh-quy-dinh-ve-boi-thuong-ho-tro-tai-dinh-cu-khi-nha-nuoc-thu-hoi-dat-119240906111916662.htm)
- [7 điểm mới về bồi thường tại TP.HCM theo Quyết định 11/2026/QĐ-UBND](https://thuviennhadat.vn/phap-ly-nha-dat/7-diem-moi-ve-boi-thuong-khi-thu-hoi-dat-tai-tp-hcm-theo-quyet-dinh-11-2026-qd-ubnd-737628.html)
- [TP.HCM thưởng cho trường hợp bàn giao đất bị thu hồi trước quy định](https://plo.vn/tphcm-se-thuong-cho-nhung-truong-hop-ban-giao-dat-bi-thu-hoi-truoc-quy-dinh-post899134.html)
- AIP-005 (trích xuất theo schema), AIP-011 (suy luận thời gian, số học), AIP-027 (đánh giá đầu cuối)
