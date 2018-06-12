import { Component, OnInit, Input, Output, EventEmitter, ViewChild } from '@angular/core';
import { Coordinates } from '../coordinates';
import { Routes } from '../routes';
import { MapService } from '../map.service';
import { LeftMenuService } from '../left-menu.service';

import { Direction } from '../direction';


import { LeftMenuComponent } from '../left-menu/left-menu.component';
import { MainMenuComponent } from '../main-menu/main-menu.component';


@Component({
  selector: 'app-map',
  templateUrl: './map.component.html',
  styleUrls: ['./map.component.less'],

})
export class MapComponent implements OnInit {
  constructor( public mapService: MapService,
               private leftMenuService: LeftMenuService,
  ) {}

  @Output() routesEmitter = new EventEmitter<Routes>();
  @ViewChild(MainMenuComponent) mainMenu: MainMenuComponent;
  @ViewChild(LeftMenuComponent) leftMenu: LeftMenuComponent;

  // нск
  // lat = 55.022887;
  // lng = 82.922912;

  // екб
  lat = 56.820071;
  lng = 60.621116;

  markers: Coordinates[] = [];
  clickStatus = 0;
  selectedFilters: string[] = [];
  waypoints = [];
  routes: Routes;


  /*
  routes = {
    "route": [
      {
        "name": ["Lenina", "duck", "fuck", "ducken"],
        "time": [20, 30, 40, 35],
        "descr": ["descr_lenina", "discr_duck", "discr_fuck", "duckduck"],
        "X": [56.845229, 56.839619, 56.840200, 56.841996],
        "type": ["park", "galery", "park", "park"],
        "Y": [60.645281, 60.647116, 60.654428, 60.658903]
      },
      {
        "name": ["Lenina", "duck", "ducken", "fuck"],
        "time": [20, 30, 35, 40],
        "descr": ["descr_lenina", "discr_duck", "duckduck", "discr_fuck"],
        "X": [56.845229, 56.839619, 56.841996, 56.840200],
        "type": ["park", "galery", "park", "park"],
        "Y": [60.645281, 60.647116, 60.658903, 60.654428]
      },
      {
        "name": ["Lenina", "duck", "fuck", "ducken"],
        "time": [20, 30, 40, 35],
        "descr": ["descr_lenina", "discr_duck", "discr_fuck", "duckduck"],
        "X": [56.845229, 56.839619, 56.840200, 56.841996],
        "type": ["park", "galery", "park", "park"],
        "Y": [60.645281, 60.647116, 60.654428, 60.658903]
      },
      {
        "name": ["Lenina", "duck", "fuck", "ducken"],
        "time": [20, 30, 40, 35],
        "descr": ["descr_lenina", "discr_duck", "discr_fuck", "duckduck"],
        "X": [56.845229, 56.839619, 56.840200, 56.841996],
        "type": ["park", "galery", "park", "park"],
        "Y": [60.645281, 60.647116, 60.654428, 60.658903]
      },
      {
        "name": ["Lenina", "duck", "fuck", "ducken"],
        "time": [20, 30, 40, 35],
        "descr": ["descr_lenina", "discr_duck", "discr_fuck", "duckduck"],
        "X": [56.845229, 56.839619, 56.840200, 56.841996],
        "type": ["park", "galery", "park", "park"],
        "Y": [60.645281, 60.647116, 60.654428, 60.658903]
      },
      {
        "name": ["Lenina", "duck", "fuck", "ducken"],
        "time": [20, 30, 40, 35],
        "descr": ["descr_lenina", "discr_duck", "discr_fuck", "duckduck"],
        "X": [56.845229, 56.839619, 56.840200, 56.841996],
        "type": ["park", "galery", "park", "park"],
        "Y": [60.645281, 60.647116, 60.654428, 60.658903]
      },
      {
        "name": ["Lenina", "duck", "fuck", "ducken"],
        "time": [20, 30, 40, 35],
        "descr": ["descr_lenina", "discr_duck", "discr_fuck", "duckduck"],
        "X": [56.845229, 56.839619, 56.840200, 56.841996],
        "type": ["park", "galery", "park", "park"],
        "Y": [60.645281, 60.647116, 60.654428, 60.658903]
      },
      {
        "name": ["Lenina", "duck", "fuck", "ducken"],
        "time": [20, 30, 40, 35],
        "descr": ["descr_lenina", "discr_duck", "discr_fuck", "duckduck"],
        "X": [56.845229, 56.839619, 56.840200, 56.841996],
        "type": ["park", "galery", "park", "park"],
        "Y": [60.645281, 60.647116, 60.654428, 60.658903]
      },
      {
        "name": ["Lenina", "duck", "fuck", "ducken"],
        "time": [20, 30, 40, 35],
        "descr": ["descr_lenina", "discr_duck", "discr_fuck", "duckduck"],
        "X": [56.845229, 56.839619, 56.840200, 56.841996],
        "type": ["park", "galery", "park", "park"],
        "Y": [60.645281, 60.647116, 60.654428, 60.658903]
      },
      {
        "name": ["Lenina", "duck", "fuck", "ducken"],
        "time": [20, 30, 40, 35],
        "descr": ["descr_lenina", "discr_duck", "discr_fuck", "duckduck"],
        "X": [56.845229, 56.839619, 56.840200, 56.841996],
        "type": ["park", "galery", "park", "park"],
        "Y": [60.645281, 60.647116, 60.654428, 60.658903]
      }
    ]
  };
  */

