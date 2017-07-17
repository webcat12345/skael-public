import { Component, OnInit } from '@angular/core';
import { Router, NavigationEnd } from '@angular/router';

@Component({
  selector: 'skael-auth',
  templateUrl: './auth.component.html',
  styleUrls: ['./auth.component.scss']
})
export class AuthComponent implements OnInit {

  isLoginPage = true;

  constructor(
    private router: Router
  ) { }

  ngOnInit() {
    this.router.events.subscribe(val => {
      if (this.router.url === '/auth/signup') {
        this.isLoginPage = false;
      } else {
        this.isLoginPage = true;
      }
    })
  }

}
