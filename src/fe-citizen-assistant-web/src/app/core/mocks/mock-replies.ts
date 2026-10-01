import { AssistantReply, SuggestionGroup } from '../models/chat.models';
import { PROCEDURES, SOURCES } from './mock-sources';

export interface MockIntent {
  /**
   * Lowercased, diacritic-free keywords, matched on whole syllables.
   * Intents are tried in order and the first match wins, so specific intents come first.
   */
  keywords: string[];
  reply: AssistantReply;
}

/** Flagship answer: documents to prepare, including when the registered owner has died. */
export const DOSSIER_REPLY: AssistantReply = {
  status: 'complete',
  title: 'Hồ sơ nhận bồi thường khi người đứng tên đã mất',
  blocks: [
    {
      type: 'paragraph',
      text: 'Khi người đứng tên nhà đất đã mất, **những người thừa kế** cử một người đại diện làm việc với phường và nhận tiền bồi thường. Hồ sơ cần chứng minh được **quyền sử dụng đất**, **nguồn gốc, thời điểm sử dụng đất** và **quan hệ thừa kế** [^1].',
    },
    { type: 'heading', text: 'Giấy tờ cần chuẩn bị' },
    {
      type: 'table',
      headers: ['Giấy tờ', 'Dùng để'],
      rows: [
        ['**Căn cước** của người đại diện', 'Xác định người nhận tiền. CMND 9 số đã hết giá trị từ 01/01/2025'],
        ['**Giấy chứng tử** hoặc **trích lục khai tử**', 'Chứng minh người đứng tên đã mất'],
        ['**Giấy chứng nhận** quyền sử dụng đất, quyền sở hữu nhà', 'Chứng minh quyền sử dụng và diện tích được công nhận'],
        ['**Bản vẽ hiện trạng**', 'Diện tích đo thực tế, đối chiếu với giấy chứng nhận'],
        ['**Tờ đăng ký nhà đất**, **giấy sang đất** (nếu có)', 'Chứng minh nguồn gốc và thời điểm bắt đầu sử dụng đất'],
        ['**Sổ hộ khẩu** cũ hoặc **giấy xác nhận thông tin cư trú**', 'Xác định nhân khẩu của hộ, căn cứ xét hỗ trợ và tái định cư'],
      ],
    },
    {
      type: 'callout',
      tone: 'warning',
      title: 'Thông tin phải khớp giữa các giấy tờ',
      text: 'Họ tên, năm sinh người đứng tên, số thửa, địa chỉ và diện tích phải **giống nhau** trên giấy chứng tử, giấy chứng nhận, bản vẽ và sổ hộ khẩu. Nếu có chỗ lệch (sai một chữ, lệch năm sinh), hồ sơ sẽ bị yêu cầu bổ sung, vì vậy nên kiểm tra trước khi nộp.',
    },
    { type: 'heading', text: 'Các bước thực hiện' },
    {
      type: 'list',
      ordered: true,
      items: [
        'Các đồng thừa kế thống nhất **người đại diện**, lập văn bản thỏa thuận có chữ ký của các thành viên.',
        'Mang bản chính và bản sao giấy tờ đến **Bộ phận Một cửa UBND phường Bình Đông** để đối chiếu.',
        'Phối hợp với tổ công tác khi **kiểm đếm** nhà, đất, tài sản trên đất.',
        'Xem **phương án bồi thường** được niêm yết công khai, góp ý nếu thấy chưa đúng.',
        'Nhận tiền theo quyết định phê duyệt và **bàn giao mặt bằng** đúng thời hạn.',
      ],
    },
    { type: 'procedure', procedure: PROCEDURES.boiThuong },
  ],
  sources: [SOURCES.luatDatDai, SOURCES.nghiDinh88, SOURCES.nghiDinh151],
  suggestions: [
    { id: 's-hs-1', text: 'Tiền bồi thường đất được tính như thế nào?' },
    { id: 's-hs-2', text: 'Mua đất bằng giấy tay có được bồi thường không?' },
    { id: 's-hs-3', text: 'Bàn giao mặt bằng sớm được thưởng bao nhiêu?' },
  ],
};

