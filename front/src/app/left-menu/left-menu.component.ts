import {Component, OnChanges, OnInit, EventEmitter, Input, Output} from '@angular/core';
import { LeftMenuService } from '../left-menu.service';
import { FiltersService } from '../filters.service';
import { Routes } from '../routes';

@Component({
  selector: 'app-left-menu',
  templateUrl: './left-menu.component.html',
  styleUrls: ['./left-menu.component.less']
})
export class LeftMenuComponent implements OnInit {
  filters: string[];
  selectedFilters: string[] = [];
  selectedRouteId: number;

  @Input() selectedMenu: string;
  @Input() routes: Routes;
  @Input() isActive: boolean;
  @Output() selectedRoute = new EventEmitter();
  @Output() sendSelectedFilters = new EventEmitter();

  logRoute() {
    console.log(typeof this.routes);
    console.log(this.routes);
  }

  selectRoute(id) {
    if (id === 'none') {
      this.selectedRouteId = null;
      return;
    }

    console.log('selected route: ' + id);
    this.selectedRouteId = id;
    this.selectedRoute.emit(id);
  }

  constructor(private filtersService: FiltersService) { }

  ngOnInit() {
    this.getFilter();
  }

  getFilter() {
    this.filtersService.getFilters().subscribe(filters => {
      this.filters = filters.data;
      console.log(typeof this.filters);
      console.log(this.filters);
    });
  }

  viewRouteList(routes) {
    console.log('LeftMenuComponent: viewRouteList method');
    console.log(routes);
    console.log(this.routes);
    this.routes = routes;
  }

  toggleFilter(id) {
    const filter = this.filters[id];

    let pos = this.selectedFilters.indexOf(filter);
    if (pos === -1) {
      this.selectedFilters.push(filter);
    } else {
      this.selectedFilters.splice(pos, 1);
    }
    console.log(this.selectedFilters);
    this.sendSelectedFilters.emit(this.selectedFilters);
  }

  clearSelectedFilters() {
    this.selectedFilters = [];
    this.sendSelectedFilters.emit(this.selectedFilters);
  }

  isFilterSelect(id): boolean {
    if (this.filters) {
      if (this.selectedFilters.indexOf(this.filters[id]) === -1) {
        return false;
      } else {
        return true;
      }
    }
  }

  isRouteSelect(id): boolean {
      if (id === this.selectedRouteId) {
        return true;
      } else {
        return false;
      }
  }
}
