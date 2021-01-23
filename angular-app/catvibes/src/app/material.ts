import { NgModule } from '@angular/core';
import {MatButtonModule} from '@angular/material/button';
import {MatToolbarModule} from '@angular/material/toolbar';
import {MatIconModule} from '@angular/material/icon';
import {MatCard, MatCardModule} from '@angular/material/card';
import {MatFormFieldModule} from '@angular/material/form-field';
import {MatInputModule} from '@angular/material/input'
import {MatProgressBarModule} from '@angular/material/progress-bar';
import {MatChipsModule} from '@angular/material/chips';
import {MatProgressSpinnerModule} from '@angular/material/progress-spinner';
import {MatGridListModule} from '@angular/material/grid-list';

@NgModule({
    imports: [MatButtonModule, MatToolbarModule, MatIconModule, 
        MatCardModule, MatFormFieldModule, MatInputModule, 
        MatProgressBarModule, MatChipsModule, MatProgressSpinnerModule,
        MatGridListModule],
    exports: [MatButtonModule, MatToolbarModule, MatIconModule, 
        MatCardModule, MatFormFieldModule, MatInputModule,
        MatProgressBarModule, MatChipsModule, MatProgressSpinnerModule,
        MatGridListModule],
})

export class MaterialModule { }