export const CALCULATION_REPLY: AssistantReply = {
  status: 'complete',
  title: 'Cách tính tiền bồi thường',
  blocks: [
    {
      type: 'paragraph',
      text: 'Tiền bồi thường gồm các khoản chính: **bồi thường về đất**, **bồi thường nhà và công trình**, các **khoản hỗ trợ** và **tiền thưởng** nếu bàn giao mặt bằng đúng hạn [^1]. Số tiền cụ thể của từng hộ nằm trong **bảng chiết tính** kèm phương án được phê duyệt.',
    },
    { type: 'heading', text: 'Bồi thường về đất' },
    {
      type: 'list',
      ordered: false,
      items: [
        'Phần diện tích **có trong giấy chứng nhận**: diện tích thu hồi × giá đất cụ thể do Thành phố quyết định.',
        'Phần **chênh lệch** khi đo thực tế lớn hơn giấy chứng nhận: được xét theo **thời điểm bắt đầu sử dụng đất** (trước 18/12/1980, từ 1980 đến 15/10/1993, hoặc từ 15/10/1993) và phải có xác nhận của UBND phường [^2].',
      ],
    },
    {
      type: 'table',
      caption: 'Ví dụ minh họa',
      headers: ['Nội dung', 'Số liệu'],
      rows: [
        ['Diện tích thu hồi (nằm trong giấy chứng nhận)', '68,5 m²'],
        ['Giá đất cụ thể', '52.000.000 đ/m²'],
        ['Tiền bồi thường đất', '68,5 × 52.000.000 = **3.562.000.000 đ**'],
      ],
    },
    { type: 'heading', text: 'Bồi thường nhà, công trình' },
    {
      type: 'paragraph',
      text: 'Tính theo **giá trị hiện có** của nhà (giá xây mới × tỷ lệ chất lượng còn lại). Tại TP.HCM, mức bồi thường nhà ở ==không thấp hơn 60% giá trị xây mới==, nên nhà cũ cũng được bù lên mức này [^3].',
    },
    {
      type: 'callout',
      tone: 'info',
      title: 'Tự kiểm tra bảng chiết tính',
      text: 'Ở mỗi dòng, **thành tiền = diện tích × đơn giá × tỷ lệ**. Tổng cộng bằng số phải khớp tổng bằng chữ. Nếu thấy sai, bạn góp ý ngay trong thời gian niêm yết phương án.',
    },
  ],
  sources: [SOURCES.luatDatDai, SOURCES.nghiDinh88, SOURCES.qd11Hcm],
  suggestions: [
    { id: 's-tt-1', text: 'Bàn giao mặt bằng sớm được thưởng bao nhiêu?' },
    { id: 's-tt-2', text: 'Không đồng ý với mức bồi thường thì khiếu nại ở đâu?' },
  ],
};

