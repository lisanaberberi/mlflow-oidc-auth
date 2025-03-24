import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable } from 'rxjs';
import { RegisteredModelPermission } from '../interfaces/user-data.interface';
import { AuthService } from './auth.service';
import { map, switchMap, delay, tap } from 'rxjs/operators';

@Injectable({
  providedIn: 'root'
})
export class ZenodoService {
  constructor(private http: HttpClient, private authService: AuthService) {}

  
  private delay(ms: number): Promise<void> {
    return new Promise(resolve => setTimeout(resolve, ms));
  }

  initiateZenodoOAuth(model: RegisteredModelPermission): Observable<string> {
    const headers = new HttpHeaders({ 'Accept': 'text/plain' });  // Explicit Accept header
    return this.http.get(`/zenodo/login?modelname=${model.name}`, { responseType: 'text', headers }).pipe(
      map(response => response)
    );
  }
  //   return this.http.get(`/zenodo/login?modelname=${model.name}`, { responseType: 'text' }).pipe(
  //     map(response => {
  //       // Now, the response is the raw redirect URL, so you can directly return it.
  //       return response;
  //     })
  //   );
  // }

  getAccessToken(): Observable<string> {
    // Introduce a delay of 2 seconds (2000 milliseconds)
    return this.http.get('/api/zenodo/token').pipe(
      map((response: any) => response.access_token)
    );
    delay(1000) // Delay the emission of the token by 2 seconds
  }

  // publishModelToZenodo(modelName: string, accessToken: string): Observable<any> {
  //   return this.http.post(`/zenodo/publish/${modelName}`, {}, {
  //     headers: {
  //       'Authorization': `Bearer ${accessToken}`
  //     }
  //   });
  // }
//   publishModelToZenodo(modelName: string, accessToken: string): Observable<any> {
//     const headers = new HttpHeaders({
//       'Content-Type': 'application/json',
//       'Authorization': `Bearer ${accessToken}`
//     });

//     // Assuming the backend expects a JSON body, even if it's empty
//     const body = {};

//     return this.http.post(`/zenodo/publish/${modelName}`, body, { headers });
//   }
// 
}