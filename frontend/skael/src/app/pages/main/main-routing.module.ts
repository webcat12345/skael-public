import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';

import { ContentComponent } from '.';

const routes: Routes = [
  {
    path: 'content', component: ContentComponent
  }, {
    path: '**', redirectTo: 'content'
  }
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class MainRoutingModule { }
