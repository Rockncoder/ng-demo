import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { CplusplusComponent } from './cplusplus.component';

describe('CplusplusComponent', () => {
  let component: CplusplusComponent;
  let fixture: ComponentFixture<CplusplusComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ CplusplusComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(CplusplusComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
