# Đề xuất 5 loại giấy tờ mới cho thủ tục giải tỏa đền bù

Tài liệu này dùng để **chốt nhãn và quy tắc gán** trước khi viết `schema.yaml`, template và sinh dữ liệu train. Các mục có `[CẦN XÁC NHẬN]` là giả định, cần đối chiếu hồ sơ thật hoặc chuyên viên trước khi code.

Trạng thái: đã chốt (mục 8) và đã code ở thủ tục `giai-toa-den-bu-tphcm`, `generator/thu_hoi.py`. Ngày lập: 2026-10-01.

Mục 2-6 là đề xuất ban đầu. Chỗ nào code khác đề xuất thì ghi ở mục 8.2; nguồn sự thật là `schema.yaml` của từng giấy tờ.

## 1. Tổng quan

### 1.1. Năm loại giấy tờ

| # | `doc_type` đề xuất | Tên đầy đủ | Ai lập | Vai trò trong hồ sơ |
|---|---|---|---|---|
| 1 | `gxn-1131` | GXN 1131 `[CẦN XÁC NHẬN]` tên và mẫu, giả định ở mục 2 | UBND cấp xã | Đầu vào: xác nhận nguồn gốc, thời điểm sử dụng đất, tình trạng tranh chấp |
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

`ty_le(nguon_goc)` `[CẦN XÁC NHẬN]` theo quy định địa phương.

> Lưu ý: bản đã code chỉ có dòng `dong_gcn` (100%). Hồ sơ hợp lệ hiện có diện tích bản vẽ bằng giấy chứng nhận, nên không có phần chênh lệch. Thêm phần chênh lệch là việc sau (mục 8.3).

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

## 7. Nhãn hồ sơ, quy tắc và ca lỗi

### 7.1. Bổ sung `ground_truth.json`

Mục mới `thu_hoi` chứa toàn bộ đợt thu hồi (dự án, số và ngày quyết định, các dòng bảng tính, hạn và ngày bàn giao, suất tái định cư). Mục `compensation` thêm các nhãn suy luận:

```json
{
  "pham_vi_thu_hoi": "mot-phan",
  "dien_tich_thu_hoi": 69.2,
  "gia_dat": 35541000,
  "tien_bt_dat": 2459437200,
  "tien_bt_cong_trinh": 138319500,
  "ban_giao_dung_han": true,
  "tien_thuong": 25000000,
  "tai_dinh_cu": {"du_dieu_kien": true, "hinh_thuc": "tu-lo-cho-o", "so_suat": 1, "nhan_khau": 4,
                  "tien_phai_nop": 0, "tien_duoc_nhan": 0},
  "tong_bt_ht": 2745728700
}
```

Toàn bộ số liệu tính từ dữ liệu đúng, không bị ca lỗi sửa. Ví dụ ca M17 (thưởng dù bàn giao trễ): giấy khen thưởng ghi 50 triệu, nhãn `tien_thuong` vẫn là 0. `tong_bt_ht` = đất + công trình + thưởng + hỗ trợ suất tối thiểu + hỗ trợ tự lo chỗ ở.

### 7.2. Quy tắc mới

| Mã | Quy tắc |
|---|---|
| R07 | GXN 1131 phải khớp giấy sang đất, giấy chứng nhận, bản vẽ hiện trạng về thời điểm sử dụng đất và thửa đất |
| R08 | Giấy tờ bồi thường phải ghi đúng chủ sử dụng (người đứng tên đã mất) và người đại diện nhận tiền |
| R09 | Diện tích tính bồi thường không vượt diện tích thu hồi |
| R10 | Số tiền trên bảng chiết tính phải đúng công thức: thành tiền từng dòng, tổng cộng, bằng chữ khớp bằng số |
| R11 | Chỉ thưởng khi bàn giao đúng hạn, không vượt mức trần |
| R12 | Số nhân khẩu trên quyết định tái định cư phải khớp sổ hộ khẩu |
| R13 | Thứ tự ngày: GXN, quyết định thu hồi và bảng chiết tính, bàn giao, khen thưởng |

### 7.3. Ca lỗi

