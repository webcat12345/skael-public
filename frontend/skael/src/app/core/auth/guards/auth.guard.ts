import { Injectable } from '@angular/core';
import { CanActivate, ActivatedRouteSnapshot, RouterStateSnapshot, Router } from '@angular/router';
import { Observable } from 'rxjs/Observable';

import { AuthService } from 'app/core/auth';

@Injectable()
export class AuthGuard implements CanActivate {

  firstTime = true;

  constructor(
    private authService: AuthService,
    private router: Router
  ) {}

  canActivate(
    next: ActivatedRouteSnapshot,
    state: RouterStateSnapshot): Observable<boolean> | Promise<boolean> | boolean {

    if (this.firstTime) {
      this.firstTime = false;
      return this.authService.checkTokenSession().map((res) => {
        return true;
      }).catch((err) => {
        this.router.navigate(['/login']);
        return Observable.of(false);
      })
    }

    if (!this.authService.isLoggedIn()) {
      this.router.navigate(['/login']);
    }

    return this.authService.isLoggedIn();
  }
}
