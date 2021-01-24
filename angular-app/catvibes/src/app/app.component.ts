import { Component, OnInit } from '@angular/core';
import { ParticlesConfig } from './particles-config';
import { JobService } from 'src/app/job.service';
import { Job } from './job.model';
import { AngularFirestoreDocument } from '@angular/fire/firestore';

import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { Observable } from 'rxjs';


declare let particlesJS: any; // Required to be properly interpreted by TypeScript

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})


export class AppComponent implements OnInit {
  title = 'catvibes';
  job: Job;

  messageForm: FormGroup;
  submitted = false;
  success = false;

  progress_percent = 0;
  buffer_percent = 0;

  download_wheel = 1;
  bpm_wheel = 1;
  render_wheel = 1;

  download_ready = false;
  download_url = "hailthealmightyoctopus.xyz";

  jobWatcher: Observable<any>;
  constructor(private jobService: JobService, private formBuilder: FormBuilder) { 
    this.messageForm = this.formBuilder.group({
      url: ['', Validators.required]
    });

    this.job = new Job();
    this.job.id = this.getUniqueId(4);
    this.job.bpm = -1;

    this.job.bpm_finished = false;
    this.job.bpm_started = false;
    this.job.download_finished = false;
    this.job.download_started = false;
    this.job.encoding_finished = false;
    this.job.encoding_started = false;
    this.job.url = "";
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
    
    this.job.youtube_url = this.messageForm.controls.url.value;
    

    this.success = true;

    this.jobWatcher = this.jobService.createJob(this.job).valueChanges();

    this.jobWatcher.subscribe(data => {
        this.job.bpm = data.bpm;

        this.job.bpm_finished = data.bpm_finished;
        this.job.bpm_started = data.bpm_started;
        this.job.download_finished = data.download_finished;
        this.job.download_started = data.download_started;
        this.job.encoding_finished = data.encoding_finished;
        this.job.encoding_started = data.encoding_started;

        this.job.youtube_url = this.messageForm.controls.url.value;
        this.job.url = data.url;

        this.progress_percent = 0
        this.buffer_percent = 0

        if (this.job.download_started == true)
        {
          this.buffer_percent += 100/3
          this.download_wheel = 50;
        }
        if (this.job.download_finished == true)
        {
          this.progress_percent += 100/3
          this.download_wheel = 100;
        }
        if (this.job.bpm_started == true)
        {
          this.buffer_percent += 100/3
          this.bpm_wheel = 50;
        }
        if (this.job.bpm_finished == true)
        {
          this.progress_percent += 100/3
          this.bpm_wheel = 100;
        }
        if (this.job.encoding_started == true)
        {
          this.buffer_percent += 100/3
          this.render_wheel = 50;
        }
        if (this.job.encoding_finished == true)
        {
          this.progress_percent += 100/3
          this.render_wheel = 100;
        }

        if (this.progress_percent == 100) {
          this.download_ready = true;
          this.download_url = this.job.url
        }
    })
    console.log(this.messageForm.controls.url.value);

  }

  vibeClick() {
    console.log('clicked');
  }

  public ngOnInit(): void {
    this.invokeParticles();
  }

  public invokeParticles(): void {
    particlesJS('particles-js', ParticlesConfig, function() {});
  }
}
