package ru.life_laboratory.gisenjoy.utils;


import android.app.DialogFragment;
import android.content.Context;
import android.os.Bundle;
import android.support.annotation.Nullable;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.AdapterView;
import android.widget.ArrayAdapter;
import android.widget.ListView;

import com.google.android.gms.maps.GoogleMap;

import java.util.ArrayList;
import java.util.List;

import ru.life_laboratory.gisenjoy.MainActivity;
import ru.life_laboratory.gisenjoy.R;
import ru.life_laboratory.gisenjoy.request.Routes;

public class RouteListDialog extends DialogFragment {

    private Routes routes;
    private View v;
    private Context context;
    private MainActivity mapActivity;
    private GoogleMap map;

    public void setData(Context context, Routes routes, MainActivity main, GoogleMap map){
        this.routes = routes;
        this.context = context;
        this.mapActivity = main;
        this.map = map;
    }

    @Nullable
    @Override
    public View onCreateView(LayoutInflater inflater, @Nullable ViewGroup container, Bundle savedInstanceState) {
        getDialog().setTitle("Доступные маршруты");
        v = inflater.inflate(R.layout.route_list_dialog, null);
        ListView listView = (ListView) v.findViewById(R.id.routers_list);
        List<String> forList = new ArrayList<>();
        for(Routes.Route route : this.routes.getRoutes()){
            forList.add(route.getStrNames());
        }
        ArrayAdapter<String> adapter = new ArrayAdapter<>(this.context, R.layout.route_list_item, forList);
        listView.setAdapter(adapter);
        listView.setOnItemClickListener(new AdapterView.OnItemClickListener() {
            @Override
            public void onItemClick(AdapterView<?> parent, View view, int position, long id) {
                mapActivity.showRoute(map, routes.getRoute(position));
                dismiss();
            }
        });
        return v;
    }

    @Override
    public void onStart() {
        super.onStart();
    }
}
