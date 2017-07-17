import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';

import { AuthGuard } from './core/auth';

export const routes: Routes = [
  {
    path: 'auth', loadChildren: './pages/auth/auth.module#AuthModule'
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
