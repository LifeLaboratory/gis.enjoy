package ru.life_laboratory.gisenjoy.request;

import java.util.List;

public class Routes {
    public class Route {
        private List<String> name;
        private List<Integer> time;
        private List<String> descr;
        private List<Double> y;
        private List<Double> x;
        private List<String> type;

        public List<String> getNames() { return this.name; }
        public List<Integer> getTime() { return this.time; }
        public List<String> getDescr() { return this.descr; }
        public List<Double> getY() { return this.y; }
        public List<Double> getX() { return this.x; }
        public List<String> getType() { return this.type; }
    }
    private List<Route> route;

    public List<Route> getRoutes() { return this.route; }

    private String message = "ok";
    public String getMessage() { return this.message; }
}
