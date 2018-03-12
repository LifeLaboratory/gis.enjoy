package ru.life_laboratory.gisenjoy.utils;

import java.util.concurrent.TimeUnit;

import okhttp3.OkHttpClient;

public class Constants {
    public static final String ServerAddr = "http://90.189.132.25:13451/";
    public static final String TAG = "GIS.ENJOY";

    public static final OkHttpClient okHttpClient = new OkHttpClient.Builder()
            .connectTimeout(60, TimeUnit.SECONDS)
            .writeTimeout(60, TimeUnit.SECONDS)
            .readTimeout(60, TimeUnit.SECONDS)
            .build();
}
