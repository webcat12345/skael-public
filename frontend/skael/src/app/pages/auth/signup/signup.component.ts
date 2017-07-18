import { Component, OnInit } from '@angular/core';

import { AuthService } from 'app/core/auth';

import { SignupInfo, Error } from 'app/core/models';

@Component({
  selector: 'skael-signup',
  templateUrl: './signup.component.html',
  styleUrls: ['./signup.component.scss']
})
export class SignupComponent implements OnInit {

  isLoading = false;
  error: Error = new Error();

  user: SignupInfo = new SignupInfo();

  constructor(
    private authService: AuthService
  ) { }

  ngOnInit() {
  }

  signup(): void {
    this.isLoading = true;
    this.error.isError = false;
    this.authService.signup(this.user).subscribe((res) => {
      this.isLoading = false;
    }, (err) => {
      this.isLoading = false;
      this.error.isError = true;
      this.error.message = err;
    })
  }

}
