import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';

import { AuthService } from 'app/core/auth';

@Component({
  selector: 'skael-layout',
  templateUrl: './layout.component.html',
  styleUrls: ['./layout.component.scss']
})
export class LayoutComponent implements OnInit {

  isLoggedIn = false;
  isSignUp = false;

  constructor(
    private authService: AuthService,
    private router: Router
  ) { }

  ngOnInit() {
    this.isLoggedIn = this.authService.isLoggedIn();
  }

  onLoginSucceed(): void {
    this.isLoggedIn = this.authService.isLoggedIn();
  }

  onLogout(): void {
    this.authService.logout().subscribe(res => {
      this.isLoggedIn = false;
    });
  }

  onToggleForm(flag: boolean): void {
    this.isSignUp = flag;
  }

}