  selectedLeftMenu = 'filters';
  selectedMainMenu = 'main';
  leftMenuIsActive = false;
  buildRoutesButtonStatus = false;

  public show = false;


  // екб тест
  direction: Direction;

  public showDirection() {
    this.show = true;
  }

  public removeDirection() {
    this.show = false;
  }

  setLeftMenuStatus(status) {
    this.leftMenuIsActive = status;
  }

  selectLeftMenu(menu: string) {
    this.selectedLeftMenu = menu;
    console.log(this.selectedLeftMenu);
  }

  selectMainMenu(menu: string) {
    this.selectedMainMenu = menu;
    console.log(this.selectedMainMenu);
  }

  getSelectedFilters(selectedFilters) {
    this.selectedFilters = selectedFilters;
    if (this.selectedFilters.length > 0) {
      this.buildRoutesButtonStatus = true;
    } else {
      this.buildRoutesButtonStatus = false;
    }
  }

  clearSelectedFilters() {
    this.leftMenu.clearSelectedFilters();
  }

  ngOnInit() {

  }

  getDirection() {
    console.log('markers');
    console.log(this.markers);

    if (this.markers.length === 2) {
      this.direction = {
        origin: { lat: this.markers[0].lat, lng: this.markers[0].lng },
        destination: { lat: this.markers[1].lat, lng: this.markers[1].lng }
      };

      this.markers = [];
    } else {
      console.log('Точки заданы неверно');
      console.log('direction:');
      console.log(this.direction);
    }
  }

  getWaypoints(waypoints) {
    if (waypoints) {
      console.log('getWaypoints: waypoints is ok');
      this.waypoints = waypoints;
    } else { // Потом надо убрать, это для написано для теста
      this.waypoints = [
        { location: { lat: 55.033141, lng: 82.919235 }, stopover: true },
        { location: { lat: 55.029599, lng: 82.920866 }, stopover: true }
      ];
    }
  }

  clearWaypoints() {
    this.waypoints = [];
  }

  getRoutes() {
    console.log('map.component getRoutes method start');

    this.mapService.httpRoutes(this.direction, this.selectedFilters).subscribe(routes => {
      this.routes = JSON.parse(routes);
      console.log('routes was geted');
      console.log(this.routes);

      this.routesEmitter.emit(this.routes);

      this.leftMenu.viewRouteList(this.routes);
      this.selectLeftMenu('routes');
      this.selectMainMenu('route');
    });

    console.log('map.component getRoutes method end');
  }

  selectRoute(id) {
    this.getDirection();
    this.showDirection();
    if (id === 'random') {
      id = Math.floor(Math.random() * this.routes.route.length);
      this.leftMenu.selectRoute(id);
    }

    console.log(this.routes.route[id].X);

    this.waypoints = [];
    for (let i = 0; i < this.routes.route[id].X.length; i++) {
      console.log(i);
      // waypoints.push({location: { lat: this.routes.route[id].X[i], lng: this.routes.route[id].Y[i]}, stopover: true});

      // перепутанны X и Y, чтобы работал тестовый запрос, в котором перепутаны X и Y
      this.waypoints.push({location: { lat: this.routes.route[id].Y[i], lng: this.routes.route[id].X[i]}, stopover: true});
    }

    console.log('waypoints: ');
    console.log(this.waypoints);
  }

  placeMarker($event) {
    switch (this.clickStatus) {
      case 0:
        this.markers.push({ lat: $event.coords.lat, lng: $event.coords.lng });
        this.clickStatus++;

        console.log('markers: ');
        console.log(this.markers);

        break;
      case 1:
        this.markers.push({ lat: $event.coords.lat, lng: $event.coords.lng });
        this.clickStatus++;



        this.setLeftMenuStatus(true);

        console.log('markers: ');
        console.log(this.markers);

        break;
      case 2:
        this.resetParameters();
        break;
    }
  }

  resetParameters() {
    this.markers = [];
    this.setLeftMenuStatus(false);
    this.clickStatus = 0;
    this.waypoints = [];

    // сброс выбора маршрута
    this.leftMenu.selectRoute('none');

    this.removeDirection();
    this.selectLeftMenu('filters');
    this.selectMainMenu('main');

    console.log('markers: ');
    console.log(this.markers);

    this.clearSelectedFilters();
  }

}
