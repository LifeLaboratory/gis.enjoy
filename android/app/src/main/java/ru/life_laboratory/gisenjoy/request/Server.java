package ru.life_laboratory.gisenjoy.request;

import org.json.JSONObject;

import retrofit2.Call;
import retrofit2.http.GET;
import retrofit2.http.Query;
import ru.life_laboratory.gisenjoy.MainActivity;

public interface Server {
    @GET("geo")
    Call<Routes> getRoutes(@Query("data") JSONObject data);

    @GET("/maps/api/directions/json")
    Call<MainActivity.RouteResponse> getRoute(@Query(value = "origin") String position,
                                              @Query(value = "destination") String destination,
                                              @Query("waypoints") String waypoints,
                                              @Query("language") String language,
                                              @Query("mode") String mode);
}
