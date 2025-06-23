import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';

// Importa los modelos que necesitaremos (aunque solo sea para tipado)
import { Team, PredictionRequest, PredictionResponse } from '../../models/api.models';
// Importa el servicio que vamos a usar
import { ApiService } from '../../services/api';

@Component({
  selector: 'app-prediction-interface',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './prediction-interface.html',
  styleUrl: './prediction-interface.scss'
})
// Implementamos la interfaz OnInit para usar el gancho de ciclo de vida ngOnInit
export class PredictionInterfaceComponent implements OnInit {

  // Creamos una propiedad para guardar los equipos
  teams: Team[] = [];
  predictionResult: PredictionResponse | null = null; // Almacenará el resultado de la predicción

   // --- Propiedades para el estado del formulario (vinculadas con ngModel) ---
  selectedHomeTeamName: string | null = null;
  selectedAwayTeamName: string | null = null;
  // Fecha de hoy en formato YYYY-MM-DD para el input de fecha
  predictionDate: string = new Date().toISOString().split('T')[0];

  // --- Propiedades para la Experiencia de Usuario (UX) ---
  isLoading = false; // Para mostrar un spinner o deshabilitar el botón
  errorMessage: string | null = null; // Para mostrar mensajes de error

  // Paso 1: Inyectamos el ApiService en el constructor.
  // Angular se encarga de crear la instancia y pasárnosla.
  constructor(private apiService: ApiService) { }

  // Paso 2: ngOnInit se ejecuta automáticamente una vez cuando el componente se inicializa.
  // Es el lugar perfecto para cargar datos iniciales.
  ngOnInit(): void {
    console.log('Componente inicializado. Llamando a getTeams()...');

    this.apiService.getTeams().subscribe({
      // Esto se ejecuta si la llamada a la API tiene éxito
      next: (data) => {
        this.teams = data;
      },
      // Esto se ejecuta si hay un error en la llamada
      error: (err) => {
        console.error('¡ERROR! No se pudieron obtener los equipos:', err);
        // Aquí podríamos mostrar un mensaje de error al usuario en el futuro
      }
    });
  }
  // --- Método que se ejecuta al enviar el formulario ---
  onSubmit(): void {
    // 1. Validaciones básicas en el frontend
    if (!this.selectedHomeTeamName || !this.selectedAwayTeamName) {
      this.errorMessage = 'Por favor, selecciona ambos equipos.';
      return;
    }
    if (this.selectedHomeTeamName === this.selectedAwayTeamName) {
      this.errorMessage = 'El equipo local y el visitante no pueden ser el mismo.';
      return;
    }

    // 2. Preparar el estado para una nueva petición
    this.isLoading = true;
    this.errorMessage = null;
    this.predictionResult = null;

    // 3. Crear el objeto de la petición para la API
    const request: PredictionRequest = {
      local_team_name: this.selectedHomeTeamName,
      visitor_team_name: this.selectedAwayTeamName,
      match_date: this.predictionDate
    };

    // 4. Llamar al servicio de la API
    this.apiService.predictMatch(request).subscribe({
      next: (response) => {
        // ¡Éxito! Guardamos el resultado y paramos la carga
        this.predictionResult = response;
        this.isLoading = false;
      },
      error: (err) => {
        // ¡Error! Mostramos el mensaje del backend y paramos la carga
        console.error('Error en la predicción:', err);
        // El error.error.detail es donde FastAPI suele poner los mensajes de HTTPException
        this.errorMessage = err.error?.detail || 'Ocurrió un error inesperado al predecir.';
        this.isLoading = false;
      }
    });
  }
}