import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';

import { MdButtonModule } from '@angular/material';

@NgModule({
  imports: [
    CommonModule,
    MdButtonModule
  ],
  exports: [
    MdButtonModule
  ],
  declarations: []
})
export class MaterialModule { }
