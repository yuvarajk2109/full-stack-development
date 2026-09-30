import { Component, inject } from '@angular/core';
import { DecimalPipe } from '@angular/common';
import { Holdings } from '../holdings';

@Component({
  selector: 'app-portfolio-badge',
  imports: [DecimalPipe],
  templateUrl: './portfolio-badge.html',
  styleUrl: './portfolio-badge.css',
})
export class PortfolioBadge {
  private readonly holdingsService = inject(Holdings);

  protected readonly totalValue = this.holdingsService.totalValue;

  constructor() {
    this.holdingsService.holdings.set(
      [
        { ticker: 'ULVR.L', quantity: 1000, price: 42.1 },
        { ticker: 'AZN.L', quantity: 120, price: 108.5 },
      ]
    )
  }
}
