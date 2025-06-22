import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';

// Importa los modelos que necesitaremos (aunque solo sea para tipado)
import { Team } from '../../models/api.models';
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
        console.log('¡Éxito! Equipos recibidos desde el backend:');
        console.table(this.teams); // console.table los muestra en una tabla bonita
      },
      // Esto se ejecuta si hay un error en la llamada
      error: (err) => {
        console.error('¡ERROR! No se pudieron obtener los equipos:', err);
        // Aquí podríamos mostrar un mensaje de error al usuario en el futuro
      }
    });
  }
}