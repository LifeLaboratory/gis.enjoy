package ru.life_laboratory.gisenjoy.request;

import android.util.Log;

import com.google.android.gms.maps.model.LatLng;

import org.json.JSONException;
import org.json.JSONObject;

import java.util.ArrayList;

import ru.life_laboratory.gisenjoy.utils.Constants;

public class Filter {
    private JSONObject origin;
    private JSONObject destination;
    private ArrayList<String> priority;
    private int time = 999;

    public Filter(){
        origin = new JSONObject();
        destination = new JSONObject();
        priority = new ArrayList<String>();
    }

    public void setOrigin(LatLng point){
        try {
            this.origin.put("X", point.latitude);
            this.origin.put("Y", point.longitude);
        } catch (Exception e){
            Log.e(Constants.TAG, e.toString());
        }
    }

    public void setDestination(LatLng point){
        try {
            this.destination.put("X", point.latitude);
            this.destination.put("Y", point.longitude);
        } catch (Exception e){
            Log.e(Constants.TAG, e.toString());
        }
    }

    public void setPriority(String ... args){
        for(String pr : args) {
            this.priority.add(pr);
        }
    }

    public void setTime(int time){
        this.time = time;
    }

    public JSONObject getData(){
        try {
            JSONObject data = new JSONObject();
            data.put("origin", this.origin);
            data.put("destination", this.destination);
            data.put("time", this.time);
            data.put("priority", this.priority);
            Log.d(Constants.TAG, data.toString());
            return data;
        } catch (JSONException e) {
            Log.e(Constants.TAG, e.toString());
            return null;
        }
    }
}
