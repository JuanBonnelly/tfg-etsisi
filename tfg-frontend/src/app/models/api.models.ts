
export interface Team {
  equipo_id: string;
  nombre: string;
  abreviatura: string;
}

export interface PredictionRequest {
  local_team_name: string;
  visitor_team_name: string;
  match_date: string; 
}

export interface PredictionResponse {
  predicted_result: string; 
  probabilities: {
    'Victoria Local': number;
    'Empate': number;
    'Victoria Visitante': number;
  };
  explanations: string[];
}