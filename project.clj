(defproject the-known-net "0.0.1"
    :description "An experimental online meta-community."
    :dependencies
      [[org.clojure/clojure "1.4.0"]
            [ring "1.1.8"]
            [hiccup "1.0.2"]
            [sandbar/sandbar "0.4.0-SNAPSHOT"]
            [compojure "1.1.5"]
            [korma "0.3.0-RC2"] 
            [cssgen "0.2.6"]]
    :dev-dependencies
      [[lein-run "1.0.0-SNAPSHOT"]]
    :main the-known-net.core)


