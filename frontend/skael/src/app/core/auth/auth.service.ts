import { Injectable } from '@angular/core';
import { environment } from 'environments/environment';

import { LocalStorageService } from 'angular-2-local-storage';
import { CookieService } from 'ngx-cookie';
import { ApiRoutingHelperService, HttpHelperService } from 'app/core/helpers';

import { Auth } from 'app/core/models';

@Injectable()
export class AuthService {

  constructor(
    private apiRoutingHelper: ApiRoutingHelperService,
    private http: HttpHelperService,
    private localStorageService: LocalStorageService,
    private cookieService: CookieService,
  ) { }

  /***
   * check if authentication info is exists
   * @returns {boolean}
   */
  isLoggedIn(): boolean {
    if (this.cookieService.get(environment.cookie.storage)) {
      return !!this.localStorageService.get(environment.localStorage.token);
    } else {
      this.localStorageService.remove(environment.localStorage.token);
      return false;
    }
  }

  /***
   * login with username and password
   * @param user
   * @param rememberMe
   * @returns {Observable<R>}
   */
  login(user: Auth, rememberMe = false) {
    return this.http.post(this.apiRoutingHelper.loginUserAPIUrl(), user).map(res => {
      this.localStorageService.set(environment.localStorage.token, res.access_token);
      this.setCookie(rememberMe);
      return {success: true};
    });
  }

  /***
   * set authentication cookie
   * @param rememberMe
   */
  private setCookie(rememberMe: boolean): void {
    if (rememberMe) {
      const now = new Date();
      const expireDate = now.setDate(now.getDate() + environment.cookie.life);
      this.cookieService.put(environment.cookie.storage, environment.cookie.value, {expires: new Date(expireDate).toUTCString()});
    } else {
      this.cookieService.put(environment.cookie.storage, environment.cookie.value);
    }
  }

}
