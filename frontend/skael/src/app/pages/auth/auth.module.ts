import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';

import { AuthRoutingModule } from './auth-routing.module';
import { MaterialModule } from 'app/shared/material/material.module'

import { LoginComponent } from './login/login.component';
import { SignupComponent } from './signup/signup.component';

@NgModule({
  imports: [
    CommonModule,
    AuthRoutingModule,
    MaterialModule
  ],
  declarations: [LoginComponent, SignupComponent]
})
export class AuthModule { }
