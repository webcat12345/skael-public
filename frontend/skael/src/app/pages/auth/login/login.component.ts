import { Component, OnInit } from '@angular/core';
import { AuthService } from 'app/core/auth';

@Component({
  selector: 'skael-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.scss']
})
export class LoginComponent implements OnInit {

  constructor(
    private authService: AuthService
  ) { }

  ngOnInit() {
    this.getAPIStatus().subscribe(res => {
      console.log(res);
    });
  }

  getAPIStatus(): void {

  }
}
