import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Coordinates } from './coordinates';
import { Routes } from './routes';
import { Observable } from 'rxjs/Observable';

@Injectable()
export class MapService {
  private routes: Routes = {
    route: []
  };

  constructor(private http: HttpClient) { }

  httpRoutes(direction, selectedFilters): Observable<string> {
    console.log('MapService: httpRoutes method start');
    console.log(direction);
    console.log(selectedFilters);

    if (direction && selectedFilters) {
      const obj = {
        origin: {
          X: direction.origin.lat,
          Y: direction.origin.lng
        },
        destination: {
          X: direction.destination.lat,
          Y: direction.destination.lng
        },
        time: 480,
        priority: selectedFilters
      };
      const results = JSON.stringify(obj);
    }

    // const url = 'http://90.189.132.25:13451/geo?data=' + results;
    // const url = 'http://90.189.132.25:13451/geo?data={"origin":{"X":53.341805,"Y":83.751245},"destination":{"X":53.344153,"Y":83.783141},"time":480,"priority":["парк","музей","памятник","кинотеатр"]}';

    const url = 'http://127.0.0.1:13451/list?data={}';
    console.log(url);
    return new Observable<string>(observer => {
      this.http.get<string>(url)
        .subscribe(
          data => observer.next(data),
          error => {
            observer.error(error);
          }
        );
    });
  }
}
