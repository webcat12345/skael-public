import { Component } from '@angular/core';
import { SharedService } from './shared/services';

@Component({
  selector: 'skael-root',
  template: `
    <div class="content-loading-ripple" *ngIf="isLoading"></div>
    <router-outlet></router-outlet>
  `
})
export class AppComponent {

  isLoading = false;

  constructor (
    private sharedService: SharedService
  ) {
    this.sharedService.loadingIsInProgress$.subscribe(flag => {
      this.isLoading = flag;
    })
  }

}
