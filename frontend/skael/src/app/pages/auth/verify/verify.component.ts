import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';

import { AuthService } from 'app/core/auth';
import { SharedService } from 'app/shared/services';

@Component({
  selector: 'skael-verify',
  templateUrl: './verify.component.html',
  styleUrls: ['./verify.component.scss']
})
export class VerifyComponent implements OnInit {

  token = '';
  isSuccess = null;

  constructor(
    private router: Router,
    private activatedRoute: ActivatedRoute,
    private authService: AuthService,
    private sharedService: SharedService
  ) { }

  ngOnInit() {
    this.sharedService.isLoading(true);
    this.activatedRoute.params.subscribe(params => {
      this.token = params['token'];
      this.verifyUser();
    });
  }

  private verifyUser(): void {
    this.authService.verifyUser(this.token).subscribe(res => {
      this.sharedService.isLoading(false);
      this.isSuccess = res['success'];
    })
  }

}
