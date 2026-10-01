export interface Organization {
  name: string;
  parent: string;
  city: string;
  initials: string;
  assistantName: string;
  serviceDesk: string;
  address: string;
  hotline: string;
  email: string;
  workingHours: string;
}

/**
 * Unit operating the assistant. Single place to change names and contact details.
 * Empty strings are hidden in the UI; fill them with the unit's official information.
 */
export const ORGANIZATION: Organization = {
  /** Department name, shown as the main title. */
  name: 'Phòng Kinh tế, Hạ tầng và Đô thị',
  /** Parent authority, shown above the department name. */
  parent: 'UBND phường Bình Đông',
  city: 'TP. Hồ Chí Minh',
  /** Short label for the logo mark. */
  initials: 'BĐ',
  assistantName: 'Trợ lý hỏi đáp bồi thường, giải tỏa',
  /** Where citizens submit dossiers in person. */
  serviceDesk: 'Bộ phận Một cửa UBND phường Bình Đông',
  address: '',
  hotline: '',
  email: '',
  workingHours: 'Thứ Hai đến Thứ Sáu, sáng 7:30 – 11:30, chiều 13:00 – 17:00',
};
