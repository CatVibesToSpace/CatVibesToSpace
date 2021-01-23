import { Component } from '@angular/core';
import { JobService } from 'src/app/job.service';
import { Job } from './job.model';

import { FormBuilder, FormGroup, Validators } from '@angular/forms';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})



export class AppComponent {
  title = 'catvibes';
  job: Job;

  messageForm: FormGroup;
  submitted = false;
  success = false;

  constructor(private jobService: JobService, private formBuilder: FormBuilder) { 
    this.messageForm = this.formBuilder.group({
      url: ['', Validators.required]
    });
  }

  /**
 * generate groups of 4 random characters
 * @example getUniqueId(1) : 607f
 * @example getUniqueId(2) : 95ca-361a-f8a1-1e73
 */
  getUniqueId(parts: number): string {
    const stringArr = [];
    for(let i = 0; i< parts; i++){
      // tslint:disable-next-line:no-bitwise
      const S4 = (((1 + Math.random()) * 0x10000) | 0).toString(16).substring(1);
      stringArr.push(S4);
    }
    return stringArr.join('-');
  }

  onSubmit() {
    this.submitted = true;

    if (this.messageForm.invalid) {
      return;
    }

    // Add stuff to submit
    this.job = new Job();
    this.job.id = this.getUniqueId(4);
    this.job.bpm = -1;

    this.job.bpm_finished = false;
    this.job.bpm_started = false;
    this.job.download_finished = false;
    this.job.download_started = false;
    this.job.encoding_finished = false;
    this.job.encoding_started = false;

    this.job.youtube_url = this.messageForm.controls.url.value;
    this.job.url = "";

    this.success = true;
    
    this.jobService.createJob(this.job);

    console.log(this.messageForm.controls.url.value);
  }

  vibeClick() {
    console.log('clicked');
  }
}
