import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { PilotSigninComponent } from './pilot-signin.component';

describe('PilotSigninComponent', () => {
  let component: PilotSigninComponent;
  let fixture: ComponentFixture<PilotSigninComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ PilotSigninComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(PilotSigninComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should be created', () => {
    expect(component).toBeTruthy();
  });
});
