import { BrowserModule } from '@angular/platform-browser';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { NgModule } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { HttpModule } from '@angular/http';
// npm libraries
import { environment } from 'environments/environment';
import { LocalStorageModule } from 'angular-2-local-storage';
import { CookieModule } from 'ngx-cookie';
import 'hammerjs';
// routing module
import { AppRoutingModule } from './app.routing';
import { MaterialModule } from './shared/material/material.module';
// services
import { HttpHelperService, ApiRoutingHelperService } from './core/helpers'
import { AuthGuard, AuthService } from './core/auth';
// app component
import { AppComponent } from './app.component';
import { LoginComponent, SignupComponent, AuthComponent } from './pages/auth';
import { LayoutComponent, NavbarComponent } from './pages/layout';

@NgModule({
  declarations: [
    AppComponent,
    LoginComponent,
    SignupComponent,
    AuthComponent,
    LayoutComponent,
    NavbarComponent
  ],
  imports: [
    BrowserModule,
    HttpModule,
    FormsModule,
    MaterialModule,
    CookieModule.forRoot(),
    BrowserAnimationsModule,
    LocalStorageModule.withConfig({prefix: environment.localStorage.prefix, storageType: 'localStorage'}),
    AppRoutingModule
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
