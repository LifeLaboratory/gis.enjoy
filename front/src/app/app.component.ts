import { Component } from '@angular/core';
import { Routes } from './routes';
import { MapComponent } from './map/map.component';
import { ViewEncapsulation } from "@angular/core";

import { Coordinates } from './coordinates';


@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css'],
  encapsulation: ViewEncapsulation.None
})
export class AppComponent {
  constructor( private mapComponent: MapComponent) { }


  // selectedLeftMenu = 'routes';
  // routes: Routes;
/*

  selectLeftMenu(menu: string) {
    this.selectedLeftMenu = menu;
    console.log(this.selectedLeftMenu);
  }
*/
/*

  getRouteFromMenu(event) {
    this.mapComponent.getRoutes();
  }
*/
/*
  setRoutes(routes: Routes) {
    console.log('AppComponent: setRoutes');

    this.routes = routes;
    console.log(this.routes);
  }
  */
}
