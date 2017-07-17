import { Component, OnInit } from '@angular/core';
import { AuthService } from 'app/core/auth';

import { Auth } from 'app/core/models';

class Error {
  public isError: boolean;
  public message: string;
  constructor() {
    this.isError = false;
    this.message = '';
  }
}

@Component({
  selector: 'skael-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.scss']
})
export class LoginComponent implements OnInit {

  user: Auth = new Auth();
  rememberMe = false;
  isLoading = false;
  error: Error = new Error();

  constructor(
    private authService: AuthService
  ) { }

  ngOnInit() {
    this.user.username = 'riteshn';
    this.user.password = 'riteshn';
  }

  login(form): void {
    this.isLoading = true;
    this.error.isError = false;
    this.authService.login(this.user).subscribe(res => {
      console.log(res);
    })
  }
}
