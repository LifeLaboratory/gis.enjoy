import { BrowserModule } from '@angular/platform-browser';
import { NgModule, Component } from '@angular/core';
import { AgmCoreModule } from '@agm/core';
import { AgmDirectionModule } from 'agm-direction';
import { AgmJsMarkerClustererModule } from '@agm/js-marker-clusterer';
import { HttpClientModule } from '@angular/common/http';


import { AppComponent } from './app.component';
import { MapComponent } from './map/map.component';

import { MapService } from './map.service';
import { MainMenuComponent } from './main-menu/main-menu.component';
import { LeftMenuComponent } from './left-menu/left-menu.component';

import {FiltersService} from './filters.service';
import {LeftMenuService} from './left-menu.service';


@NgModule({
  declarations: [
    AppComponent,
    MapComponent,
    MainMenuComponent,
    LeftMenuComponent,
  ],
  imports: [
    BrowserModule,
    AgmCoreModule.forRoot({
      apiKey: 'AIzaSyCIv-So_me7cBT7C2nUbPEyll_4pNq8iD4'
    }),
    HttpClientModule,
    AgmDirectionModule,
    AgmJsMarkerClustererModule
  ],
  providers: [
    MapService,
    MapComponent,
    FiltersService,
    LeftMenuService,
    LeftMenuComponent
  ],
  bootstrap: [AppComponent]
})
export class AppModule { }
