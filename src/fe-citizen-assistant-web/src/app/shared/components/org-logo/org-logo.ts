import { ChangeDetectionStrategy, Component, input } from '@angular/core';

/** Placeholder mark for the unit (initials in a circle). Replace with the official logo file when available. */
@Component({
  selector: 'app-org-logo',
  changeDetection: ChangeDetectionStrategy.OnPush,
  host: { 'aria-hidden': 'true', '[style.--logo-size.px]': 'size()' },
  template: `{{ initials() }}`,
  styles: `
    :host {
      display: inline-grid;
      flex: none;
      place-items: center;
      width: var(--logo-size, 40px);
      height: var(--logo-size, 40px);
      border: 2px solid #fff;
      border-radius: 50%;
      background: var(--color-primary);
      color: #fff;
      font-size: calc(var(--logo-size, 40px) * 0.36);
      font-weight: 700;
      line-height: 1;
    }
  `,
})
export class OrgLogo {
  readonly initials = input.required<string>();
  readonly size = input(40);
}
