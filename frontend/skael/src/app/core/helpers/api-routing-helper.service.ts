import { Injectable } from '@angular/core';
import { environment } from 'environments/environment';

@Injectable()
export class ApiRoutingHelperService {

  private baseUrl = environment.baseAPIUrl;

  constructor() { }

  getUserAPIUrl(): string {
    return this.baseUrl + 'users/';
  }

  loginUserAPIUrl(): string {
    return this.baseUrl + 'auth';
  }

}
