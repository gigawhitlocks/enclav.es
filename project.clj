(defproject the-known-net "0.0.1"
    :description "An experimental online meta-community."
    :dependencies
      [[org.clojure/clojure "1.4.0"]
            [ring "1.1.8"]
           ; [ring/ring-devel "0.2.5"]
           ; [ring/ring-jetty-adapter "0.2.5"]
           ; [compojure "0.4.0"]
          ;  [hiccup "0.2.6"]]
          [hiccup "1.0.2"]
           [compojure "1.1.5"]]
    :dev-dependencies
      [[lein-run "1.0.0-SNAPSHOT"]]
    :main the-known-net.core)