export const MOCK_INTENTS: MockIntent[] = [
  {
    keywords: ['tam cu', 'thue nha', 'o tam'],
    reply: {
      status: 'no-official-source',
      title: 'Hỗ trợ tạm cư',
      blocks: [
        {
          type: 'paragraph',
          text: 'Theo thông tin tham khảo, hộ phải di chuyển chỗ ở mà chưa được bố trí tái định cư ngay có thể được **hỗ trợ tiền thuê nhà** trong thời gian chờ. Mức hỗ trợ cụ thể theo tháng và theo nhân khẩu do Thành phố quy định và ghi trong phương án của từng dự án.',
        },
      ],
      sources: [SOURCES.forumPost],
      suggestions: [{ id: 's-tc-1', text: 'Điều kiện để được tái định cư là gì?' }],
    },
  },
  {
    keywords: ['tien thuong', 'duoc thuong', 'khen thuong', 'ban giao mat bang', 'ban giao som', 'ban giao truoc'],
    reply: {
      status: 'complete',
      title: 'Thưởng bàn giao mặt bằng',
      blocks: [
        {
          type: 'paragraph',
          text: 'Hộ **bàn giao mặt bằng đúng hoặc trước thời hạn** được UBND phường ra quyết định thưởng. Bàn giao trễ hạn thì **không được thưởng** [^1].',
        },
        {
          type: 'table',
          headers: ['Trường hợp', 'Mức thưởng tối đa'],
          rows: [
            ['Thu hồi **toàn bộ** thửa đất', 'Bằng tiền bồi thường đất, tối đa **50.000.000 đ**'],
            ['Thu hồi **một phần** thửa đất', '50% tiền bồi thường đất, tối đa **25.000.000 đ**'],
          ],
        },
        {
          type: 'callout',
          tone: 'success',
          title: 'Lưu ý',
          text: 'Ngày bàn giao được tính theo **biên bản bàn giao mặt bằng**. Bạn nên giữ bản sao biên bản này.',
        },
      ],
      sources: [SOURCES.qd11Hcm],
      suggestions: [{ id: 's-th-1', text: 'Khi nào được nhận tiền bồi thường?' }],
    },
  },
  {
    keywords: ['tai dinh cu', 'can ho', 'nen dat', 'suat', 'cho o khac', 'tu lo cho o'],
    reply: {
      status: 'complete',
      title: 'Điều kiện tái định cư',
      blocks: [
        {
          type: 'paragraph',
          text: 'Hộ được xét **tái định cư** khi bị thu hồi hết đất ở, hoặc phần còn lại không đủ điều kiện để ở, **và** không còn chỗ ở nào khác trên địa bàn phường [^1].',
        },
        {
          type: 'table',
          caption: 'Các hình thức tái định cư',
          headers: ['Hình thức', 'Nội dung'],
          rows: [
            ['Căn hộ chung cư', 'Nhận căn hộ tại khu tái định cư, nộp thêm hoặc nhận lại phần chênh lệch'],
            ['Nền đất', 'Nhận nền đất, nộp tiền sử dụng đất theo giá tái định cư'],
            ['Tự lo chỗ ở', 'Nhận tiền hỗ trợ để tự lo chỗ ở'],
          ],
        },
        {
          type: 'paragraph',
          text: 'Nếu tiền bồi thường đất **thấp hơn giá trị suất tái định cư tối thiểu**, hộ được hỗ trợ khoản chênh lệch [^2].',
        },
      ],
      sources: [SOURCES.nghiDinh88, SOURCES.qd11Hcm],
      suggestions: [
        { id: 's-tdc-1', text: 'Chưa có nhà tái định cư thì được hỗ trợ tạm cư không?' },
        { id: 's-tdc-2', text: 'Hồ sơ nhận bồi thường cần những giấy tờ gì?' },
      ],
    },
  },
  {
    keywords: ['khieu nai', 'khong dong y', 'kien nghi', 'khoi kien', 'thac mac'],
    reply: {
      status: 'complete',
      title: 'Khiếu nại về bồi thường',
      blocks: [
        {
          type: 'paragraph',
          text: 'Nếu không đồng ý với quyết định thu hồi đất hoặc phương án bồi thường, bạn có quyền **khiếu nại** đến người đã ban hành quyết định, tức **Chủ tịch UBND phường Bình Đông**, hoặc khởi kiện tại Tòa án [^1].',
        },
        {
          type: 'list',
          ordered: true,
          items: [
            'Trong thời gian **niêm yết phương án**, góp ý trực tiếp để được điều chỉnh sớm.',
            'Sau khi có quyết định, gửi **đơn khiếu nại** trong thời hạn ==90 ngày== kể từ ngày nhận quyết định.',
            'Đơn ghi rõ nội dung không đồng ý, kèm bảng chiết tính và giấy tờ chứng minh.',
          ],
        },
        {
          type: 'callout',
          tone: 'info',
          title: 'Trong thời gian khiếu nại',
          text: 'Việc khiếu nại không làm dừng việc thu hồi đất. Bạn vẫn cần phối hợp kiểm đếm và bàn giao mặt bằng theo quyết định.',
        },
      ],
      sources: [SOURCES.luatKhieuNai, SOURCES.luatDatDai],
      suggestions: [{ id: 's-kn-1', text: 'Tiền bồi thường đất được tính như thế nào?' }],
    },
  },
  {
    keywords: ['giay tay', 'giay sang', 'giay viet tay', 'chua co so'],
    reply: {
      status: 'complete',
      title: 'Đất mua bằng giấy tay',
      blocks: [
        {
          type: 'paragraph',
          text: 'Đất mua bằng **giấy tay** (giấy sang đất), chưa có giấy chứng nhận, **vẫn có thể được bồi thường** nếu đủ điều kiện: sử dụng ổn định, không tranh chấp và được **UBND phường xác nhận** nguồn gốc, thời điểm bắt đầu sử dụng [^1].',
        },
        {
          type: 'list',
          ordered: false,
          items: [
            'Giữ **bản gốc giấy sang đất**, kể cả giấy viết tay, cũ, mờ chữ.',
            'Chuẩn bị giấy tờ chứng minh đã ở, đã sử dụng đất từ lâu: tờ đăng ký nhà đất, biên lai thuế, hóa đơn điện nước.',
            'Thời điểm bắt đầu sử dụng (trước 1980, 1980–1993 hay sau 15/10/1993) ảnh hưởng đến **mức bồi thường**.',
          ],
        },
      ],
      sources: [SOURCES.luatDatDai, SOURCES.nghiDinh88],
      suggestions: [{ id: 's-gt-1', text: 'Hồ sơ nhận bồi thường cần những giấy tờ gì?' }],
    },
  },
  {
    keywords: ['khong phep', 'khong co giay phep', 'trai phep', 'xay them'],
    reply: {
      status: 'complete',
      title: 'Nhà xây không phép',
      blocks: [
        {
          type: 'paragraph',
          text: 'Nhà, công trình xây **sau khi đã có thông báo thu hồi đất** thì **không được bồi thường**. Với nhà xây không phép trước thời điểm đó, phường xem xét từng trường hợp theo thời điểm xây dựng để **bồi thường hoặc hỗ trợ** [^1].',
        },
        {
          type: 'callout',
          tone: 'warning',
          title: 'Không xây thêm sau thông báo thu hồi',
          text: 'Phần xây thêm, sửa chữa mở rộng sau khi có thông báo thu hồi đất sẽ không được tính vào bảng chiết tính.',
        },
      ],
      sources: [SOURCES.luatDatDai],
      suggestions: [{ id: 's-kp-1', text: 'Tiền bồi thường nhà được tính như thế nào?' }],
    },
  },
  {
    keywords: ['da mat', 'qua doi', 'thua ke', 'giay to', 'chuan bi', 'can gi'],
    reply: DOSSIER_REPLY,
  },
  {
    keywords: ['tra cuu', 'tinh trang', 'chi tra', 'nhan tien', 'khi nao', 'tien do', 'lich'],
    reply: {
      status: 'complete',
      title: 'Tiến độ chi trả bồi thường',
      blocks: [
        {
          type: 'paragraph',
          text: 'Tiền bồi thường được chi trả sau khi **phương án được phê duyệt**. Lịch chi trả cụ thể được phường **thông báo bằng văn bản** đến từng hộ và niêm yết tại trụ sở UBND phường [^1].',
        },
        {
          type: 'table',
          caption: 'Các bước thường gặp',
          headers: ['Bước', 'Bạn cần làm'],
          rows: [
            ['Thông báo thu hồi đất', 'Theo dõi thông báo, chuẩn bị hồ sơ'],
            ['Kiểm đếm', 'Có mặt khi tổ công tác đo đạc, kiểm đếm'],
            ['Niêm yết phương án', 'Kiểm tra bảng chiết tính, góp ý nếu sai'],
            ['Phê duyệt và chi trả', 'Nhận tiền theo lịch được thông báo'],
            ['Bàn giao mặt bằng', 'Bàn giao đúng hạn để được thưởng'],
          ],
        },
      ],
      sources: [SOURCES.nghiDinh151, SOURCES.dvcHcm],
      suggestions: [{ id: 's-cp-1', text: 'Bàn giao mặt bằng sớm được thưởng bao nhiêu?' }],
    },
  },
  {
    keywords: ['tinh', 'gia dat', 'bao nhieu', 'muc boi thuong', 'dien tich', 'cong trinh', 'chiet tinh'],
    reply: CALCULATION_REPLY,
  },
  {
    // Recognised topics outside land-recovery compensation: point to the right desk.
    keywords: [
      'khai sinh', 'ket hon', 'khai tu', 'can cuoc', 'thuong tru', 'tam tru',
      'ho kinh doanh', 'giay phep xay dung', 'sua chua', 'den duong', 'via he',
    ],
    reply: {
      status: 'complete',
      title: 'Ngoài phạm vi hỗ trợ',
      blocks: [
        {
          type: 'callout',
          tone: 'info',
          title: 'Trợ lý chỉ hỗ trợ về bồi thường, giải phóng mặt bằng',
          text: 'Trợ lý này chỉ trả lời các câu hỏi về **bồi thường, hỗ trợ, tái định cư khi Nhà nước thu hồi đất** trên địa bàn phường Bình Đông.',
        },
        {
          type: 'paragraph',
          text: 'Với thủ tục khác, bạn vui lòng liên hệ **Bộ phận Một cửa UBND phường Bình Đông** để được hướng dẫn.',
        },
      ],
      sources: [],
      suggestions: [
        { id: 's-oos-1', text: 'Hồ sơ nhận bồi thường cần những giấy tờ gì?' },
        { id: 's-oos-2', text: 'Tiền bồi thường đất được tính như thế nào?' },
      ],
    },
  },
  {
    keywords: ['boi thuong', 'den bu', 'giai toa', 'thu hoi', 'giai phong mat bang'],
    reply: {
      status: 'complete',
      title: 'Quy trình bồi thường, giải tỏa',
      blocks: [
        {
          type: 'paragraph',
          text: 'Khi Nhà nước thu hồi đất để thực hiện dự án, **UBND phường** ra quyết định thu hồi và phê duyệt phương án bồi thường, hỗ trợ, tái định cư [^1]. Quy trình gồm các bước:',
        },
        {
          type: 'list',
          ordered: true,
          items: [
            '**Thông báo thu hồi đất** gửi đến từng hộ.',
            '**Kiểm đếm** nhà, đất, tài sản trên đất.',
            '**Lập và niêm yết phương án** bồi thường để người dân góp ý.',
            '**Phê duyệt phương án**, ban hành quyết định thu hồi đất.',
            '**Chi trả** tiền bồi thường, bố trí tái định cư.',
            '**Bàn giao mặt bằng**.',
          ],
        },
      ],
      sources: [SOURCES.nghiDinh151, SOURCES.luatDatDai],
      suggestions: [
        { id: 's-qt-1', text: 'Hồ sơ nhận bồi thường cần những giấy tờ gì?' },
        { id: 's-qt-2', text: 'Tiền bồi thường đất được tính như thế nào?' },
      ],
    },
  },
];

