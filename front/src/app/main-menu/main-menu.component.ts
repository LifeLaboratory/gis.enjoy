import {Component, OnInit, EventEmitter, Output, Input} from '@angular/core';
import { LeftMenuService } from '../left-menu.service';
import { MapService } from '../map.service';
// import { MapComponent } from '../map/map.component';
// import { MapRoutesService } from '../map-routes.service';

@Component({
  selector: 'app-main-menu',
  templateUrl: './main-menu.component.html',
  styleUrls: ['./main-menu.component.less']
})
export class MainMenuComponent implements OnInit {
  @Input() buildRoutesButtonStatus: boolean;
  @Input() selectedMenu: boolean;
  @Output() resetParam = new EventEmitter();
  @Output() randomRoute = new EventEmitter();

  constructor(private leftMenuService: LeftMenuService,
              private mapService: MapService
  ) { }

  @Output() getRoutes = new EventEmitter();

  buildRoutes() {
    if (this.buildRoutesButtonStatus) {
      this.getRoutes.emit(null);
    }
  }

  resetParameters() {
    this.resetParam.emit(null);
  }

  selectRandomRoute() {
    this.randomRoute.emit(null);
  }

  ngOnInit() {
  }
}

