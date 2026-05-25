import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

import { Team, PredictionRequest, PredictionResponse } from '../models/api.models';

@Injectable({
  providedIn: 'root' 
})
export class ApiService {
  private readonly apiUrl = 'http://localhost:8000';

  constructor(private http: HttpClient) { }
  /**
   * @returns 
   */
  getTeams(): Observable<Team[]> {   
    return this.http.get<Team[]>(`${this.apiUrl}/teams`);
  }

  /**
   * @param request 
   * @returns 
   */
  predictMatch(request: PredictionRequest): Observable<PredictionResponse> {
    return this.http.post<PredictionResponse>(`${this.apiUrl}/predict`, request);
  }
}