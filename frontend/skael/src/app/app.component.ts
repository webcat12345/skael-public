import { Component, OnInit } from '@angular/core';
import { Http, Response } from '@angular/http';
import 'rxjs/add/operator/map';

@Component({
  selector: 'skael-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent implements OnInit{
  title = 'app';
  postgres_version = '';

  constructor (private http: Http) {}

  ngOnInit() {
    // this.http.get("/api/hello").subscribe((res: Response) => {
    //     this.postgres_version = res.json().postgres_version;
    // });
  }
}
