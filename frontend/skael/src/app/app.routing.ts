import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';

import { LoginComponent, SignupComponent, AuthComponent, VerifyComponent } from './pages/auth';
import { LayoutComponent } from './pages/layout';

export const routes: Routes = [
  {
    path: 'login', component: AuthComponent,
    children: [{ path: '', component: LoginComponent }]
  }, {
    path: 'signup', component: AuthComponent,
    children: [
      { path: '', component: SignupComponent },
      { path: 'verify/:token', component: VerifyComponent}
    ]
  }, {
    path: '', component: LayoutComponent
  }, {
    path: '**', redirectTo: '', pathMatch: 'full'
  }
];

@NgModule({
  imports: [ RouterModule.forRoot(routes)],
  exports: [ RouterModule ]
})
export class AppRoutingModule {}
