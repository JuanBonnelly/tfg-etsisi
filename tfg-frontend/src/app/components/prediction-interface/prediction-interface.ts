import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';


import { Team, PredictionRequest, PredictionResponse } from '../../models/api.models';
import { ApiService } from '../../services/api';

@Component({
  selector: 'app-prediction-interface',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './prediction-interface.html',
  styleUrl: './prediction-interface.scss'
})

export class PredictionInterfaceComponent implements OnInit {
  teams: Team[] = [];
  predictionResult: PredictionResponse | null = null; 
  selectedHomeTeamName: string | null = null;
  selectedAwayTeamName: string | null = null;
  predictionDate: string = new Date().toISOString().split('T')[0];
  isLoading = false; 
  errorMessage: string | null = null; 

  constructor(private apiService: ApiService) { }

  ngOnInit(): void {
    console.log('Componente inicializado. ');
    this.apiService.getTeams().subscribe({
      next: (data) => {
        this.teams = data;
      },
      error: (err) => {
        console.error('No se pudieron obtener los equipos:', err);

      }
    });
  }
  onSubmit(): void {
    if (!this.selectedHomeTeamName || !this.selectedAwayTeamName) {
      this.errorMessage = 'Por favor, selecciona ambos equipos.';
      return;
    }
    if (this.selectedHomeTeamName === this.selectedAwayTeamName) {
      this.errorMessage = 'El equipo local y el visitante no pueden ser el mismo.';
      return;
    }
    this.isLoading = true;
    this.errorMessage = null;
    this.predictionResult = null;
    const request: PredictionRequest = {
      local_team_name: this.selectedHomeTeamName,
      visitor_team_name: this.selectedAwayTeamName,
      match_date: this.predictionDate
    };

    this.apiService.predictMatch(request).subscribe({
      next: (response) => {
        this.predictionResult = response;
        this.isLoading = false;
      },
      error: (err) => {
        console.error('Error en la predicción:', err);
        this.errorMessage = err.error?.detail || 'Ocurrió un error inesperado al predecir.';
        this.isLoading = false;
      }
    });
  }
}