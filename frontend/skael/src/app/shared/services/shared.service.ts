import { Injectable } from '@angular/core';
import { Subject } from 'rxjs/Subject';

@Injectable()
export class SharedService {

  private loadingIsInProgress = new Subject<boolean>();

  loadingIsInProgress$ = this.loadingIsInProgress.asObservable();

  constructor() { }

  isLoading(flag: boolean): void {
    this.loadingIsInProgress.next(flag);
  }

}
