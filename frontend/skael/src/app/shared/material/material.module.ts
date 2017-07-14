import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';

import { MdButtonModule, MdInputModule } from '@angular/material';

@NgModule({
  imports: [
    CommonModule,
    MdButtonModule,
    MdInputModule
  ],
  exports: [
    MdButtonModule,
    MdInputModule
  ],
  declarations: []
})
export class MaterialModule { }
