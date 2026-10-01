import { ChangeDetectionStrategy, Component, computed, input, signal } from '@angular/core';
import { AdministrativeProcedure, ServiceLevel } from '../../../core/models/chat.models';
import { Icon } from '../icon/icon';

const SERVICE_LEVEL_LABELS: Record<ServiceLevel, string> = {
  'full-online': 'Dịch vụ công trực tuyến toàn trình',
  'partial-online': 'Dịch vụ công trực tuyến một phần',
  'in-person': 'Làm việc trực tiếp tại phường',
};

/** Highlighted card for an administrative procedure detected in the answer. */
@Component({
  selector: 'app-procedure-card',
  imports: [Icon],
  changeDetection: ChangeDetectionStrategy.OnPush,
  templateUrl: './procedure-card.html',
  styleUrl: './procedure-card.scss',
})
export class ProcedureCard {
  readonly procedure = input.required<AdministrativeProcedure>();

  protected readonly expanded = signal(false);
  protected readonly serviceLevel = computed(() => SERVICE_LEVEL_LABELS[this.procedure().serviceLevel]);
  protected readonly detailsId = computed(() => `procedure-details-${this.procedure().id}`);
  protected readonly titleId = computed(() => `procedure-title-${this.procedure().id}`);

  protected toggle(): void {
    this.expanded.update((v) => !v);
  }
}
