package ru.life_laboratory.gisenjoy;

import android.content.Context;
import android.os.Handler;
import android.os.StrictMode;
import android.support.multidex.MultiDex;
import android.support.multidex.MultiDexApplication;
import android.util.Log;

import ru.life_laboratory.gisenjoy.utils.Constants;

public class App extends MultiDexApplication implements Runnable {

    private static App Instance;
    public static volatile Handler applicationHandler = null;


    @Override
    public void onCreate() {
        super.onCreate();
        Log.d(Constants.TAG, "App");
        Instance = this;

        applicationHandler = new Handler(getMainLooper());

        new Thread(this).start();

        StrictMode.setThreadPolicy(new StrictMode.ThreadPolicy.Builder().detectDiskReads().detectDiskWrites().detectNetwork().penaltyLog().build());
    }



    public static App getInstance()
    {
        return Instance;
    }

    @Override
    public void run() {
//        NativeLoader.initNativeLibs(App.getInstance());
    }

    @Override
    protected void attachBaseContext(Context base) {
        super.attachBaseContext(base);
        MultiDex.install(this);
    }
}
