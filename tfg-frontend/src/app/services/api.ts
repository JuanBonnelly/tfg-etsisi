import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

// Importamos los modelos de datos que definimos en la Tarea 3.1
import { Team, PredictionRequest, PredictionResponse } from '../models/api.models';

@Injectable({
  providedIn: 'root' // Esto hace que el servicio esté disponible en toda la aplicación
})
export class ApiService {

  // La URL base de nuestro backend. ¡Asegúrate de que tu backend corre en el puerto 8000!
  private readonly apiUrl = 'http://localhost:8000';

  // Angular nos "inyecta" el cliente HTTP a través del constructor.
  // Esto es la magia de la Inyección de Dependencias.
  constructor(private http: HttpClient) { }

  /**
   * Obtiene la lista completa de equipos desde el endpoint /teams.
   * @returns Un Observable que emitirá un array de objetos Team.
   */
  getTeams(): Observable<Team[]> {
    // Hacemos una petición GET a http://localhost:8000/teams
    // El <Team[]> le dice a TypeScript qué tipo de datos esperamos recibir.
    return this.http.get<Team[]>(`${this.apiUrl}/teams`);
  }

  /**
   * Envía una petición de predicción al endpoint /predict.
   * @param request El objeto con los datos del partido a predecir.
   * @returns Un Observable que emitirá un objeto PredictionResponse.
   */
  predictMatch(request: PredictionRequest): Observable<PredictionResponse> {
    // Hacemos una petición POST a http://localhost:8000/predict
    // El segundo argumento 'request' se enviará como el cuerpo (body) de la petición en formato JSON.
    return this.http.post<PredictionResponse>(`${this.apiUrl}/predict`, request);
  }
}