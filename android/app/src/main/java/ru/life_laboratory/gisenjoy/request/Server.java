package ru.life_laboratory.gisenjoy.request;

import org.json.JSONObject;

import java.util.List;

import retrofit2.Call;
import retrofit2.http.GET;
import retrofit2.http.Query;
import ru.life_laboratory.gisenjoy.MainActivity;

public interface Server {
    // получение точек для карты
    @GET("geo")
    Call<Routes> getRoutes(@Query("data") JSONObject data);

    // авторизация
    @GET("auth")
    Call<Auth> auth(@Query("data") JSONObject data);

    @GET("registration")
    Call<String> register(@Query("data") JSONObject data);

    @GET("logout")
    Call<Auth> logout(@Query("session") String UUID);

    @GET("route")
    Call<Msg> saveRoute(@Query("param") String param, @Query("data") String data);

    @GET("route")
    Call<PublicRoutes> getPublicRoute(@Query("param") String param);

    @GET("filter")
    Call<Data> getFilters();

    // построение маршрута
    @GET("/maps/api/directions/json")
    Call<MainActivity.RouteResponse> getRoute(@Query(value = "origin") String position,
                                              @Query(value = "destination") String destination,
                                              @Query("waypoints") String waypoints,
                                              @Query("language") String language,
                                              @Query("mode") String mode);

    class Data {
        public List<String> data;
    }

    class Msg {
        public String Answer;
    }

    class Auth {
        public DataAuth Data;
        public String Answer;
        public class DataAuth {
            public String UUID;
            public String error_info;
        }
        public String toString(){
            return Answer + " UUID: " + Data.UUID;
        }
    }

    class SaveRoute {
        public String Is_private;
        public String Score;
        public String Name;
        public String UUID;
        public Routes.Route Route;
    }

    public class PublicRoutes {
        public String Answer;
        public List<PublicRoute> Data;
    }

    public class PublicRoute {
        public String name;
        public float score;
        public int id_route;
        public Routes.Route route;
    }

}
