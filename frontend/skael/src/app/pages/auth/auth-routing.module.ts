import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';

import { LoginComponent } from './login/login.component';
import { SignupComponent } from './signup/signup.component';
import { AuthComponent } from './auth/auth.component';
import { PilotSigninComponent } from './pilot-signin/pilot-signin.component';
import { PilotSignupComponent } from './pilot-signup/pilot-signup.component';

const routes: Routes = [
  {
    path: 'login', component: LoginComponent
  }, {
    path: 'signup', component: SignupComponent
  }, {
    path: 'auth', component: AuthComponent,
    children: [
      { path: 'signin', component: PilotSigninComponent },
      { path: 'signup', component: PilotSignupComponent },
      { path: '**', redirectTo: 'signin'}
    ]
  }, {
    path: '**',
    redirectTo: 'auth'
  }
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class AuthRoutingModule { }
