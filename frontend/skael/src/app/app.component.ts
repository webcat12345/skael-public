import { Component } from '@angular/core';
import 'rxjs/add/operator/map';

@Component({
  selector: 'skael-root',
  template: `<router-outlet></router-outlet>`
})
export class AppComponent {

  constructor () {}

}
