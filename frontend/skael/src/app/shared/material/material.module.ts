import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';

import { MdButtonModule, MdInputModule, MdCheckboxModule, MdProgressBarModule } from '@angular/material';

@NgModule({
  imports: [
    CommonModule,
    MdButtonModule,
    MdInputModule,
    MdCheckboxModule,
    MdProgressBarModule
  ],
  exports: [
    MdButtonModule,
    MdInputModule,
    MdCheckboxModule,
    MdProgressBarModule
  ],
  declarations: []
})
export class MaterialModule { }