| Mã | `kind` | Giấy tờ, trường | Cách gây lỗi | Kỳ vọng |
|---|---|---|---|---|
| M10 | `field_conflict` | `gxn-1131.thoi_diem_su_dung` | `year_shift` (lệch 1-3 năm) | `request_supplement`, R07 |
| M11 | `field_conflict` | `bt-dat.chu_su_dung` | `typo_name` | `request_supplement`, R08 |
| M12 | `field_conflict` | `bt-dat.tong_cong` | `money_swap` (đảo 2 chữ số) | `request_supplement`, R10 |
| M13 | `field_conflict` | `bt-dat.tong_bang_chu` | `money_shift` (lệch 1-20 triệu) | `request_supplement`, R10 |
| M14 | `field_conflict` | `bt-dat.d1_dien_tich` | `area_up` (lớn hơn 5-25%) | `request_supplement`, R09 |
| M15 | `calc_error` | `bt-cong-trinh.ct1_thanh_tien` | quên bổ sung 60%, hoặc lệch 5-15% | `request_supplement`, R10 |
| M16 | `field_value` | `khen-thuong.so_tien` (+ bằng chữ) | 60, 75 hoặc 100 triệu | `request_supplement`, R11 |
| M17 | `thu_hoi_override` | có `khen-thuong` dù bàn giao trễ | | `request_supplement`, R11 |
| M18 | `field_conflict` | `tai-dinh-cu.so_nhan_khau` | `int_shift` (±1) | `request_supplement`, R12 |
| M19 | `date_order` | `bt-dat.ngay_lap` trước ngày GXN | `before` | `request_supplement`, R13 |

> Lưu ý: M12, M13, M15 chỉ sửa một số, các số khác vẫn đúng. Mô hình chỉ phát hiện được khi tự tính lại, không so khớp chuỗi giữa các giấy tờ được. Đây là ca kiểm tra AIP-011.

M16, M17, M18 khai báo `needs` (cần có giấy khen thưởng, cần bàn giao trễ, cần có giấy tái định cư). Generator chỉ chọn các ca này khi kịch bản biến thể của hồ sơ cho phép.

### 7.4. Trục biến thể mới (`coverage`)

| Trục | Giá trị | Ảnh hưởng |
|---|---|---|
| `pham_vi` | `toan-bo`, `mot-phan` | Diện tích thu hồi, mức thưởng, điều kiện TĐC |
| `ban_giao` | `dung-han`, `tre-han` | Có hay không có `khen-thuong` |
| `tdc` | `can-ho`, `nen-dat`, `tu-lo-cho-o`, `khong` | Biến thể hoặc không có `tai-dinh-cu` |

Ba trục mới đặt trước 5 trục cũ nên đổi nhanh nhất: 16 hồ sơ đầu phủ mọi tình huống bồi thường, 1.728 hồ sơ phủ mọi tổ hợp. Không cần sửa `dossier.plan()`.

Hồ sơ hợp lệ có thể **không có** `khen-thuong` (bàn giao trễ) hoặc `tai-dinh-cu` (không đủ điều kiện). Hai giấy tờ này khai báo `when` trong `procedure.yaml`. Khi không có vì không đủ điều kiện, generator không ghi vào `missing_documents`, vì đây không phải lỗi thiếu giấy tờ.

## 8. Các quyết định đã chốt

### 8.1. Trả lời câu hỏi mở

| # | Câu hỏi | Đã chốt |
|---|---|---|
| 1 | GXN 1131 là giấy gì? | Giữ giả định: giấy UBND cấp xã xác nhận nguồn gốc, thời điểm sử dụng đất. `doc_type: gxn-1131`. Vẫn `[CẦN XÁC NHẬN]` khi có mẫu thật |
| 2 | Giấy tờ đầu ra là đầu vào hay đầu ra của hệ thống? | Làm cả hai. Mỗi trường có nhãn trích xuất + bbox; `compensation` có số đúng để chấm phần tự tính |
| 3 | Đất và công trình chung hay riêng? | Hai tờ riêng (`bt-dat`, `bt-cong-trinh`), mỗi tờ một bố cục A4 ngang |
| 4 | Địa bàn | Chỉ TP.HCM (địa giới sau 01/7/2025), Quyết định 11/2026/QĐ-UBND. Thủ tục riêng `giai-toa-den-bu-tphcm`, thủ tục cũ giữ nguyên |
| 5 | Hỗ trợ (tạm cư, di chuyển...) | Chưa làm. Chỉ có hỗ trợ đủ suất TĐC tối thiểu và hỗ trợ tự lo chỗ ở |
| 6 | Danh sách nhiều hộ | Không. Mỗi quyết định một hộ |

