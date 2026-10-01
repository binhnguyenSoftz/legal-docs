import { AdministrativeProcedure, SourceReference } from '../models/chat.models';

/**
 * Demo reference data for land-recovery compensation. Document numbers follow
 * src/data-golden-set-generator/specs/de-xuat-giay-to-boi-thuong.md, where several
 * are still marked [CẦN XÁC NHẬN]. URLs, update dates and excerpts are illustrative
 * and must be checked against the official texts before going live.
 */
export const SOURCES = {
  luatDatDai: {
    id: 'src-luat-dat-dai',
    kind: 'legal-document',
    title: 'Luật Đất đai 2024, Chương VII: Bồi thường, hỗ trợ, tái định cư khi Nhà nước thu hồi đất',
    documentNumber: '31/2024/QH15',
    publisher: 'Cơ sở dữ liệu quốc gia về văn bản pháp luật',
    url: 'https://vbpl.vn',
    domain: 'vbpl.vn',
    updatedAt: '2026-06-30',
    excerpt:
      'Việc bồi thường, hỗ trợ, tái định cư phải bảo đảm dân chủ, khách quan, công bằng, công khai, minh bạch, kịp thời và đúng quy định của pháp luật.',
    official: true,
  },
  nghiDinh88: {
    id: 'src-nd-88',
    kind: 'legal-document',
    title: 'Nghị định 88/2024/NĐ-CP quy định về bồi thường, hỗ trợ, tái định cư khi Nhà nước thu hồi đất',
    documentNumber: '88/2024/NĐ-CP',
    publisher: 'Cổng thông tin điện tử Chính phủ',
    url: 'https://xaydungchinhsach.chinhphu.vn/toan-van-nghi-dinh-quy-dinh-ve-boi-thuong-ho-tro-tai-dinh-cu-khi-nha-nuoc-thu-hoi-dat-119240906111916662.htm',
    domain: 'xaydungchinhsach.chinhphu.vn',
    updatedAt: '2026-05-15',
    official: true,
  },
  nghiDinh151: {
    id: 'src-nd-151',
    kind: 'legal-document',
    title: 'Nghị định 151/2025/NĐ-CP về phân định thẩm quyền của chính quyền địa phương 2 cấp trong lĩnh vực đất đai',
    documentNumber: '151/2025/NĐ-CP',
    publisher: 'Cổng thông tin điện tử Chính phủ',
    url: 'https://vanban.chinhphu.vn',
    domain: 'vanban.chinhphu.vn',
    updatedAt: '2026-07-01',
    excerpt:
      'Từ ngày 01/7/2025, Ủy ban nhân dân cấp xã quyết định thu hồi đất và phê duyệt phương án bồi thường, hỗ trợ, tái định cư theo thẩm quyền.',
    official: true,
  },
  qd11Hcm: {
    id: 'src-qd-11-hcm',
    kind: 'legal-document',
    title: 'Quyết định 11/2026/QĐ-UBND quy định về bồi thường, hỗ trợ, tái định cư trên địa bàn TP.HCM',
    documentNumber: '11/2026/QĐ-UBND',
    publisher: 'UBND Thành phố Hồ Chí Minh',
    url: 'https://hochiminhcity.gov.vn',
    domain: 'hochiminhcity.gov.vn',
    updatedAt: '2026-03-06',
    excerpt:
      'Hộ gia đình, cá nhân bàn giao mặt bằng trước thời hạn được thưởng; mức bồi thường nhà ở không thấp hơn 60% giá trị xây mới.',
    official: true,
  },
  luatKhieuNai: {
    id: 'src-luat-khieu-nai',
    kind: 'legal-document',
    title: 'Luật Khiếu nại 2011',
    documentNumber: '02/2011/QH13',
    publisher: 'Cơ sở dữ liệu quốc gia về văn bản pháp luật',
    url: 'https://vbpl.vn',
    domain: 'vbpl.vn',
    updatedAt: '2026-01-10',
    excerpt:
      'Thời hiệu khiếu nại là 90 ngày, kể từ ngày nhận được quyết định hành chính hoặc biết được quyết định hành chính, hành vi hành chính.',
    official: true,
  },
  dvcHcm: {
    id: 'src-dvc-hcm',
    kind: 'portal',
    title: 'Cổng Dịch vụ công Thành phố Hồ Chí Minh',
    publisher: 'UBND Thành phố Hồ Chí Minh',
    url: 'https://dichvucong.hochiminhcity.gov.vn',
    domain: 'dichvucong.hochiminhcity.gov.vn',
    updatedAt: '2026-09-25',
    official: true,
  },
  forumPost: {
    id: 'src-forum',
    kind: 'guide',
    title: 'Bài viết chia sẻ kinh nghiệm nhận hỗ trợ tạm cư',
    publisher: 'Nguồn không chính thức',
    url: 'https://example.com',
    domain: 'example.com',
    official: false,
  },
} satisfies Record<string, SourceReference>;

export const PROCEDURES = {
  boiThuong: {
    id: 'proc-boi-thuong',
    name: 'Bồi thường, hỗ trợ, tái định cư khi Nhà nước thu hồi đất',
    field: 'Đất đai: bồi thường, giải phóng mặt bằng',
    processingTime: 'Theo kế hoạch thu hồi đất của từng dự án',
    applicant: 'Hộ gia đình, cá nhân có đất bị thu hồi, hoặc người thừa kế',
    serviceLevel: 'in-person',
    fee: 'Không thu phí',
    authority: 'UBND phường Bình Đông',
    requiredDocuments: [
      'Căn cước của người đại diện nhận bồi thường',
      'Giấy chứng nhận quyền sử dụng đất, quyền sở hữu nhà ở',
      'Bản vẽ hiện trạng nhà, đất',
      'Tờ đăng ký nhà đất, giấy sang đất (nếu có)',
      'Sổ hộ khẩu hoặc giấy xác nhận thông tin cư trú',
      'Giấy chứng tử hoặc trích lục khai tử (nếu người đứng tên đã mất)',
    ],
    legalBasis: ['Luật Đất đai 31/2024/QH15, Chương VII', 'Nghị định 88/2024/NĐ-CP', 'Quyết định 11/2026/QĐ-UBND TP.HCM'],
    detailUrl: 'https://dichvucong.hochiminhcity.gov.vn',
  },
} satisfies Record<string, AdministrativeProcedure>;
