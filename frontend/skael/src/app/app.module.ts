import { BrowserModule } from '@angular/platform-browser';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { NgModule } from '@angular/core';
import { HttpModule } from '@angular/http';
// npm libraries
import { environment } from 'environments/environment';
import { LocalStorageModule } from 'angular-2-local-storage';
import { CookieModule } from 'ngx-cookie';
import 'hammerjs';
// routing module
import { AppRoutingModule } from './app.routing';
// auth module
import { AuthModule } from './pages/auth/auth.module';
// services
import { HttpHelperService, ApiRoutingHelperService } from './core/helpers'
import { AuthGuard, AuthService } from './core/auth';
// app component
import { AppComponent } from './app.component';

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
    AppRoutingModule,
    AuthModule
  ],
  providers: [
    HttpHelperService,
    ApiRoutingHelperService,
    AuthService,
    AuthGuard
  ],
  bootstrap: [AppComponent]
})
export class AppModule { }
