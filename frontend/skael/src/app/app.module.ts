import { BrowserModule } from '@angular/platform-browser';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { NgModule } from '@angular/core';
import { HttpModule } from '@angular/http';

import 'hammerjs';

import { AppRoutingModule } from './app.routing';

import { AppComponent } from './app.component';

import { HttpHelperService } from './core/helpers'

@NgModule({
  declarations: [
    AppComponent
  ],
  imports: [
    BrowserModule,
    HttpModule,
    BrowserAnimationsModule,
    AppRoutingModule
  ],
  providers: [HttpHelperService],
  bootstrap: [AppComponent]
})
export class AppModule { }
