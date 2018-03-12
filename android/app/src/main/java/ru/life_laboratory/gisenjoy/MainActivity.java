package ru.life_laboratory.gisenjoy;

import android.content.Context;
import android.content.pm.PackageManager;
import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.os.Bundle;
import android.support.design.widget.NavigationView;
import android.support.design.widget.Snackbar;
import android.support.multidex.MultiDex;
import android.support.v4.app.ActivityCompat;
import android.support.v4.view.GravityCompat;
import android.support.v4.widget.DrawerLayout;
import android.support.v7.app.ActionBarDrawerToggle;
import android.support.v7.app.AppCompatActivity;
import android.support.v7.widget.Toolbar;
import android.util.Log;
import android.view.Menu;
import android.view.MenuItem;
import android.view.View;

import com.google.android.gms.maps.CameraUpdateFactory;
import com.google.android.gms.maps.GoogleMap;
import com.google.android.gms.maps.OnMapReadyCallback;
import com.google.android.gms.maps.SupportMapFragment;
import com.google.android.gms.maps.model.BitmapDescriptorFactory;
import com.google.android.gms.maps.model.LatLng;
import com.google.android.gms.maps.model.LatLngBounds;
import com.google.android.gms.maps.model.MarkerOptions;
import com.google.android.gms.maps.model.PolylineOptions;
import com.google.maps.android.PolyUtil;

import java.util.List;

import retrofit2.Call;
import retrofit2.Callback;
import retrofit2.Response;
import retrofit2.Retrofit;
import retrofit2.converter.gson.GsonConverterFactory;
import ru.life_laboratory.gisenjoy.utils.Constants;
import ru.life_laboratory.gisenjoy.request.Filter;
import ru.life_laboratory.gisenjoy.request.Routes;
import ru.life_laboratory.gisenjoy.request.Server;
import ru.life_laboratory.gisenjoy.utils.RouteListDialog;
import ru.life_laboratory.gisenjoy.utils.Utilities;

