package ru.life_laboratory.gisenjoy;

import android.app.ProgressDialog;
import android.content.Context;
import android.content.DialogInterface;
import android.content.pm.PackageManager;
import android.content.res.Resources;
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
import android.support.v7.app.AlertDialog;
import android.support.v7.app.AppCompatActivity;
import android.support.v7.widget.Toolbar;
import android.text.InputType;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.Menu;
import android.view.MenuItem;
import android.view.View;
import android.view.ViewGroup;
import android.widget.AdapterView;
import android.widget.ArrayAdapter;
import android.widget.EditText;
import android.widget.ListView;
import android.widget.SeekBar;
import android.widget.Spinner;
import android.widget.TextView;
import android.widget.ThemedSpinnerAdapter;
import android.widget.Toast;

import com.google.android.gms.maps.CameraUpdateFactory;
import com.google.android.gms.maps.GoogleMap;
import com.google.android.gms.maps.OnMapReadyCallback;
import com.google.android.gms.maps.SupportMapFragment;
import com.google.android.gms.maps.model.BitmapDescriptorFactory;
import com.google.android.gms.maps.model.LatLng;
import com.google.android.gms.maps.model.LatLngBounds;
import com.google.android.gms.maps.model.MarkerOptions;
import com.google.android.gms.maps.model.PolylineOptions;
import com.google.gson.Gson;
import com.google.maps.android.PolyUtil;

import org.json.JSONException;
import org.json.JSONObject;
import org.w3c.dom.Text;

import java.util.ArrayList;
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
import ru.life_laboratory.gisenjoy.utils.Utilities;

