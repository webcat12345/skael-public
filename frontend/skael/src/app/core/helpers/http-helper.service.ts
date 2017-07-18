import { Injectable } from '@angular/core';
import { Http, RequestOptions, Headers, Response, URLSearchParams} from '@angular/http';
import { Observable } from 'rxjs/Observable';
import 'rxjs/Rx';

import { CookieService } from 'ngx-cookie';
import { LocalStorageService } from 'angular-2-local-storage';
import { environment } from 'environments/environment';

@Injectable()
export class HttpHelperService {

  constructor(
    private http: Http,
    private localStorageService: LocalStorageService,
    private cookieService: CookieService
  ) { }

  /***
   * generate request options
   * @param isUrlEncoded
   * @param requiredAuth
   * @param customHeader
   * @param customParam
   * @returns {RequestOptions}
   */
  private generateReqOptions(isUrlEncoded = false, requiredAuth = false, customHeader?: Headers , customParam?: Object): RequestOptions {
    let headers = new Headers({ 'Content-Type': 'application/json' });
    const search = new URLSearchParams();

    if (isUrlEncoded) {
      headers = new Headers({'Content-Type': 'application/x-www-form-urlencoded'});
    }

    if (requiredAuth) {
      const token = this.localStorageService.get(environment.localStorage.token);
      headers.append('Authorization', 'JWT ' + token);
    }

    if (customHeader) {
      customHeader.forEach((value, key) => {
        headers.append(key, value[0]);
      });
    }

    if (customParam) {
      // tslint:disable-next-line:forin
      for (const key in customParam) {
          search.set(key, customParam[key]);
      }
    }

    return new RequestOptions({ headers, search });
  }

  /***
   * http get helper
   * @param url
   * @param query
   * @param requiredAuth
   * @param headers
   * @returns {Observable<Response>}
   */
  get(url: string, query: Object, requiredAuth = false, headers?: Headers): Observable<any> {
    return this.http.get(url, this.generateReqOptions(false, requiredAuth, headers, query));
  }

  /***
   * http post helper
   * @param url
   * @param body
   * @param isUrlEncoded
   * @param requiredAuth
   * @param headers
   * @returns {Observable<R|T>}
   */
  post(url: string, body: any, isUrlEncoded = false, requiredAuth = false, headers?: Headers): Observable<any> {
    if (isUrlEncoded) {
      const urlSearchParams = new URLSearchParams();
      Object.keys(body).forEach(key => {
        urlSearchParams.append(key, body[key]);
      });
      body = urlSearchParams.toString();
    }
    return this.http.post(url, body, this.generateReqOptions(isUrlEncoded, requiredAuth, headers))
      .map(x => x.json())
      .catch(this.handleError);
  }

  /***
   * http delete helper
   * @param url
   * @param isUrlEncoded
   * @param requiredAuth
   * @param headers
   * @returns {Observable<R|T>}
   */
  delete(url: string, isUrlEncoded = false, requiredAuth = false, headers?: Headers): Observable<any> {
    return this.http.delete(url, this.generateReqOptions(isUrlEncoded, requiredAuth, headers))
      .map(x => x.json())
      .catch(this.handleError);
  }

  /***
   * http exception handler
   * @param error
   * @returns {any}
   */
  private handleError (error: Response | any) {
    let errMsg: string;
    if (error instanceof Response) {
      const body = error.json() || '';

      /***
       * ! IMPORTANT SECTION
       * if error is 401 (Unauthorized) then
       * current session should be destoried
       */

      if (error.status === 401) {
        this.localStorageService.remove(environment.localStorage.token);
        this.cookieService.remove(environment.cookie.storage);
      }

      errMsg = body.msg;
    } else {
      errMsg = error.message ? error.message : error.toString();
    }
    return Observable.throw(errMsg);
  }
}
