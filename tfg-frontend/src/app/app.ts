import { Component } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { PredictionInterfaceComponent } from './components/prediction-interface/prediction-interface';


@Component({
  selector: 'app-root',
  standalone: true,
  imports: [RouterOutlet,  PredictionInterfaceComponent],
  templateUrl: './app.html',
  styleUrl: './app.scss'
})
export class App {
  protected title = 'tfg-frontend';
}