public class MainActivity extends AppCompatActivity
        implements NavigationView.OnNavigationItemSelectedListener {

    private SupportMapFragment mapFragment;
    private static LatLng pointA, pointB;
    private boolean statusA = false;
    AlertDialog.Builder userDialog, loginDialogBuilder, registerDialogBuilder, priorityDialogBuilder, saveRoutesDialogBuilder;
    AlertDialog dialog = null, loginDialog = null, registerDialog = null, priorityDialog = null, saveRoutesDialog = null;
    String sex = "Man";
    int Time = 0;
    NavigationView navigationView;
    String UUID = null;
    Menu mainMenu;
    Routes.Route mainRoute = null;
    GoogleMap mainMap = null;

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
        navigationView = (NavigationView) findViewById(R.id.nav_view);
        navigationView.setNavigationItemSelectedListener(this);
        // если еще не авторизован
        navigationView.getMenu().getItem(0).setVisible(false);
        navigationView.getMenu().getItem(1).setVisible(false);
        navigationView.getMenu().getItem(2).setVisible(false);
        // если авторизован
//        navigationView.getMenu().getItem(3).setVisible(false);
//        navigationView.getMenu().getItem(4).setVisible(false);

        Utilities.checkLocationPermissions(this, 0);

        // подгрузка карты
        mapFragment = SupportMapFragment.newInstance();
        getSupportFragmentManager().beginTransaction().add(R.id.map_fragment, mapFragment).commit();
        mapFragment.getMapAsync(new OnMapReadyCallback() {
            @Override
            public void onMapReady(GoogleMap googleMap) {
                mainMap = googleMap;
                googleMap.getUiSettings().setCompassEnabled(true);
                googleMap.getUiSettings().setZoomControlsEnabled(true);
                googleMap.getUiSettings().setCompassEnabled(true);
                googleMap.getUiSettings().setMyLocationButtonEnabled(true);
                googleMap.moveCamera(CameraUpdateFactory.newLatLngZoom(new LatLng(53.346786, 83.777506), 12));
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
                            mainMenu.getItem(0).setVisible(false);
                            googleMap.clear();
                            pointA = latLng;
                            statusA = true;
                            Snackbar.make(mapFragment.getView(), "Необходимо выбрать точку финиша.", Snackbar.LENGTH_LONG)
                                    .setAction("Построить", new View.OnClickListener() {
                                        @Override
                                        public void onClick(View v) {
                                            Log.d(Constants.TAG, pointA.toString().concat(" ").concat(pointB.toString()));
                                            // получение времени, которое можем затратить
                                            AlertDialog.Builder builder = new AlertDialog.Builder(MainActivity.this);
                                            builder.setTitle("Сколько времени хотите использовать? (мин)");

                                            EditText input = new EditText(MainActivity.this);
                                            input.setInputType(InputType.TYPE_CLASS_NUMBER);
                                            builder.setView(input);
                                            builder.setPositiveButton("Далее", new DialogInterface.OnClickListener() {
                                                @Override
                                                public void onClick(DialogInterface dialogParam, int which) {
                                                    Log.d(Constants.TAG, input.getText().toString());
                                                    Time = Integer.valueOf(input.getText().toString());
                                                    priorityDialogBuilder = new AlertDialog.Builder(MainActivity.this);
                                                    priorityDialogBuilder.setTitle("Приоритеты");

                                                    ArrayAdapter<String> arrayAdapter = new ArrayAdapter<String>(MainActivity.this, android.R.layout.select_dialog_item);

                                                    Retrofit restAdapter = new Retrofit.Builder().baseUrl(Constants.ServerAddr)
                                                            .addConverterFactory(GsonConverterFactory.create()).client(Constants.okHttpClient).build();
                                                    Server filterService = restAdapter.create(Server.class);
                                                    Call<Server.Data> filters = filterService.getFilters();
                                                    filters.enqueue(new Callback<Server.Data>() {
                                                        @Override
                                                        public void onResponse(Call<Server.Data> call, Response<Server.Data> response) {
                                                            for(String filt : response.body().data){
                                                                arrayAdapter.add(filt);
                                                            }
                                                            arrayAdapter.notifyDataSetChanged();
                                                        }
                                                        @Override
                                                        public void onFailure(Call<Server.Data> call, Throwable t) {
                                                            Log.e(Constants.TAG, t.toString());
                                                        }
                                                    });

                                                    priorityDialogBuilder.setNegativeButton("Отмена", new DialogInterface.OnClickListener() {
                                                        @Override
                                                        public void onClick(DialogInterface dialog, int which) {
                                                            dialog.dismiss();
                                                        }
                                                    });

                                                    priorityDialogBuilder.setAdapter(arrayAdapter, null);

                                                    Filter data = new Filter();
                                                    Log.d(Constants.TAG, pointA.toString() + " " + pointB.toString());
                                                    data.setOrigin(pointA);
                                                    data.setDestination(pointB);
                                                    data.setTime(Time);

                                                    priorityDialogBuilder.setPositiveButton("Построить", new DialogInterface.OnClickListener() {
                                                        @Override
                                                        public void onClick(DialogInterface dialogInterface, int i) {
                                                            priorityDialog.dismiss();
                                                            ProgressDialog progressDialog = new ProgressDialog(MainActivity.this,
                                                                    R.style.Theme_AppCompat_DayNight_Dialog);
                                                            progressDialog.setIndeterminate(true);
                                                            progressDialog.setMessage("Построение предполагаемых маршрутов...");
                                                            progressDialog.setCancelable(false);
                                                            progressDialog.show();
                                                            Retrofit retrofit = new Retrofit.Builder().baseUrl(Constants.ServerAddr).
                                                                    addConverterFactory(GsonConverterFactory.create()).client(Constants.okHttpClient).build();
                                                            Server routes = retrofit.create(Server.class);

                                                            Call<Routes> routesCall = routes.getRoutes(data.getData());
                                                            routesCall.enqueue(new Callback<Routes>() {
                                                                @Override
                                                                public void onResponse(Call<Routes> call, Response<Routes> response) {
                                                                    if(response.body() != null) {
                                                                        if(UUID != null) {
                                                                            mainMenu.getItem(0).setVisible(true);
                                                                        }
                                                                        Routes body = response.body();
                                                                        if (body.getRoutes().size() > 0) {
                                                                            for (Routes.Route route : body.getRoutes()) {
                                                                                Log.d(Constants.TAG, route.getStrNames());
                                                                            }
                                                                            userDialog = new AlertDialog.Builder(MainActivity.this);
                                                                            userDialog.setCustomTitle(null);
                                                                            View v = getLayoutInflater().inflate(R.layout.route_list_dialog, null);
                                                                            ListView listView = (ListView) v.findViewById(R.id.routers_list);
                                                                            List<String> forList = new ArrayList<>();
                                                                            for(Routes.Route route : body.getRoutes()){
                                                                                forList.add(route.getStrNames());
                                                                            }
                                                                            ArrayAdapter<String> adapter = new ArrayAdapter<>(getApplicationContext(), R.layout.route_list_item, forList);
                                                                            listView.setAdapter(adapter);
                                                                            listView.setOnItemClickListener(new AdapterView.OnItemClickListener() {
                                                                                @Override
                                                                                public void onItemClick(AdapterView<?> parent, View view, int position, long id) {
                                                                                    showRoute(mainMap, body.getRoute(position));
                                                                                    dialog.dismiss();
                                                                                }
                                                                            });
                                                                            userDialog.setView(v);
                                                                            if(dialog == null) {
                                                                                dialog = userDialog.create();
                                                                                dialog.show();
                                                                            } else
                                                                                dialog.show();
                                                                            statusA = false;
                                                                        } else {
                                                                            Snackbar.make(mapFragment.getView(), "Not found", Snackbar.LENGTH_LONG).setAction("Action", null).show();
                                                                        }
                                                                    } else {
                                                                        Snackbar.make(mapFragment.getView(), "Нет соединения с сервером", Snackbar.LENGTH_LONG).setAction("Action", null).show();
                                                                    }
                                                                    progressDialog.dismiss();
                                                                }
                                                                @Override
                                                                public void onFailure(Call<Routes> call, Throwable t) {
                                                                    Snackbar.make(mapFragment.getView(), t.toString(), Snackbar.LENGTH_LONG).setAction("Action", null).show();
                                                                }
                                                            });
                                                        }
                                                    });
                                                    if(priorityDialog != null) {
                                                        priorityDialog.show();
                                                    } else {
                                                        priorityDialog = priorityDialogBuilder.create();
                                                        priorityDialog.getListView().setOnItemClickListener(new AdapterView.OnItemClickListener() {
                                                            @Override
                                                            public void onItemClick(AdapterView<?> adapterView, View view, int i, long l) {
                                                                String strName = arrayAdapter.getItem(i);
                                                                data.addPriority(strName);
                                                                arrayAdapter.remove(strName);
                                                                arrayAdapter.notifyDataSetChanged();
                                                                Log.d(Constants.TAG, strName);
                                                                Toast.makeText(getApplicationContext(), strName + " добавлен в приоритеты", Toast.LENGTH_SHORT).show();
                                                            }
                                                        });
                                                        priorityDialog.show();
                                                    }
                                                }
                                            });
                                            builder.show();
                                        }
                                    }).show();
                            Log.d(Constants.TAG, pointA.toString().concat(" <- PointA"));
                        } else { // выбор конечной точки
                            statusA = false;
                            pointB = latLng;
                            Log.d(Constants.TAG, pointA.toString().concat(" ").concat(pointB.toString()));
                            // получение времени, которое можем затратить
                            AlertDialog.Builder builder = new AlertDialog.Builder(MainActivity.this);
                            builder.setTitle("Сколько времени хотите использовать? (мин)");

                            EditText input = new EditText(MainActivity.this);
                            input.setInputType(InputType.TYPE_CLASS_NUMBER);
                            builder.setView(input);
                            builder.setPositiveButton("Далее", new DialogInterface.OnClickListener() {
                                @Override
                                public void onClick(DialogInterface dialogParam, int which) {
                                    Log.d(Constants.TAG, input.getText().toString());
                                    Time = Integer.valueOf(input.getText().toString());
                                    priorityDialogBuilder = new AlertDialog.Builder(MainActivity.this);
                                    priorityDialogBuilder.setTitle("Приоритеты");

                                    ArrayAdapter<String> arrayAdapter = new ArrayAdapter<String>(MainActivity.this, android.R.layout.select_dialog_item);

                                    Retrofit restAdapter = new Retrofit.Builder().baseUrl(Constants.ServerAddr)
                                            .addConverterFactory(GsonConverterFactory.create()).client(Constants.okHttpClient).build();
                                    Server filterService = restAdapter.create(Server.class);
                                    Call<Server.Data> filters = filterService.getFilters();
                                    filters.enqueue(new Callback<Server.Data>() {
                                        @Override
                                        public void onResponse(Call<Server.Data> call, Response<Server.Data> response) {
                                            for(String filt : response.body().data){
                                                arrayAdapter.add(filt);
                                            }
                                            arrayAdapter.notifyDataSetChanged();
                                        }
                                        @Override
                                        public void onFailure(Call<Server.Data> call, Throwable t) {
                                            Log.e(Constants.TAG, t.toString());
                                        }
                                    });

                                    priorityDialogBuilder.setNegativeButton("Отмена", new DialogInterface.OnClickListener() {
                                        @Override
                                        public void onClick(DialogInterface dialog, int which) {
                                            dialog.dismiss();
                                        }
                                    });

                                    priorityDialogBuilder.setAdapter(arrayAdapter, null);

                                    Filter data = new Filter();
                                    Log.d(Constants.TAG, pointA.toString() + " " + pointB.toString());
                                    data.setOrigin(pointA);
                                    data.setDestination(pointB);
                                    data.setTime(Time);

                                    priorityDialogBuilder.setPositiveButton("Построить", new DialogInterface.OnClickListener() {
                                        @Override
                                        public void onClick(DialogInterface dialogInterface, int i) {
                                            priorityDialog.dismiss();
                                            ProgressDialog progressDialog = new ProgressDialog(MainActivity.this,
                                                    R.style.Theme_AppCompat_DayNight_Dialog);
                                            progressDialog.setIndeterminate(true);
                                            progressDialog.setMessage("Построение предполагаемых маршрутов...");
                                            progressDialog.setCancelable(false);
                                            progressDialog.show();
                                            Retrofit retrofit = new Retrofit.Builder().baseUrl(Constants.ServerAddr).
                                                    addConverterFactory(GsonConverterFactory.create()).client(Constants.okHttpClient).build();
                                            Server routes = retrofit.create(Server.class);

                                            Call<Routes> routesCall = routes.getRoutes(data.getData());
                                            routesCall.enqueue(new Callback<Routes>() {
                                                @Override
                                                public void onResponse(Call<Routes> call, Response<Routes> response) {
                                                    if(response.body() != null) {
                                                        if(UUID != null) {
                                                            mainMenu.getItem(0).setVisible(true);
                                                        }
                                                        Routes body = response.body();
                                                        if (body.getRoutes().size() > 0) {
                                                            for (Routes.Route route : body.getRoutes()) {
                                                                Log.d(Constants.TAG, route.getStrNames());
                                                            }
                                                            userDialog = new AlertDialog.Builder(MainActivity.this);
                                                            userDialog.setCustomTitle(null);
                                                            View v = getLayoutInflater().inflate(R.layout.route_list_dialog, null);
                                                            ListView listView = (ListView) v.findViewById(R.id.routers_list);
                                                            List<String> forList = new ArrayList<>();
                                                            for(Routes.Route route : body.getRoutes()){
                                                                forList.add(route.getStrNames());
                                                            }
                                                            ArrayAdapter<String> adapter = new ArrayAdapter<>(getApplicationContext(), R.layout.route_list_item, forList);
                                                            listView.setAdapter(adapter);
                                                            listView.setOnItemClickListener(new AdapterView.OnItemClickListener() {
                                                                @Override
                                                                public void onItemClick(AdapterView<?> parent, View view, int position, long id) {
                                                                    showRoute(mainMap, body.getRoute(position));
                                                                    dialog.dismiss();
                                                                }
                                                            });
                                                            userDialog.setView(v);
                                                            if(dialog == null) {
                                                                dialog = userDialog.create();
                                                                dialog.show();
                                                            } else
                                                                dialog.show();
                                                            statusA = false;
                                                        } else {
                                                            Snackbar.make(mapFragment.getView(), "Not found", Snackbar.LENGTH_LONG).setAction("Action", null).show();
                                                        }
                                                    } else {
                                                        Snackbar.make(mapFragment.getView(), "Нет соединения с сервером", Snackbar.LENGTH_LONG).setAction("Action", null).show();
                                                    }
                                                    progressDialog.dismiss();
                                                }
                                                @Override
                                                public void onFailure(Call<Routes> call, Throwable t) {
                                                    Snackbar.make(mapFragment.getView(), t.toString(), Snackbar.LENGTH_LONG).setAction("Action", null).show();
                                                }
                                            });
                                        }
                                    });
                                    if(priorityDialog != null) {
                                        priorityDialog.show();
                                    } else {
                                        priorityDialog = priorityDialogBuilder.create();
                                        priorityDialog.getListView().setOnItemClickListener(new AdapterView.OnItemClickListener() {
                                            @Override
                                            public void onItemClick(AdapterView<?> adapterView, View view, int i, long l) {
                                                String strName = arrayAdapter.getItem(i);
                                                data.addPriority(strName);
                                                arrayAdapter.remove(strName);
                                                arrayAdapter.notifyDataSetChanged();
                                                Log.d(Constants.TAG, strName);
                                                Toast.makeText(getApplicationContext(), strName + " добавлен в приоритеты", Toast.LENGTH_SHORT).show();
                                            }
                                        });
                                        priorityDialog.show();
                                    }
                                }
                            });
                            builder.show();
                            Snackbar.make(mapFragment.getView(), "Построение маршрута...", Snackbar.LENGTH_LONG).setAction("Action", null).show();
                            Log.d(Constants.TAG, pointB.toString().concat(" <- PointB"));
                        }
                    }
                });
            }
        });
    }

    // отображение маршрута
    public void showRoute(GoogleMap googleMap, Routes.Route route){
        this.mainRoute = route;
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
        ProgressDialog progressDialog = new ProgressDialog(MainActivity.this,
                R.style.Theme_AppCompat_DayNight_Dialog);
        progressDialog.setIndeterminate(true);
        progressDialog.setMessage("Построение маршрута...");
        progressDialog.show();
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
                progressDialog.dismiss();
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
        getMenuInflater().inflate(R.menu.activity_main_menu, menu);
        menu.getItem(0).setVisible(false);
        mainMenu = menu;
        return true;
    }

    @Override
    public boolean onOptionsItemSelected(MenuItem item) {
        switch (item.getItemId()){
            case R.id.save_route: { // сохранение маршрута
                if(mainRoute != null){
                    Server.SaveRoute routeForSave = new Server.SaveRoute();
                    routeForSave.Is_private = "false";
                    routeForSave.Name = "Test1";

                    AlertDialog.Builder alertBuilder = new AlertDialog.Builder(MainActivity.this);
                    alertBuilder.setCancelable(true);
                    alertBuilder.setTitle("Название маршрута");

                    EditText nameEdit = new EditText(MainActivity.this);
                    alertBuilder.setView(nameEdit);

                    alertBuilder.setPositiveButton("Далее", new DialogInterface.OnClickListener() {
                        @Override
                        public void onClick(DialogInterface dialogInterface, int i) {
                            routeForSave.Name = nameEdit.getText().toString();
                            routeForSave.UUID = UUID;
                            routeForSave.Route = mainRoute;

                            AlertDialog.Builder alertBuilder = new AlertDialog.Builder(MainActivity.this);
                            alertBuilder.setCancelable(true);
                            alertBuilder.setTitle("Оценка маршрута");

                            SeekBar scoreEdit = new SeekBar(MainActivity.this);
                            scoreEdit.setMax(5);
                            alertBuilder.setView(scoreEdit);

                            alertBuilder.setPositiveButton("Сохранить", new DialogInterface.OnClickListener() {
                                @Override
                                public void onClick(DialogInterface dialogInterface, int i) {
                                    routeForSave.Score = String.valueOf(scoreEdit.getProgress());
                                    Retrofit restAdapter = new Retrofit.Builder().baseUrl(Constants.ServerAddr)
                                            .addConverterFactory(GsonConverterFactory.create()).client(Constants.okHttpClient).build();
                                    Server routeService = restAdapter.create(Server.class);
                                    Gson gson = new Gson();
                                    String jsonRouteForSave = gson.toJson(routeForSave);
                                    Call<Server.Msg> routeSave = routeService.saveRoute("add", jsonRouteForSave);
                                    routeSave.enqueue(new Callback<Server.Msg>() {
                                        @Override
                                        public void onResponse(Call<Server.Msg> call, Response<Server.Msg> response) {
                                            Snackbar.make(mapFragment.getView(), "Маршрут сохранен", Snackbar.LENGTH_LONG).setAction("Action", null).show();
                                            Log.d(Constants.TAG, response.body().Answer);
                                        }
                                        @Override
                                        public void onFailure(Call<Server.Msg> call, Throwable t) {
                                            Log.e(Constants.TAG, t.toString());
                                            Snackbar.make(mapFragment.getView(), t.toString(), Snackbar.LENGTH_LONG).setAction("Action", null).show();
                                        }
                                    });
                                }
                            });

                            alertBuilder.setNegativeButton("Отмена", new DialogInterface.OnClickListener() {
                                @Override
                                public void onClick(DialogInterface dialogInterface, int i) { }
                            });

                            AlertDialog alert = alertBuilder.create();
                            alert.show();
                        }
                    });
                    alertBuilder.setNeutralButton("Отмена", new DialogInterface.OnClickListener() {
                        @Override
                        public void onClick(DialogInterface dialogInterface, int i) {}
                    });

                    AlertDialog alert = alertBuilder.create();
                    alert.show();
                } else {
                    Toast.makeText(getApplicationContext(), "Необходимо выбрать маршрут", Toast.LENGTH_SHORT).show();
                }
            }; break;
        }
        return super.onOptionsItemSelected(item);
    }

    @SuppressWarnings("StatementWithEmptyBody")
    @Override
    public boolean onNavigationItemSelected(MenuItem item) {
        int id = item.getItemId();
        switch(id){
            case R.id.nav_user: { // личный кабинет
                Snackbar.make(mapFragment.getView(), "В разработке", Snackbar.LENGTH_LONG).setAction("Action", null).show();
            }; break;
            case R.id.nav_login: { // авторизация
                if (loginDialog == null){
                    loginDialogBuilder = new AlertDialog.Builder(MainActivity.this);
                    loginDialogBuilder.setCustomTitle(null);
                    loginDialogBuilder.setTitle("Авторизация");
                    View v = getLayoutInflater().inflate(R.layout.user_login_dialog, null);
                    EditText loginEdit = (EditText) v.findViewById(R.id.user_login);
                    EditText passwordEdit = (EditText) v.findViewById(R.id.user_password);
                    loginDialogBuilder.setView(v);
                    loginDialogBuilder.setPositiveButton("Вход", new DialogInterface.OnClickListener() {
                        @Override
                        public void onClick(DialogInterface dialogInterface, int i) {
                            try {
                                JSONObject objForLogin = new JSONObject();
                                objForLogin.put("Login",loginEdit.getText().toString());
                                objForLogin.put("Password",passwordEdit.getText().toString());
                                Log.d(Constants.TAG, objForLogin.toString());
                                Retrofit retrofit = new Retrofit.Builder().baseUrl(Constants.ServerAddr).
                                        addConverterFactory(GsonConverterFactory.create()).client(Constants.okHttpClient).build();
                                Server auth = retrofit.create(Server.class);
                                Call<Server.Auth> authCall = auth.auth(objForLogin);
                                authCall.enqueue(new Callback<Server.Auth>() {
                                    @Override
                                    public void onResponse(Call<Server.Auth> call, Response<Server.Auth> response) {
                                        Log.d(Constants.TAG, response.body().Answer);
                                        if(response.body().Answer.equals("Success")) {
                                            Log.d(Constants.TAG, response.body().toString());
                                            loginDialog.dismiss();
                                            Toast.makeText(getApplicationContext(), "Успех", Toast.LENGTH_SHORT).show();
                                            // если еще не авторизован
                                            navigationView.getMenu().getItem(0).setVisible(true);
                                            navigationView.getMenu().getItem(1).setVisible(true);
                                            navigationView.getMenu().getItem(2).setVisible(true);
                                            // если авторизован
                                            navigationView.getMenu().getItem(3).setVisible(false);
                                            navigationView.getMenu().getItem(4).setVisible(false);
                                            UUID = response.body().Data.UUID;
                                            Log.d(Constants.TAG, UUID);
                                        } else if(response.body().Answer.equals("Warning")) {
                                            Toast.makeText(getApplicationContext(), response.body().Data.error_info, Toast.LENGTH_SHORT).show();
                                        }
                                    }
                                    @Override
                                    public void onFailure(Call<Server.Auth> call, Throwable t) {
                                        Log.e(Constants.TAG, t.toString());
                                    }
                                });
                            } catch (JSONException e) {
                                Log.e(Constants.TAG, e.toString().concat(" <- error from MainActivity.Register"));
                            }
                            loginDialog.dismiss();
                        }
                    });
                    loginDialogBuilder.setNegativeButton("Отмена", new DialogInterface.OnClickListener() {
                        @Override
                        public void onClick(DialogInterface dialogInterface, int i) {
                            loginDialog.dismiss();
                        }
                    });
                    loginDialog = loginDialogBuilder.create();
                    loginDialog.show();
                } else {
                    loginDialog.show();
                }
            }; break;
            case R.id.nav_register: { // регистрация
                if (registerDialog == null){
                    registerDialogBuilder = new AlertDialog.Builder(MainActivity.this);
                    registerDialogBuilder.setCustomTitle(null);
                    registerDialogBuilder.setTitle("Регистрация");
                    View v = getLayoutInflater().inflate(R.layout.user_register_dialog, null);
                    EditText loginEdit = (EditText) v.findViewById(R.id.user_login);
                    EditText passwordEdit = (EditText) v.findViewById(R.id.user_password);
                    EditText rePasswordEdit = (EditText) v.findViewById(R.id.user_re_password);
                    EditText nameEdit = (EditText) v.findViewById(R.id.user_name);
                    EditText emailEdit = (EditText) v.findViewById(R.id.user_email);
                    EditText cityEdit = (EditText) v.findViewById(R.id.user_city);
                    Spinner spinner = (Spinner) v.findViewById(R.id.user_sex);
                    spinner.setAdapter(new SexAdapter(
                            getApplicationContext(),
                            new String[]{
                                    "женский",
                                    "мужской"
                            }));
                    spinner.setOnItemSelectedListener(new AdapterView.OnItemSelectedListener() {
                        @Override
                        public void onItemSelected(AdapterView<?> adapterView, View view, int i, long l) {
                            Log.d(Constants.TAG, String.valueOf(i));
                            sex = i == 0 ? "WOMAN" : "MAN";
                        }
                        @Override
                        public void onNothingSelected(AdapterView<?> adapterView) { }
                    });
                    registerDialogBuilder.setView(v);
                    registerDialogBuilder.setPositiveButton("Регистрация", new DialogInterface.OnClickListener() {
                        @Override
                        public void onClick(DialogInterface dialogInterface, int i) {
                            if(!passwordEdit.getText().toString().equals(rePasswordEdit.getText().toString())){
                                passwordEdit.setError("Пароли не совпадают");
                                rePasswordEdit.setError("Пароли не совпадают");
                            } else {
                                passwordEdit.setError(null);
                                rePasswordEdit.setError(null);
                                try {
                                    JSONObject objForRegister = new JSONObject();
                                    objForRegister.put("Login",loginEdit.getText().toString());
                                    objForRegister.put("Password",passwordEdit.getText().toString());
                                    objForRegister.put("Name",nameEdit.getText().toString());
                                    objForRegister.put("Email",emailEdit.getText().toString());
                                    objForRegister.put("City",cityEdit.getText().toString());
                                    objForRegister.put("Sex",sex);
                                    Log.d(Constants.TAG, objForRegister.toString());
                                    Retrofit retrofit = new Retrofit.Builder().baseUrl(Constants.ServerAddr).
                                            addConverterFactory(GsonConverterFactory.create()).client(Constants.okHttpClient).build();
                                    Server register = retrofit.create(Server.class);
                                    Call<String> registerCall = register.register(objForRegister);
                                    registerCall.enqueue(new Callback<String>() {
                                        @Override
                                        public void onResponse(Call<String> call, Response<String> response) {
                                            Log.d(Constants.TAG, String.valueOf(response.body()));
                                        }
                                        @Override
                                        public void onFailure(Call<String> call, Throwable t) {
                                            Log.e(Constants.TAG, t.toString());
                                        }
                                    });
                                    registerDialog.dismiss();
                                } catch (JSONException e) {
                                    Log.e(Constants.TAG, e.toString().concat(" <- error from MainActivity.Register"));
                                }
                            }
                        }
                    });
                    registerDialogBuilder.setNegativeButton("Отмена", new DialogInterface.OnClickListener() {
                        @Override
                        public void onClick(DialogInterface dialogInterface, int i) {
                            registerDialog.dismiss();
                        }
                    });
                    registerDialog = registerDialogBuilder.create();
                    registerDialog.show();
                } else {
                    registerDialog.show();
                }
            }; break;
            case R.id.nav_exit: { // выход
                // если еще не авторизован
                navigationView.getMenu().getItem(0).setVisible(false);
                navigationView.getMenu().getItem(1).setVisible(false);
                navigationView.getMenu().getItem(2).setVisible(false);
                // если авторизован
                navigationView.getMenu().getItem(3).setVisible(true);
                navigationView.getMenu().getItem(4).setVisible(true);
                Retrofit retrofit = new Retrofit.Builder().baseUrl(Constants.ServerAddr).
                        addConverterFactory(GsonConverterFactory.create()).client(Constants.okHttpClient).build();
                Server logout = retrofit.create(Server.class);
                Call<Server.Auth> logoutCall = logout.logout(UUID);
                logoutCall.enqueue(new Callback<Server.Auth>() {
                    @Override
                    public void onResponse(Call<Server.Auth> call, Response<Server.Auth> response) {
                        Toast.makeText(getApplicationContext(), response.body().Answer, Toast.LENGTH_SHORT).show();
                        UUID = null;
                    }
                    @Override
                    public void onFailure(Call<Server.Auth> call, Throwable t) { }
                });
            }; break;
            case R.id.nav_routes: { // созраненные маршруты
                saveRoutesDialogBuilder = new AlertDialog.Builder(MainActivity.this);
                saveRoutesDialogBuilder.setCustomTitle(null);
                View v = getLayoutInflater().inflate(R.layout.route_list_dialog, null);
                ListView listView = (ListView) v.findViewById(R.id.routers_list);

                List<String> forList = new ArrayList<>();
                List<Routes.Route> routesPublic  = new ArrayList<>();
                ArrayAdapter<String> adapter = new ArrayAdapter<>(getApplicationContext(), R.layout.route_list_item, forList);
                listView.setAdapter(adapter);
                listView.setOnItemClickListener(new AdapterView.OnItemClickListener() {
                    @Override
                    public void onItemClick(AdapterView<?> parent, View view, int position, long id) {
                        showRoute(mainMap, routesPublic.get(position));
                        saveRoutesDialog.dismiss();
                    }
                });

                Retrofit retrofit = new Retrofit.Builder().baseUrl(Constants.ServerAddr).
                        addConverterFactory(GsonConverterFactory.create()).client(Constants.okHttpClient).build();
                Server route = retrofit.create(Server.class);
                Call<Server.PublicRoutes> publicRouters = route.getPublicRoute("get");
                publicRouters.enqueue(new Callback<Server.PublicRoutes>() {
                    @Override
                    public void onResponse(Call<Server.PublicRoutes> call, Response<Server.PublicRoutes> response) {
                        Log.d(Constants.TAG, response.body().toString());
                        for(Server.PublicRoute data : response.body().Data){
                            forList.add(data.name + " | " + data.score);
                            routesPublic.add(data.route);
                        }
                        adapter.notifyDataSetChanged();
                    }

                    @Override
                    public void onFailure(Call<Server.PublicRoutes> call, Throwable t) {}
                });

                saveRoutesDialogBuilder.setView(v);
                if(saveRoutesDialog == null) {
                    saveRoutesDialog = saveRoutesDialogBuilder.create();
                    saveRoutesDialog.show();
                } else
                    saveRoutesDialog.show();
            }; break;
        }
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

    public static class SexAdapter extends ArrayAdapter<String> implements ThemedSpinnerAdapter {
        android.support.v7.widget.ThemedSpinnerAdapter.Helper mDropDownHelper;

        SexAdapter(Context context, String[] objects) {
            super(context, R.layout.list_item_for_spiner, objects);
            mDropDownHelper = new android.support.v7.widget.ThemedSpinnerAdapter.Helper(context);
        }

        @Override
        public View getDropDownView(int position, View convertView, ViewGroup parent) {
            View view;
            if (convertView == null) {
                LayoutInflater inflater = mDropDownHelper.getDropDownViewInflater();
                view = inflater.inflate(R.layout.list_item_for_spiner, parent, false);
            } else {
                view = convertView;
            }
            TextView textView = (TextView) view.findViewById(android.R.id.text1);
            textView.setText(getItem(position));
            return view;
        }

        @Override
        public Resources.Theme getDropDownViewTheme() {
            return mDropDownHelper.getDropDownViewTheme();
        }

        @Override
        public void setDropDownViewTheme(Resources.Theme theme) {
            mDropDownHelper.setDropDownViewTheme(theme);
        }
    }
}
