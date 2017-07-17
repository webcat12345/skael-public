import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';

import { MdButtonModule, MdInputModule, MdCheckboxModule } from '@angular/material';

@NgModule({
  imports: [
    CommonModule,
    MdButtonModule,
    MdInputModule,
    MdCheckboxModule
  ],
  exports: [
    MdButtonModule,
    MdInputModule,
    MdCheckboxModule
  ],
  declarations: []
})
export class MaterialModule { }
