import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';

import { AuthRoutingModule } from './auth-routing.module';
import { MaterialModule } from 'app/shared/material/material.module'

import { LoginComponent } from './login/login.component';
import { SignupComponent } from './signup/signup.component';
import { AuthComponent } from './auth/auth.component';
import { PilotSigninComponent } from './pilot-signin/pilot-signin.component';
import { PilotSignupComponent } from './pilot-signup/pilot-signup.component';

import { AuthService } from 'app/core/auth';

@NgModule({
  imports: [
    CommonModule,
    AuthRoutingModule,
    MaterialModule
  ],
  declarations: [
    LoginComponent,
    SignupComponent,
    AuthComponent,
    PilotSigninComponent,
    PilotSignupComponent
  ],
  providers: [
    AuthService
  ]
})
export class AuthModule { }
