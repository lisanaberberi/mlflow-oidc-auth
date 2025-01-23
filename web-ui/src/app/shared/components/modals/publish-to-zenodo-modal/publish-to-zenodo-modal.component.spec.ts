import { ComponentFixture, TestBed } from '@angular/core/testing';

import { PublishToZenodoModalComponent } from './publish-to-zenodo-modal.component';

describe('PublishToZenodoModalComponent', () => {
  let component: PublishToZenodoModalComponent;
  let fixture: ComponentFixture<PublishToZenodoModalComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ PublishToZenodoModalComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(PublishToZenodoModalComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
