package ru.life_laboratory.gisenjoy;

import android.annotation.SuppressLint;
import android.content.Context;
import android.content.pm.PackageManager;
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

import com.google.android.gms.maps.CameraUpdateFactory;
import com.google.android.gms.maps.GoogleMap;
import com.google.android.gms.maps.OnMapReadyCallback;
import com.google.android.gms.maps.SupportMapFragment;
import com.google.android.gms.maps.model.LatLng;

import org.json.JSONException;
import org.json.JSONObject;

import java.util.ArrayList;
import java.util.List;

import retrofit2.Call;
import retrofit2.Callback;
import retrofit2.Response;
import retrofit2.Retrofit;
import retrofit2.converter.gson.GsonConverterFactory;
import ru.life_laboratory.gisenjoy.request.Constants;
import ru.life_laboratory.gisenjoy.request.Filter;
import ru.life_laboratory.gisenjoy.request.Routes;
import ru.life_laboratory.gisenjoy.request.Server;

public class MainActivity extends AppCompatActivity
        implements NavigationView.OnNavigationItemSelectedListener {

    private SupportMapFragment mapFragment;

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

        // подгрузка карты
        mapFragment = SupportMapFragment.newInstance();
        getSupportFragmentManager().beginTransaction().add(R.id.map_fragment, mapFragment).commit();
        mapFragment.getMapAsync(new OnMapReadyCallback() {
            @Override
            public void onMapReady(GoogleMap googleMap) {
                googleMap.getUiSettings().setCompassEnabled(true);
                googleMap.getUiSettings().setZoomControlsEnabled(true);
                googleMap.getUiSettings().setCompassEnabled(true);
                googleMap.moveCamera(CameraUpdateFactory.newLatLngZoom(new LatLng(55.7536207,37.6204141), 16));
                Snackbar.make(mapFragment.getView(), "Карта загружена", Snackbar.LENGTH_LONG).setAction("Action", null).show();

                if (ActivityCompat.checkSelfPermission(getApplicationContext(), android.Manifest.permission.ACCESS_FINE_LOCATION) != PackageManager.PERMISSION_GRANTED &&
                        ActivityCompat.checkSelfPermission(getApplicationContext(), android.Manifest.permission.ACCESS_COARSE_LOCATION) != PackageManager.PERMISSION_GRANTED) {
                    Snackbar.make(mapFragment.getView(), "Нет доступа к геопозиции", Snackbar.LENGTH_LONG).setAction("Action", null).show();
                    return;
                }
                googleMap.setMyLocationEnabled(true);
            }
        });

        // пример получения маршрутов
        Retrofit retrofit = new Retrofit.Builder().baseUrl(Constants.ServerAddr).
                addConverterFactory(GsonConverterFactory.create()).client(Constants.okHttpClient).build();
        Server routes = retrofit.create(Server.class);

        Filter data = new Filter();
        data.setOrigin(55.76721929882096,37.5531281614891);
        data.setDestination(55.75408367251468,37.6190461302391);
        data.setPriority("Памятник","Театр","Музей","Парк","Галерея");
        data.setTime(480);

        Call<Routes> routesCall = routes.getRoutes(data.getData());
        routesCall.enqueue(new Callback<Routes>() {
            @Override
            public void onResponse(Call<Routes> call, Response<Routes> response) {
                if(response.body() != null) {
                    Log.d(Constants.TAG, response.body().toString());
                    Routes body = response.body();
                    if (!body.getMessage().equals("ok")) {
                        for (Routes.Route route : body.getRoutes()) {
                            for (String name : route.getNames()) {
                                Log.i(Constants.TAG, name);
                            }
                        }
                    } else {
                        Snackbar.make(mapFragment.getView(), body.getMessage(), Snackbar.LENGTH_LONG).setAction("Action", null).show();
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
}
