import { Injectable } from '@angular/core';
import { Filters } from './filters';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs/Observable';

@Injectable()
export class FiltersService {
  constructor(private http: HttpClient) {}

  getFilters (): Observable<Filters> {
    const url = 'http://90.189.132.25:13451/filter';

    return new Observable<Filters>(observer => {
      this.http.get<Filters>(url)
        .subscribe(
          data => observer.next(data),
          error => {
            observer.error(error);
          }
        );
    });
  }
}
