import { Injectable } from '@angular/core';

import { ApiRoutingHelperService, HttpHelperService } from 'app/core/helpers';

@Injectable()
export class AuthService {

  constructor(
    private apiRoutingHelper: ApiRoutingHelperService,
    private http: HttpHelperService
  ) { }

  getUser() {
    const body = {
      'email': 'ritesh.nadhani@skael.com',
      'plaintext_password': 'riteshn',
      'username': 'riteshn'
    };
    return this.http.post(this.apiRoutingHelper.getUserAPIUrl(), body).map(x => x.json());
  }

}
