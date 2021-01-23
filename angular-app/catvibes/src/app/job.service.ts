import { Injectable } from '@angular/core';
import { AngularFirestore } from '@angular/fire/firestore';
import { Job } from 'src/app/job.model';

@Injectable({
  providedIn: 'root'
})
export class JobService {

  constructor(private firestore: AngularFirestore) { }

  getJobs() {
    return this.firestore.collection('jobs').snapshotChanges();
  }
  
  createJob(job: Job){

    this.firestore.collection('jobs').doc(job.id).set(JSON.parse(JSON.stringify(job)));

    return this.firestore.collection('jobs').doc(job.id)
    //return this.firestore.collection('jobs').add(JSON.parse(JSON.stringify(job)));
  }


}
