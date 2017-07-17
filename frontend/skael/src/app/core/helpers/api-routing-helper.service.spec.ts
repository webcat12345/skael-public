import { TestBed, inject } from '@angular/core/testing';

import { ApiRoutingHelperService } from './api-routing-helper.service';

describe('ApiRoutingHelperService', () => {
  beforeEach(() => {
    TestBed.configureTestingModule({
      providers: [ApiRoutingHelperService]
    });
  });

  it('should be created', inject([ApiRoutingHelperService], (service: ApiRoutingHelperService) => {
    expect(service).toBeTruthy();
  }));
});
