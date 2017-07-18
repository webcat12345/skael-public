import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';

import { AuthService } from 'app/core/auth';

@Component({
  selector: 'skael-main',
  templateUrl: './main.component.html',
  styleUrls: ['./main.component.scss']
})
export class MainComponent implements OnInit {

  isLoggedIn = false;

  constructor(
    private authService: AuthService,
    private router: Router
  ) { }

  ngOnInit() {
    this.isLoggedIn = this.authService.isLoggedIn();
  }

  onLogout(): void {
    this.authService.logout().subscribe(res => {
      this.router.navigate(['/login']);
    });
  }
}
