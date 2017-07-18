import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';

import { AuthService } from 'app/core/auth';

@Component({
  selector: 'skael-main',
  templateUrl: './main.component.html',
  styleUrls: ['./main.component.scss']
})
export class MainComponent implements OnInit {

  constructor(
    private authService: AuthService,
    private router: Router
  ) { }

  ngOnInit() {
  }

  onLogout(): void {
    this.router.navigate(['/login']);
    this.authService.logout().subscribe(res => {
      if (res.success) {
      }
    });
  }

  onClickAPITest(): void {
    this.authService.getUserInfo('c2fca35d-0e41-4c62-944a-114cd7365e1c').subscribe(res => {
      console.log(res);
    });
  }
}