### 8.2. Chỗ code khác đề xuất ban đầu

- Bồi thường đất chỉ có một dòng "Đất ở (có giấy chứng nhận)", tỷ lệ 100% (xem mục 3.3).
- Thủ tục mới tách khỏi `giai-toa-den-bu`, dùng lại 7 giấy tờ đầu vào bằng khóa `from`. Vì vậy hồ sơ thủ tục cũ sinh ra giống hệt trước khi có thay đổi này.
- Ngày nộp hồ sơ trong 01/3-31/5/2026, để mọi giấy tờ đầu ra lập sau ngày Quyết định 11/2026 có hiệu lực (06/3/2026).
- Thu hồi một phần: nếu phần đất còn lại dưới 36 m² thì không đủ để ở. Khi đó nhà bị tính bồi thường cả căn, và hộ đủ điều kiện tái định cư nếu không có chỗ ở khác.

### 8.3. Số liệu giả lập cần thay bằng số thật

Tất cả nằm ở đầu `generator/thu_hoi.py`:

| Hằng số | Giá trị đang dùng |
|---|---|
| `BUILD_PRICE` | Đơn giá xây mới 3,2-7,2 triệu/m² sàn theo kết cấu; niên hạn 30-80 năm |
| `MIN_REMAINING_RATE` | Tỷ lệ chất lượng còn lại thấp nhất 20% |
| `YARD_PRICE`, `FENCE_PRICE`, `WELL_PRICE` | Sân 165.000 đ/m², tường rào 720.000 đ/m, giếng 3,5 triệu |
| `MIN_RESIDUAL` | Diện tích còn lại tối thiểu để ở: 36 m² |
| `MIN_APARTMENT`, `MIN_LOT` | Suất TĐC tối thiểu: căn hộ 36 m², nền 50 m² |
| `SELF_ARRANGE_RATE` | Hỗ trợ tự lo chỗ ở: 5% tiền bồi thường đất |
| Giá đất | Phường 30-250 triệu/m², xã 5-40 triệu/m² (ngẫu nhiên) |

Việc tiếp theo:

1. Có mẫu GXN 1131 thật thì sửa schema và template `gxn-1131`.
2. Thêm phần diện tích chênh lệch (bản vẽ lớn hơn giấy chứng nhận). Khi đó GXN quyết định tỷ lệ bồi thường theo mốc 1980/1993.
3. Nhờ chuyên viên duyệt khoảng 20 hồ sơ sinh thử.

## 9. Tài liệu tham chiếu

- [Quy định về bồi thường khi thu hồi đất theo Luật Đất đai 2024](https://xaydungchinhsach.chinhphu.vn/chinh-sach-moi-ve-boi-thuong-thu-hoi-dat-theo-luat-dat-dai-2024-119240227145829751.htm)
- [Toàn văn Nghị định quy định về bồi thường, hỗ trợ, tái định cư](https://xaydungchinhsach.chinhphu.vn/toan-van-nghi-dinh-quy-dinh-ve-boi-thuong-ho-tro-tai-dinh-cu-khi-nha-nuoc-thu-hoi-dat-119240906111916662.htm)
- [7 điểm mới về bồi thường tại TP.HCM theo Quyết định 11/2026/QĐ-UBND](https://thuviennhadat.vn/phap-ly-nha-dat/7-diem-moi-ve-boi-thuong-khi-thu-hoi-dat-tai-tp-hcm-theo-quyet-dinh-11-2026-qd-ubnd-737628.html)
- [TP.HCM thưởng cho trường hợp bàn giao đất bị thu hồi trước quy định](https://plo.vn/tphcm-se-thuong-cho-nhung-truong-hop-ban-giao-dat-bi-thu-hoi-truoc-quy-dinh-post899134.html)
- AIP-005 (trích xuất theo schema), AIP-011 (suy luận thời gian, số học), AIP-027 (đánh giá đầu cuối)
