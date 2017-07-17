import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { PilotSignupComponent } from './pilot-signup.component';

describe('PilotSignupComponent', () => {
  let component: PilotSignupComponent;
  let fixture: ComponentFixture<PilotSignupComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ PilotSignupComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(PilotSignupComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should be created', () => {
    expect(component).toBeTruthy();
  });
});
