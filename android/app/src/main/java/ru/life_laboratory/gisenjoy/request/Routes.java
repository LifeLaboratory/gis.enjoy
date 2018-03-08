package ru.life_laboratory.gisenjoy.request;

import java.util.List;

public class Routes {
    public class Route {
        private List<String> name;
        private List<Integer> time;
        private List<String> descr;
        private List<Double> Y;
        private List<Double> X;
        private List<String> type;

        public List<String> getNames() { return this.name; }
        public List<Integer> getTime() { return this.time; }
        public List<String> getDescr() { return this.descr; }
        public List<Double> getY() { return this.Y; }
        public List<Double> getX() { return this.X; }
        public List<String> getType() { return this.type; }
        public String getStrNames() {
            String Result = "";
            for(String n : name){
                Result = Result.concat(n.concat("->"));
            }
            return Result.substring(2, Result.length() - 4);
        }
        public String getStrCoord(int position) { return  String.valueOf(this.X.get(position)).concat(",").concat(String.valueOf(this.Y.get(position))); }
    }
    private List<Route> route;

    public List<Route> getRoutes() { return this.route; }

    public Route getRoute(int position) { return this.route.get(position); }
}