public class MainActivity extends AppCompatActivity
        implements NavigationView.OnNavigationItemSelectedListener {

    private SupportMapFragment mapFragment;
    private LatLng pointA, pointB;
    private boolean statusA = false;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        Toolbar toolbar = (Toolbar) findViewById(R.id.toolbar);
        setSupportActionBar(toolbar);

        // боковое меню
        DrawerLayout drawer = (DrawerLayout) findViewById(R.id.drawer_layout);
        ActionBarDrawerToggle toggle = new ActionBarDrawerToggle(
                this, drawer, toolbar, R.string.navigation_drawer_open, R.string.navigation_drawer_close);
        drawer.addDrawerListener(toggle);
        toggle.syncState();
        NavigationView navigationView = (NavigationView) findViewById(R.id.nav_view);
        navigationView.setNavigationItemSelectedListener(this);

        Utilities.checkLocationPermissions(this, 0);

        // подгрузка карты
        mapFragment = SupportMapFragment.newInstance();
        getSupportFragmentManager().beginTransaction().add(R.id.map_fragment, mapFragment).commit();
        mapFragment.getMapAsync(new OnMapReadyCallback() {
            @Override
            public void onMapReady(GoogleMap googleMap) {
                googleMap.getUiSettings().setCompassEnabled(true);
                googleMap.getUiSettings().setZoomControlsEnabled(true);
                googleMap.getUiSettings().setCompassEnabled(true);
                googleMap.moveCamera(CameraUpdateFactory.newLatLngZoom(new LatLng(55.027412240599176,82.93513591522219), 12));
                Snackbar.make(mapFragment.getView(), "Карта загружена. Необходимо выбрать точку старта.", Snackbar.LENGTH_LONG).setAction("Action", null).show();

                if (ActivityCompat.checkSelfPermission(getApplicationContext(), android.Manifest.permission.ACCESS_FINE_LOCATION) != PackageManager.PERMISSION_GRANTED &&
                        ActivityCompat.checkSelfPermission(getApplicationContext(), android.Manifest.permission.ACCESS_COARSE_LOCATION) != PackageManager.PERMISSION_GRANTED) {
                    Snackbar.make(mapFragment.getView(), "Нет доступа к геопозиции", Snackbar.LENGTH_LONG).setAction("Action", null).show();
                    return;
                }
                googleMap.setMyLocationEnabled(true);

                // выбор точки
                googleMap.setOnMapClickListener(new GoogleMap.OnMapClickListener() {
                    @Override
                    public void onMapClick(LatLng latLng) {
                        if(!statusA){ // выбор первой точки
                            pointA = latLng;
                            statusA = true;
                            // TODO: добавить action для построения маршрута по одной точке
                            Snackbar.make(mapFragment.getView(), "Необходимо выбрать точку финиша.", Snackbar.LENGTH_LONG)
                                    .setAction("Построить", new View.OnClickListener() {
                                        @Override
                                        public void onClick(View v) {
                                            getRoutes(pointA, pointA, googleMap);
                                        }
                                    }).show();
                        } else { // выбор конечной точки
                            pointB = latLng;
                            getRoutes(pointA, pointB, googleMap);
                            Snackbar.make(mapFragment.getView(), "Построение маршрута...", Snackbar.LENGTH_LONG).setAction("Action", null).show();
                        }
                    }
                });
            }
        });
    }

    // получение маршрутов и вывод диалогового окна выбора маршрута
    private void getRoutes(LatLng pointA, LatLng pointB, GoogleMap googleMap){
        Retrofit retrofit = new Retrofit.Builder().baseUrl(Constants.ServerAddr).
                addConverterFactory(GsonConverterFactory.create()).client(Constants.okHttpClient).build();
        Server routes = retrofit.create(Server.class);

        Filter data = new Filter();
        data.setOrigin(pointA);
        data.setDestination(pointB);
        data.setPriority("Памятник","Театр","Музей","Парк","Галерея");
        data.setTime(60);

        Call<Routes> routesCall = routes.getRoutes(data.getData());
        routesCall.enqueue(new Callback<Routes>() {
            @Override
            public void onResponse(Call<Routes> call, Response<Routes> response) {
                if(response.body() != null) {
                    Routes body = response.body();
                    if (body.getRoutes().size() > 0) {
                        for (Routes.Route route : body.getRoutes()) {
                            Log.d(Constants.TAG, route.getStrNames());
                        }
                        RouteListDialog routeDialog = new RouteListDialog();
                        routeDialog.setData(getApplicationContext(), body, MainActivity.this, googleMap);
                        routeDialog.show(getFragmentManager(), "Error");
                    } else {
                        Snackbar.make(mapFragment.getView(), "Not found", Snackbar.LENGTH_LONG).setAction("Action", null).show();
                    }
                } else {
                    Snackbar.make(mapFragment.getView(), "Нет соединения с сервером", Snackbar.LENGTH_LONG).setAction("Action", null).show();
                }
            }
            @Override
            public void onFailure(Call<Routes> call, Throwable t) {
                Snackbar.make(mapFragment.getView(), t.toString(), Snackbar.LENGTH_LONG).setAction("Action", null).show();
            }
        });
    }

    // отображение маршрута
    final public void showRoute(GoogleMap googleMap, Routes.Route route){
        LatLngBounds.Builder latLngBuilder = new LatLngBounds.Builder();
        String waypoints = "";
        for (int i = 0; i < route.getNames().size(); i++) {
            if(i != 0 && i != route.getNames().size() - 1) {
                waypoints = waypoints.concat(route.getStrCoord(i)).concat("|");
                googleMap.addMarker(new MarkerOptions().position(new LatLng(route.getX().get(i), route.getY().get(i))).title(route.getNames().get(i))).setTag(route);
            } else if(i == 0){
                googleMap.addMarker(new MarkerOptions().position(new LatLng(route.getX().get(i), route.getY().get(i))).title(route.getNames().get(i)).icon(BitmapDescriptorFactory.fromBitmap(resizeMapIcons("point_a", 50, 50)))).setTag(route);
            } else if(i == route.getNames().size() - 1){
                googleMap.addMarker(new MarkerOptions().position(new LatLng(route.getX().get(i), route.getY().get(i))).title(route.getNames().get(i)).icon(BitmapDescriptorFactory.fromBitmap(resizeMapIcons("point_b", 50, 50)))).setTag(route);
            }
        }

        // получение маршрута
        Retrofit restAdapter = new Retrofit.Builder().baseUrl("https://maps.googleapis.com")
                .addConverterFactory(GsonConverterFactory.create()).client(Constants.okHttpClient).build();
        Server routeService = restAdapter.create(Server.class);
        Call<RouteResponse> routeResponse = routeService.getRoute(route.getStrCoord(0),
                route.getStrCoord(route.getNames().size() - 1), "optimize:true|".concat(waypoints), "ru", "walking");
        routeResponse.enqueue(new Callback<RouteResponse>() {
            @Override
            public void onResponse(Call<RouteResponse> call, Response<RouteResponse> response) {
                List <LatLng> points = PolyUtil.decode(response.body().getPoints());
                PolylineOptions line = new PolylineOptions();
                for(LatLng point : points){
                    line.add(point);
                    latLngBuilder.include(point);
                }
                googleMap.addPolyline(line);
            }
            @Override
            public void onFailure(Call<RouteResponse> call, Throwable t) {
                Log.e(Constants.TAG, t.toString());
            }
        });
    }

    // обработка нажатия кнопки "назад"
    @Override
    public void onBackPressed() {
        DrawerLayout drawer = (DrawerLayout) findViewById(R.id.drawer_layout);
        if (drawer.isDrawerOpen(GravityCompat.START)) {
            drawer.closeDrawer(GravityCompat.START);
        } else {
            super.onBackPressed();
        }
    }

    @Override
    public boolean onCreateOptionsMenu(Menu menu) {
        return true;
    }

    @Override
    public boolean onOptionsItemSelected(MenuItem item) {
        return super.onOptionsItemSelected(item);
    }

    @SuppressWarnings("StatementWithEmptyBody")
    @Override
    public boolean onNavigationItemSelected(MenuItem item) {
        int id = item.getItemId();
        return true;
    }

    @Override
    protected void attachBaseContext(Context newBase) {
        super.attachBaseContext(newBase);
        MultiDex.install(this);
    }

    // класс маршрута
    public class RouteResponse {

        public List<Route> routes;

        public String getPoints() {
            if(this.routes.size() > 0)
                return this.routes.get(0).overview_polyline.points;
            else
                return "";
        }

        class Route {
            OverviewPolyline overview_polyline;
        }

        class OverviewPolyline {
            String points;
        }
    }

    // изменение размера изображения
    public Bitmap resizeMapIcons(String iconName, int width, int height){
        Bitmap imageBitmap = BitmapFactory.decodeResource(getResources(),getResources().getIdentifier(iconName, "drawable", getPackageName()));
        Bitmap resizedBitmap = Bitmap.createScaledBitmap(imageBitmap, width, height, false);
        return resizedBitmap;
    }
}
