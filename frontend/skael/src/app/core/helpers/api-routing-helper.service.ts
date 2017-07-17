import { Injectable } from '@angular/core';
import { environment } from 'environments/environment';

@Injectable()
export class ApiRoutingHelperService {

  private baseUrl = environment.baseAPIUrl;

  constructor() { }

  userAPIUrl(): string {
    return this.baseUrl + 'users/';
  }

  authAPIUrl(): string {
    return this.baseUrl + 'auth';
  }

  userAuthAPIUrl(): string {
    return this.baseUrl + 'users/auth'
  }
}
