import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';

import { MaterialModule } from 'app/shared/material/material.module'

import { LoginComponent } from './login/login.component';
import { SignupComponent } from './signup/signup.component';
import { AuthComponent } from './auth/auth.component';
import { PilotSigninComponent } from './pilot-signin/pilot-signin.component';
import { PilotSignupComponent } from './pilot-signup/pilot-signup.component';

import { AuthRoutingModule } from './auth-routing.module';

import { AuthService } from 'app/core/auth';

@NgModule({
  imports: [
    CommonModule,
    FormsModule,
    MaterialModule,
    AuthRoutingModule
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
  ],
  exports: [
    LoginComponent,
    SignupComponent,
    AuthComponent,
    PilotSigninComponent,
    PilotSignupComponent
  ]
})
export class AuthModule { }
