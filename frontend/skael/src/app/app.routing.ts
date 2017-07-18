import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';

import { LoginComponent, SignupComponent } from './pages/auth';

import { AuthGuard } from './core/auth';

export const routes: Routes = [
  {
    path: 'login', component: LoginComponent
  }, {
    path: 'signup', component: SignupComponent
  }, {
    path: 'main', loadChildren: './pages/main/main.module#MainModule', canActivate: [AuthGuard]
  }, {
    path: '**',
    redirectTo: 'main'
  }
];

@NgModule({
  imports: [ RouterModule.forRoot(routes)],
  exports: [ RouterModule ]
})
export class AppRoutingModule {}
