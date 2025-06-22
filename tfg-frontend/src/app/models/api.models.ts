// src/app/models/api.models.ts

export interface Team {
  equipo_id: string;
  nombre: string;
  abreviatura: string;
}

export interface PredictionRequest {
  local_team_name: string;
  visitor_team_name: string;
  match_date: string; // Formato 'YYYY-MM-DD'
}

export interface PredictionResponse {
  predicted_result: string; // 'Victoria Local', 'Empate', o 'Victoria Visitante'
  probabilities: {
    'Victoria Local': number;
    'Empate': number;
    'Victoria Visitante': number;
  };
}