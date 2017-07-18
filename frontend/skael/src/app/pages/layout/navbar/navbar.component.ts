import { Component, OnInit, Input, EventEmitter, Output } from '@angular/core';
import { Router } from '@angular/router';

import { AuthService } from 'app/core/auth';

@Component({
  selector: 'skael-navbar',
  templateUrl: './navbar.component.html',
  styleUrls: ['./navbar.component.scss']
})
export class NavbarComponent implements OnInit {

  @Output() onToggleForm: EventEmitter<boolean> = new EventEmitter();
  @Output() onLogout: EventEmitter<any> = new EventEmitter();
  @Input() isLoggedIn: boolean;

  isSignUp = false;

  constructor(
    private authService: AuthService,
    private router: Router
  ) { }

  ngOnInit() {
  }

  showSignIn(): void {
    this.isSignUp = false;
    this.onToggleForm.emit(this.isSignUp);
  }

  showSignUp(): void {
    this.isSignUp = true;
    this.onToggleForm.emit(this.isSignUp);
  }

  logout(): void {
    this.onLogout.emit();
  }
}
