package ru.life_laboratory.gisenjoy.request;

import org.json.JSONObject;

import retrofit2.Call;
import retrofit2.http.GET;
import retrofit2.http.Query;

public interface Server {
    @GET("geo")
    Call<Routes> getRoutes(@Query("data") JSONObject data);
}
