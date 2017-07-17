import { BrowserModule } from '@angular/platform-browser';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { NgModule } from '@angular/core';
import { HttpModule } from '@angular/http';

import { environment } from 'environments/environment';
import { LocalStorageModule } from 'angular-2-local-storage';
import { CookieModule } from 'ngx-cookie';
import 'hammerjs';

import { AppRoutingModule } from './app.routing';

import { AppComponent } from './app.component';

import { HttpHelperService, ApiRoutingHelperService } from './core/helpers'

@NgModule({
  declarations: [
    AppComponent
  ],
  imports: [
    BrowserModule,
    HttpModule,
    CookieModule.forRoot(),
    BrowserAnimationsModule,
    LocalStorageModule.withConfig({prefix: environment.localStorage.prefix, storageType: 'localStorage'}),
    AppRoutingModule
  ],
  providers: [HttpHelperService, ApiRoutingHelperService],
  bootstrap: [AppComponent]
})
export class AppModule { }
