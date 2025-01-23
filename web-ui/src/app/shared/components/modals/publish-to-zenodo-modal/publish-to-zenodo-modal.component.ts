import { Component, Inject } from '@angular/core';
import { MatDialogRef, MAT_DIALOG_DATA } from '@angular/material/dialog';

@Component({
  selector: 'ml-publish-to-zenodo-modal',
  templateUrl: './publish-to-zenodo-modal.component.html',
  styleUrls: ['./publish-to-zenodo-modal.component.scss']
})
export class PublishToZenodoModalComponent {

  constructor(
    public dialogRef: MatDialogRef<PublishToZenodoModalComponent>,
    // @Inject(MAT_DIALOG_DATA) public data: any 
  ) {}

  onPublishToZenodo() {
    // Redirect to Zenodo.org (or perform other actions)
    window.location.href = 'https://zenodo.org/'; 
    this.dialogRef.close(); 
  }

  onCancel() {
    this.dialogRef.close();
  }
}