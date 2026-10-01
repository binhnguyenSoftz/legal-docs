import { ChangeDetectionStrategy, Component, computed, input, output } from '@angular/core';
import { MatMenuModule } from '@angular/material/menu';
import { MatTooltipModule } from '@angular/material/tooltip';
import { Icon } from '../icon/icon';
import { OrgLogo } from '../org-logo/org-logo';

export interface NavLink {
  label: string;
  href: string;
  icon: string;
  active?: boolean;
}

export interface CurrentUser {
  fullName: string;
  identityLevel: string;
}

export interface OrganizationInfo {
  name: string;
  parent: string;
  initials: string;
}

export type SystemStatus = 'online' | 'degraded' | 'offline';

const STATUS_LABELS: Record<SystemStatus, string> = {
  online: 'Hệ thống đang hoạt động',
  degraded: 'Hệ thống đang chậm',
  offline: 'Mất kết nối',
};

@Component({
  selector: 'app-government-header',
  imports: [Icon, OrgLogo, MatMenuModule, MatTooltipModule],
  changeDetection: ChangeDetectionStrategy.OnPush,
  templateUrl: './government-header.html',
  styleUrl: './government-header.scss',
})
export class GovernmentHeader {
  readonly organization = input.required<OrganizationInfo>();
  readonly user = input.required<CurrentUser>();
  readonly status = input<SystemStatus>('online');
  readonly navLinks = input<NavLink[]>([]);
  readonly menuToggle = output<void>();

  protected readonly statusLabel = computed(() => STATUS_LABELS[this.status()]);
  protected readonly initials = computed(() => {
    const parts = this.user().fullName.trim().split(/\s+/);
    return ((parts.at(-2)?.[0] ?? '') + (parts.at(-1)?.[0] ?? '')).toUpperCase();
  });
}
