import { ComponentFixture, TestBed } from '@angular/core/testing';

import { PredictionInterfaceComponent } from './prediction-interface';

describe('PredictionInterface', () => {
  let component: PredictionInterfaceComponent;
  let fixture: ComponentFixture<PredictionInterfaceComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [PredictionInterfaceComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(PredictionInterfaceComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