export const NO_RESULT_REPLY: AssistantReply = {
  status: 'no-result',
  blocks: [],
  sources: [],
  suggestions: [
    { id: 's-nr-1', text: 'Hồ sơ nhận bồi thường cần những giấy tờ gì?' },
    { id: 's-nr-2', text: 'Tiền bồi thường đất được tính như thế nào?' },
  ],
};

export const SUGGESTION_GROUPS: SuggestionGroup[] = [
  {
    category: 'dossier',
    title: 'Hồ sơ cần chuẩn bị',
    description: 'Giấy tờ nhà đất, người thừa kế',
    icon: 'folder',
    question: { id: 'g-1', category: 'dossier', text: 'Hồ sơ nhận bồi thường cần những giấy tờ gì?' },
  },
  {
    category: 'calculation',
    title: 'Cách tính tiền bồi thường',
    description: 'Đất, nhà, công trình, tiền thưởng',
    icon: 'wallet',
    question: { id: 'g-2', category: 'calculation', text: 'Tiền bồi thường đất được tính như thế nào?' },
  },
  {
    category: 'resettlement',
    title: 'Tái định cư, hỗ trợ',
    description: 'Căn hộ, nền đất, tự lo chỗ ở',
    icon: 'home',
    question: { id: 'g-3', category: 'resettlement', text: 'Điều kiện để được tái định cư là gì?' },
  },
  {
    category: 'payment',
    title: 'Chi trả, khiếu nại',
    description: 'Lịch nhận tiền, góp ý, khiếu nại',
    icon: 'scale',
    question: { id: 'g-4', category: 'payment', text: 'Khi nào được nhận tiền bồi thường?' },
  },
];

export const POPULAR_QUESTIONS = [
  { id: 'p-1', text: 'Người đứng tên sổ đã mất thì ai nhận tiền bồi thường?' },
  { id: 'p-2', text: 'Mua đất bằng giấy tay có được bồi thường không?' },
  { id: 'p-3', text: 'Bàn giao mặt bằng sớm được thưởng bao nhiêu?' },
];
